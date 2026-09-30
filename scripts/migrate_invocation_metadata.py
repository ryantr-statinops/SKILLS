#!/usr/bin/env python3
"""Migrate the repository's skills to the invocation metadata contract."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ("common", "personal", "meta")
VALID_INVOCATIONS = {"user", "model", "both"}

# Explicitly classify each skill: orchestration workflows and routers are
# opt-in; skills intentionally discoverable by agents or users use both.
USER_INVOCATION_IDS = {
    "common/delivery/release",
    "common/foundation/task-planning",
    "common/workflow/feature-delivery",
    "common/workflow/bug-fixing",
    "common/workflow/research-decision",
    "common/workflow/data-analysis",
    "meta/skill-authoring",
    "meta/skill-intake",
    "meta/skill-maintenance",
    "personal/education",
    "personal/engineering",
    "personal/engineering/ai",
    "personal/engineering/backend",
    "personal/engineering/data",
    "personal/engineering/frontend",
    "personal/engineering/infrastructure",
    "personal/quant",
    "personal/workflow/orca-orchestration",
}

BOTH_INVOCATION_IDS = {
    "common/agent/context-loading",
    "common/agent/failure-recovery",
    "common/data/data-cleaning",
    "common/data/data-inspection",
    "common/data/reproducible-analysis",
    "common/data/schema-validation",
    "common/delivery/change-review",
    "common/engineering/code-review",
    "common/engineering/debugging",
    "common/engineering/dependency-management",
    "common/engineering/documentation",
    "common/engineering/git-workflow",
    "common/engineering/refactoring",
    "common/engineering/testing",
    "common/foundation/context-management",
    "common/foundation/repository-onboarding",
    "common/foundation/requirements-analysis",
    "common/research/comparison",
    "common/research/research",
    "common/security/secure-development",
    "common/security/security-review",
    "meta/skill-discovery",
    "meta/skill-evaluation",
    "personal/decision/architecture-tradeoff",
    "personal/decision/scope-control",
    "personal/decision/technology-selection",
    "personal/education/latex",
    "personal/education/r",
    "personal/engineering/ai/core",
    "personal/engineering/backend/api-design",
    "personal/engineering/backend/core",
    "personal/engineering/backend/go",
    "personal/engineering/backend/nodejs",
    "personal/engineering/backend/python",
    "personal/engineering/backend/service-architecture",
    "personal/engineering/core",
    "personal/engineering/data/core",
    "personal/engineering/data/databases",
    "personal/engineering/data/orchestration",
    "personal/engineering/data/pipelines",
    "personal/engineering/frontend/lightweight-web",
    "personal/engineering/infrastructure/docker",
    "personal/engineering/infrastructure/linux",
    "personal/engineering/infrastructure/networking",
    "personal/product/architecture-review",
    "personal/product/mvp-design",
    "personal/product/project-scoping",
    "personal/quant/production-workflow",
    "personal/quant/research",
    "personal/statistics",
    "personal/workflow/brainstorming",
    "personal/workflow/personal-debugging",
    "personal/workflow/personal-research",
    "personal/workflow/project-init",
}

EXPECTED_SKILL_IDS = USER_INVOCATION_IDS | BOTH_INVOCATION_IDS


def skill_files() -> list[Path]:
    return sorted(
        path
        for category in CATEGORIES
        for path in (ROOT / category).rglob("SKILL.md")
    )


def skill_id(path: Path) -> str:
    return path.parent.relative_to(ROOT).as_posix()


def expected_invocation(identifier: str) -> str:
    if identifier in USER_INVOCATION_IDS:
        return "user"
    if identifier in BOTH_INVOCATION_IDS:
        return "both"
    raise ValueError(f"missing invocation mapping for skill: {identifier}")


def frontmatter_bounds(lines: list[str], path: Path) -> tuple[int, int]:
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return 0, index
    raise ValueError(f"unterminated YAML frontmatter: {path.relative_to(ROOT)}")


def migrate_text(text: str, identifier: str, path: Path | None = None) -> str:
    display_path = path or Path(identifier) / "SKILL.md"
    lines = text.splitlines(keepends=True)
    _, end = frontmatter_bounds(lines, display_path)
    expected = expected_invocation(identifier)
    invocation_index = None
    version_index = None

    for index in range(1, end):
        key, separator, value = lines[index].partition(":")
        if not separator:
            continue
        key = key.strip()
        if key == "invocation":
            invocation_index = index
        elif key == "version":
            version_index = index
        if key == "invocation" and value.strip() not in VALID_INVOCATIONS:
            raise ValueError(f"invalid invocation in {display_path}: {value.strip()}")

    if invocation_index is not None:
        ending = "\n" if lines[invocation_index].endswith("\n") else ""
        lines[invocation_index] = f"invocation: {expected}{ending}"
    else:
        if version_index is None:
            raise ValueError(f"missing version before invocation in {display_path}")
        ending = "\n" if lines[version_index].endswith("\n") else "\n"
        lines.insert(version_index + 1, f"invocation: {expected}{ending}")

    return "".join(lines)


def check_or_apply(apply: bool) -> int:
    paths = skill_files()
    identifiers = {skill_id(path) for path in paths}
    if identifiers != EXPECTED_SKILL_IDS:
        unknown = sorted(identifiers - EXPECTED_SKILL_IDS)
        missing = sorted(EXPECTED_SKILL_IDS - identifiers)
        print(
            f"error: invocation mapping does not match the skill inventory "
            f"(unknown={unknown}, missing={missing})",
            file=sys.stderr,
        )
        return 1

    failures = 0
    changes = 0
    for path in paths:
        identifier = skill_id(path)
        try:
            current = path.read_text(encoding="utf-8")
            migrated = migrate_text(current, identifier, path)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            failures += 1
            continue

        if current != migrated:
            changes += 1
            if apply:
                path.write_text(migrated, encoding="utf-8")
                print(f"updated {path.relative_to(ROOT)}")
            else:
                print(f"needs update: {path.relative_to(ROOT)}")

    if failures:
        return 1
    if not apply and changes:
        print(f"{changes} skill(s) need invocation metadata migration.")
        return 1
    print(f"Invocation metadata is consistent for {len(paths)} skill(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="check without writing")
    mode.add_argument("--apply", action="store_true", help="apply the migration")
    args = parser.parse_args()
    return check_or_apply(args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
