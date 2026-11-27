#!/usr/bin/env python3
"""Direct installer for agent skills into target runtimes (.agents/skills).

Supports:
  1. --global: symlink skills into user-level ~/.agents/skills/ (or custom --target)
  2. --project: copy skills directly into <project>/.agents/skills/<hyphenated-name>
  3. --bundle: resolve and install a named bundle from data/bundles.json
  4. --check: preview actions without modifying files
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
BUNDLES_PATH = ROOT / "data/bundles.json"


def load_bundles() -> dict[str, list[str]]:
    if not BUNDLES_PATH.is_file():
        return {}
    with open(BUNDLES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {bundle["id"]: bundle["skills"] for bundle in data.get("bundles", [])}


def skill_id_to_adapter_name(skill_id: str) -> str:
    """Convert path-like ID (e.g. common/engineering/debugging) to hyphenated adapter name."""
    return skill_id.replace("/", "-")


def resolve_skills(selected: list[str], bundle_name: str | None) -> list[tuple[str, Path]]:
    """Return list of (adapter_name, source_skill_dir)."""
    skill_ids: set[str] = set()
    bundles = load_bundles()

    if bundle_name:
        if bundle_name not in bundles:
            raise ValueError(f"Unknown bundle: {bundle_name}. Available: {', '.join(sorted(bundles.keys()))}")
        skill_ids.update(bundles[bundle_name])

    for item in selected:
        if item in bundles:
            skill_ids.update(bundles[item])
        else:
            skill_ids.add(item)

    results: list[tuple[str, Path]] = []
    for sid in sorted(skill_ids):
        source_dir = ROOT / sid
        if not (source_dir / "SKILL.md").is_file():
            raise ValueError(f"Skill entrypoint not found: {source_dir / 'SKILL.md'}")
        results.append((skill_id_to_adapter_name(sid), source_dir))
    return results


def install_global(
    skills: list[tuple[str, Path]], target_dir: Path, check: bool = False
) -> list[str]:
    actions = []
    for adapter_name, source_dir in skills:
        dest_link = target_dir / adapter_name
        rel_target = os.path.relpath(source_dir, target_dir)
        if dest_link.is_symlink():
            current_target = os.readlink(dest_link)
            if current_target == rel_target:
                continue
            actions.append(f"relink {dest_link} -> {rel_target}")
            if not check:
                dest_link.unlink()
                dest_link.symlink_to(rel_target)
        elif dest_link.exists():
            actions.append(f"skip existing non-symlink: {dest_link}")
        else:
            actions.append(f"link {dest_link} -> {rel_target}")
            if not check:
                target_dir.mkdir(parents=True, exist_ok=True)
                dest_link.symlink_to(rel_target)
    return actions


def install_project(
    skills: list[tuple[str, Path]], target_dir: Path, check: bool = False
) -> list[str]:
    actions = []
    for adapter_name, source_dir in skills:
        dest_dir = target_dir / adapter_name
        if dest_dir.exists():
            actions.append(f"update {dest_dir}")
            if not check:
                shutil.rmtree(dest_dir)
                shutil.copytree(source_dir, dest_dir)
        else:
            actions.append(f"copy {source_dir} -> {dest_dir}")
            if not check:
                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.copytree(source_dir, dest_dir)
    return actions


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*", help="Skill IDs or bundle names")
    parser.add_argument("--bundle", "-b", help="Named bundle to install")
    parser.add_argument(
        "--global",
        dest="is_global",
        action="store_true",
        help="Install as symlinks into user-level skills directory (default: ~/.agents/skills)",
    )
    parser.add_argument(
        "--project",
        type=Path,
        help="Project directory to install into (copies into <project>/.agents/skills)",
    )
    parser.add_argument(
        "--target",
        type=Path,
        help="Custom destination directory override",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Preview changes without writing",
    )
    parser.add_argument(
        "--list-bundles",
        action="store_true",
        help="List available bundles and exit",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.list_bundles:
        bundles = load_bundles()
        for name, skills in sorted(bundles.items()):
            print(f"{name} ({len(skills)} skills):")
            for sid in skills:
                print(f"  - {sid}")
        return 0

    if not args.skills and not args.bundle:
        print("error: specify at least one skill or --bundle", file=sys.stderr)
        return 2

    try:
        resolved = resolve_skills(args.skills, args.bundle)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.target:
        dest = args.target
    elif args.is_global:
        dest = Path.home() / ".agents/skills"
    elif args.project:
        dest = args.project / ".agents/skills"
    else:
        print("error: specify --global, --project <dir>, or --target <dir>", file=sys.stderr)
        return 2

    if args.is_global:
        actions = install_global(resolved, dest, check=args.check)
    else:
        actions = install_project(resolved, dest, check=args.check)

    prefix = "[check] " if args.check else ""
    for action in actions:
        print(f"{prefix}{action}")
    if not actions:
        print(f"{prefix}all {len(resolved)} skills are up to date in {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
