#!/usr/bin/env python3
"""Expose an installed portable skill tree through a native runtime layout."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="portable .agent/skills directory")
    parser.add_argument("destination", type=Path, help="native .agents/skills directory")
    parser.add_argument("--check", action="store_true", help="report changes without writing")
    return parser.parse_args()


def adapter_entries(source: Path, destination: Path) -> list[tuple[Path, Path]]:
    if not source.is_dir():
        raise ValueError(f"portable skill directory does not exist: {source}")
    entries: list[tuple[Path, Path]] = []
    names: dict[str, Path] = {}
    for entrypoint in sorted(source.rglob("SKILL.md")):
        relative_dir = entrypoint.parent.relative_to(source)
        if not relative_dir.parts:
            raise ValueError(f"skill entrypoint must be nested below source: {entrypoint}")
        name = "-".join(relative_dir.parts)
        previous = names.setdefault(name, relative_dir)
        if previous != relative_dir:
            raise ValueError(f"adapter name collision for {name}: {previous} and {relative_dir}")
        entries.append((source / relative_dir, destination / name))
    if not entries:
        raise ValueError(f"no SKILL.md files found below {source}")
    return entries


def check_entries(entries: list[tuple[Path, Path]]) -> list[tuple[Path, Path]]:
    changes: list[tuple[Path, Path]] = []
    for source_dir, target in entries:
        expected = os.path.relpath(source_dir, target.parent)
        if target.is_symlink() and os.readlink(target) == expected:
            continue
        if target.exists() or target.is_symlink():
            raise ValueError(f"adapter target already exists with different content: {target}")
        changes.append((source_dir, target))
    return changes


def main() -> int:
    args = parse_args()
    entries = adapter_entries(args.source.resolve(), args.destination.resolve())
    changes = check_entries(entries)
    if args.check:
        for source_dir, target in changes:
            expected = os.path.relpath(source_dir, target.parent)
            print(f"add {target} -> {expected}")
        return 0
    args.destination.mkdir(parents=True, exist_ok=True)
    for source_dir, target in changes:
        target.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(os.path.relpath(source_dir, target.parent), target)
        print(f"created {target}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        raise SystemExit(f"error: {exc}")
