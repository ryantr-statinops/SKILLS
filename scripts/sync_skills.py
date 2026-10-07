#!/usr/bin/env python3
"""Sync selected skill directories into a project's agent directory."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import re
import tempfile

from bundles import load_bundle_registry, validate_bundle_registry

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
MANIFEST_NAME = ".skill-sync.json"
CATALOG_NAME = ".skill-catalog.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy selected SKILLS categories/skills into an agent directory."
    )
    parser.add_argument(
        "destination",
        type=Path,
        nargs="?",
        help="Target skills directory, e.g. project/.agent/skills",
    )
    parser.add_argument(
        "skills",
        nargs="*",
        help="Source paths relative to this repository, e.g. common/git or meta/skill-authoring",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="SKILLS repository root (defaults to this script's repository)",
    )
    parser.add_argument("--check", action="store_true", help="Validate inputs without copying")
    parser.add_argument("--update", action="store_true", help="Update a previously managed destination")
    parser.add_argument("--bundle", help="sync a named bundle instead of explicit skills")
    parser.add_argument("--list-bundles", action="store_true", help="list available bundles")
    return parser.parse_args()


def resolve_skill(source: Path, relative: str) -> Path:
    path = (source / relative).resolve()
    try:
        path.relative_to(source.resolve())
    except ValueError as exc:
        raise ValueError(f"skill path escapes source repository: {relative}") from exc
    if not path.is_dir():
        raise ValueError(f"skill directory does not exist: {relative}")
    if not (path / "SKILL.md").is_file():
        raise ValueError(f"skill directory has no SKILL.md: {relative}")
    return path


def load_source_bundles(source: Path) -> list[dict[str, object]]:
    registry_path = source / "data/bundles.json"
    skills_path = source / "data/skills.json"
    try:
        skill_registry = json.loads(skills_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid source skill registry: {skills_path}") from exc
    records = skill_registry.get("skills")
    if not isinstance(records, list):
        raise ValueError(f"invalid source skill registry: {skills_path}")
    try:
        return validate_bundle_registry(load_bundle_registry(registry_path), records)
    except ValueError as exc:
        raise ValueError(f"invalid source bundle registry: {registry_path}: {exc}") from exc


def load_source_skill_records(source: Path) -> list[dict[str, object]]:
    try:
        data = json.loads((source / "data/skills.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("invalid source skill registry") from exc
    records = data.get("skills")
    if not isinstance(records, list):
        raise ValueError("invalid source skill registry")
    return records


def resolve_bundle(source: Path, identifier: str) -> list[str]:
    for bundle in load_source_bundles(source):
        if bundle["id"] == identifier:
            return list(bundle["skills"])
    raise ValueError(f"unknown bundle: {identifier}")


def resolve_dependencies(source: Path, selected: list[str]) -> list[str]:
    records = {str(record["id"]): record for record in load_source_skill_records(source)}
    ordered: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str) -> None:
        if identifier in visiting:
            raise ValueError(f"cyclic skill dependency: {identifier}")
        if identifier in visited:
            return
        record = records.get(identifier)
        if record is None:
            raise ValueError(f"skill dependency is missing from registry: {identifier}")
        visiting.add(identifier)
        for required in record.get("requires", []):
            visit(str(required))
        visiting.remove(identifier)
        visited.add(identifier)
        ordered.append(identifier)

    for identifier in selected:
        visit(identifier)
    return ordered


def linked_resources(source: Path, skill: Path) -> list[Path]:
    """Return existing repository files referenced by a skill entrypoint."""
    entrypoint = skill / "SKILL.md"
    resources: list[Path] = []
    for raw_target in MARKDOWN_LINK_RE.findall(entrypoint.read_text(encoding="utf-8")):
        target = raw_target.split("#", 1)[0].strip().strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (entrypoint.parent / target).resolve()
        try:
            resolved.relative_to(source.resolve())
        except ValueError as exc:
            raise ValueError(f"linked resource escapes source repository: {target}") from exc
        if not resolved.exists():
            raise ValueError(f"linked resource does not exist: {target}")
        if not resolved.is_relative_to(skill.resolve()):
            resources.append(resolved)
    return resources


def export_targets(source: Path, destination: Path, skills: list[tuple[str, Path]]) -> list[tuple[Path, Path]]:
    targets: dict[Path, Path] = {}
    for relative, path in skills:
        targets[path] = destination / path.relative_to(source)
        for resource in linked_resources(source, path):
            targets[resource] = destination / resource.relative_to(source)

    selected: list[tuple[Path, Path]] = []
    covering_directories: list[Path] = []
    for path, target in sorted(targets.items(), key=lambda item: (len(item[0].parts), str(item[0]))):
        if any(path.is_relative_to(parent) for parent in covering_directories):
            continue
        selected.append((path, target))
        if path.is_dir():
            covering_directories.append(path)
    return sorted(selected, key=lambda item: str(item[1]))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_for(
    source: Path,
    bundle: str | None,
    selected: list[str],
    targets: list[tuple[Path, Path]],
) -> dict[str, object]:
    files: list[Path] = []
    for path, _ in targets:
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(item for item in path.rglob("*") if item.is_file())
    return {
        "schema_version": 1,
        "source": str(source),
        "bundle": bundle,
        "skills": selected,
        "files": [
            {
                "path": str(path.relative_to(source)),
                "sha256": sha256(path),
            }
            for path in sorted(files)
        ],
    }


def catalog_for(source: Path, selected: list[str]) -> dict[str, object]:
    records = {str(record["id"]): record for record in load_source_skill_records(source)}
    return {
        "schema_version": 2,
        "skills": [records[identifier] for identifier in selected],
    }


def flattened_files(targets: list[tuple[Path, Path]]) -> dict[str, tuple[Path, Path]]:
    flattened: dict[str, tuple[Path, Path]] = {}
    for source_path, target_path in targets:
        if source_path.is_file():
            flattened[str(source_path)] = (source_path, target_path)
        elif source_path.is_dir():
            for source_file in source_path.rglob("*"):
                if source_file.is_file():
                    target_file = target_path / source_file.relative_to(source_path)
                    flattened[str(source_file)] = (source_file, target_file)
    return flattened


def update_destination(
    source: Path,
    destination: Path,
    bundle: str | None,
    selected: list[str],
    targets: list[tuple[Path, Path]],
    check: bool,
) -> None:
    manifest_path = destination / MANIFEST_NAME
    if not manifest_path.is_file():
        raise ValueError("--update requires an existing .skill-sync.json manifest")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        old_files = {str(item["path"]): str(item["sha256"]) for item in manifest["files"]}
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid .skill-sync.json manifest") from exc

    new_files = flattened_files(targets)
    new_relative = {
        str(Path(source_path).relative_to(source)): pair
        for source_path, pair in new_files.items()
    }
    modified = []
    for relative, expected_hash in old_files.items():
        target = destination / relative
        if target.is_file() and sha256(target) != expected_hash:
            modified.append(str(target))
    if modified:
        raise ValueError("managed files were modified locally: " + ", ".join(modified))

    collisions = []
    for relative, (_, target) in new_relative.items():
        if target.exists() and (relative not in old_files or not target.is_file()):
            collisions.append(str(target))
        for parent in target.parents:
            if parent.exists() and not parent.is_dir():
                collisions.append(str(parent))
                break
    if collisions:
        raise ValueError("update target collision or non-directory ancestor: " + ", ".join(sorted(set(collisions))))

    catalog_path = destination / CATALOG_NAME
    if catalog_path.exists() and not catalog_path.is_file():
        raise ValueError(f"update metadata path is not a file: {catalog_path}")
    old_paths = set(old_files)
    new_paths = set(new_relative)
    removed = sorted(old_paths - new_paths)
    added = sorted(new_paths - old_paths)
    changed = sorted(
        relative
        for relative in old_paths & new_paths
        if not (destination / relative).exists() or old_files[relative] != sha256(new_relative[relative][0])
    )
    for relative in added:
        print(f"{'would add' if check else 'adding'} {destination / relative}")
    for relative in changed:
        print(f"{'would update' if check else 'updating'} {destination / relative}")
    for relative in removed:
        print(f"{'would remove' if check else 'removing'} {destination / relative}")
    if check:
        return

    with tempfile.TemporaryDirectory(prefix=".skill-sync-", dir=destination.parent) as staging_name:
        staging = Path(staging_name)
        for relative, (source_file, _) in new_relative.items():
            staged_file = staging / relative
            staged_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, staged_file)
        backups: dict[Path, bytes] = {}
        created: set[Path] = set()
        try:
            for relative in removed:
                target = destination / relative
                if target.is_file():
                    backups[target] = target.read_bytes()
                    target.unlink()
            for relative in sorted(added + changed):
                target = destination / relative
                if target.is_file():
                    backups[target] = target.read_bytes()
                else:
                    created.add(target)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(staging / relative, target)
            manifest_path.write_text(
                json.dumps(manifest_for(source, bundle, selected, targets), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            (destination / CATALOG_NAME).write_text(
                json.dumps(catalog_for(source, selected), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        except Exception:
            for target in created:
                if target.is_file() or target.is_symlink():
                    target.unlink()
            for target, content in backups.items():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            raise


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    if not source.is_dir():
        print(f"error: source repository does not exist: {source}", file=sys.stderr)
        return 2

    try:
        bundles = load_source_bundles(source)
        if args.list_bundles:
            for bundle in bundles:
                print(f"{bundle['id']}\t{bundle['scope']}\t{len(bundle['skills'])} skill(s)")
            return 0
        if args.destination is None:
            raise ValueError("destination is required unless --list-bundles is used")
        if args.bundle and args.skills:
            raise ValueError("--bundle cannot be combined with explicit skills")
        selected = resolve_bundle(source, args.bundle) if args.bundle else args.skills
        if not selected:
            raise ValueError("provide explicit skills or --bundle")
        selected = resolve_dependencies(source, selected)
        destination = args.destination.resolve()
        skills = [(relative, resolve_skill(source, relative)) for relative in selected]
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    targets = export_targets(source, destination, skills)
    if args.update:
        try:
            update_destination(source, destination, args.bundle, selected, targets, args.check)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        return 0
    if not args.update and (destination / MANIFEST_NAME).is_file():
        print("error: destination is already managed; use --update with the complete selection", file=sys.stderr)
        return 2
    conflicts = [str(target) for _, target in targets if target.exists()]
    if conflicts:
        print("error: target paths already exist; no files were changed:", file=sys.stderr)
        for target in conflicts:
            print(f"  {target}", file=sys.stderr)
        return 2

    for path, target in targets:
        relative = path.relative_to(source)
        print(f"{'would sync' if args.check else 'syncing'} {relative} -> {target}")
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            if path.is_dir():
                shutil.copytree(path, target)
            else:
                shutil.copy2(path, target)

    if not args.check:
        destination.mkdir(parents=True, exist_ok=True)
        (destination / MANIFEST_NAME).write_text(
            json.dumps(
                manifest_for(source, args.bundle, selected, targets),
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        (destination / CATALOG_NAME).write_text(
            json.dumps(catalog_for(source, selected), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
