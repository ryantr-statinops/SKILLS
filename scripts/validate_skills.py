#!/usr/bin/env python3
"""Validate the repository's skill layout without external dependencies."""

from pathlib import Path
import json
import re
import sys

from generate_skill_index import (
    ENUMS,
    REQUIRED,
    VERSION_RE,
    REGISTRY_SCHEMA_VERSION,
    collect,
    render_json,
    render_markdown,
)
from bundles import load_and_validate_bundles
from promotions import load_and_validate_promotions

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {"common", "personal", "meta"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACEHOLDERS = ("skill-name", "Describe what this skill", "Use this skill when ...")
HANDOFF_FIELDS = (
    "Selected when:",
    "Do not activate when:",
    "Expected output:",
    "User-facing report:",
    "Confirmation boundary:",
)
MODEL_ACTIVATION_FIELDS = (
    "## When to use",
    "## Do not activate when",
    "## Expected output",
    "## Validation",
    "## Agent handoff",
)


def activation_contract_errors(text: str, invocation: str) -> list[str]:
    """Return missing activation-boundary sections for model-invoked skills."""
    if invocation != "model":
        return []
    return [
        f"missing model activation contract section: {section}"
        for section in MODEL_ACTIVATION_FIELDS
        if section not in text
    ]


def handoff_contract_errors(text: str) -> list[str]:
    marker = "## Agent handoff\n"
    if marker not in text:
        return ["missing agent handoff section"]
    body = text.split(marker, 1)[1]
    next_heading = body.find("\n## ")
    if next_heading != -1:
        body = body[:next_heading]
    lines = body.splitlines()
    errors = []
    for field in HANDOFF_FIELDS:
        value = None
        for index, line in enumerate(lines):
            candidate = line.strip()
            if candidate.startswith("- "):
                candidate = candidate[2:].strip()
            if not candidate.startswith(field):
                continue
            value = candidate[len(field):].strip()
            if not value:
                for continuation in lines[index + 1:]:
                    continuation = continuation.strip()
                    if continuation.startswith("- "):
                        continuation = continuation[2:].strip()
                    if not continuation or any(continuation.startswith(name) for name in HANDOFF_FIELDS):
                        break
                    value = continuation
                    break
            break
        if value is None:
            errors.append(f"missing agent handoff field: {field}")
        elif not value:
            errors.append(f"empty agent handoff field: {field}")
    return errors


def error(message: str) -> None:
    print(f"ERROR: {message}")


def validate_skill(path: Path) -> int:
    failures = 0
    relative = path.relative_to(ROOT)
    category = relative.parts[0]
    skill_file = path / "SKILL.md"
    if not NAME_RE.fullmatch(path.name):
        error(f"invalid skill directory name: {path.relative_to(ROOT)}")
        failures += 1
    if not skill_file.is_file():
        error(f"missing SKILL.md: {path.relative_to(ROOT)}")
        return failures + 1

    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        error(f"missing YAML frontmatter: {skill_file.relative_to(ROOT)}")
        failures += 1
    else:
        frontmatter = text[4 : text.index("\n---\n", 4)]
        for field in REQUIRED:
            if not re.search(rf"^\s*{re.escape(field)}\s*.+$", frontmatter, re.MULTILINE):
                error(f"missing {field[:-1]} in {skill_file.relative_to(ROOT)}")
                failures += 1
        values = {}
        for line in frontmatter.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                values[key.strip()] = value.strip().strip('"\'')
        if values.get("name") != path.name:
            error(f"name does not match directory in {skill_file.relative_to(ROOT)}")
            failures += 1
        if values.get("category") != category:
            error(f"category does not match path in {skill_file.relative_to(ROOT)}")
            failures += 1
        for field, allowed in ENUMS.items():
            if values.get(field) not in allowed:
                error(f"invalid {field} in {skill_file.relative_to(ROOT)}")
                failures += 1
        if values.get("version") and not VERSION_RE.fullmatch(values["version"]):
            error(f"invalid version in {skill_file.relative_to(ROOT)}")

        for message in activation_contract_errors(text, values.get("invocation", "")):
            error(f"{message} in {skill_file.relative_to(ROOT)}")
            failures += 1

    for placeholder in PLACEHOLDERS:
        if placeholder in text:
            error(f"unfinished placeholder in {skill_file.relative_to(ROOT)}: {placeholder}")
            failures += 1

    for message in handoff_contract_errors(text):
        error(f"{message} in {skill_file.relative_to(ROOT)}")
        failures += 1

    for directory in path.iterdir():
        if directory.is_dir() and not any(directory.iterdir()):
            error(f"empty resource directory: {directory.relative_to(ROOT)}")
            failures += 1

    if category in {"common", "personal"}:
        evaluation = path / "examples/evaluation.md"
        if not evaluation.is_file():
            error(f"missing skill evaluation: {evaluation.relative_to(ROOT)}")
            failures += 1
        else:
            evaluation_text = evaluation.read_text(encoding="utf-8")
            for section in (
                "## Representative task",
                "## Boundary task",
                "Task:",
                "Expected:",
                "Failure condition:",
                "Validation:",
            ):
                if section not in evaluation_text:
                    error(f"missing evaluation section in {evaluation.relative_to(ROOT)}: {section}")
                    failures += 1

    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).split("#", 1)[0]
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (skill_file.parent / target).resolve()
        if not resolved.exists():
            error(f"broken link in {skill_file.relative_to(ROOT)}: {target}")
            failures += 1
    return failures


def main() -> int:
    failures = 0
    for category in CATEGORIES:
        category_path = ROOT / category
        if not category_path.is_dir():
            error(f"missing category directory: {category}")
            failures += 1
            continue
        for skill_file in sorted(category_path.rglob("SKILL.md")):
            failures += validate_skill(skill_file.parent)
    try:
        records = collect()
        bundles = load_and_validate_bundles(records)
        load_and_validate_promotions(records, bundles)
        generated = {
            ROOT / "docs/skill-index.md": render_markdown(records),
            ROOT / "data/skills.json": render_json(records),
        }
        registry = json.loads((ROOT / "data/skills.json").read_text(encoding="utf-8"))
        if registry.get("schema_version") != REGISTRY_SCHEMA_VERSION:
            error(
                f"invalid registry schema version: expected {REGISTRY_SCHEMA_VERSION}"
            )
            failures += 1
        for path, expected in generated.items():
            if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                error(f"stale or missing generated file: {path.relative_to(ROOT)}")
                failures += 1
    except ValueError as exc:
        error(str(exc))
        failures += 1
    if failures:
        print(f"Validation failed with {failures} issue(s).")
        return 1
    print("All skills passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
