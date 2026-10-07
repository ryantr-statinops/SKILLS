#!/usr/bin/env python3
"""Find candidate skills from the generated machine-readable registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

from bundles import load_and_validate_bundles
from generate_skill_index import collect

ROOT = Path(__file__).resolve().parents[1]
TOKEN_RE = re.compile(r"[a-z0-9]+")
VALID_INVOCATIONS = {"user", "model", "both"}
REQUIRED_RECORD_FIELDS = ("id", "name", "description", "category", "subject", "scope", "status", "version", "path")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="outcome or keywords to match")
    parser.add_argument("--category", choices=("common", "personal", "meta"))
    parser.add_argument("--scope", choices=("universal", "personal", "repository"))
    parser.add_argument(
        "--status",
        choices=("draft", "experimental", "stable", "deprecated"),
    )
    parser.add_argument("--invocation", choices=tuple(sorted(VALID_INVOCATIONS)))
    parser.add_argument("--bundle", help="restrict results to a named bundle")
    parser.add_argument("--registry", type=Path, help="use an installed skill catalog")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def normalize_registry(data: dict[str, object]) -> list[dict[str, str]]:
    if not isinstance(data, dict):
        raise ValueError("registry must be an object")
    schema_version = data.get("schema_version")
    if schema_version not in {1, 2, 3}:
        raise ValueError(f"unsupported registry schema version: {schema_version}")
    skills = data.get("skills")
    if not isinstance(skills, list):
        raise ValueError("skills must be a list")
    normalized = []
    for record in skills:
        if not isinstance(record, dict):
            raise ValueError("skill record must be an object")
        item = dict(record)
        for field in REQUIRED_RECORD_FIELDS:
            if not isinstance(item.get(field), str) or not item[field]:
                raise ValueError(f"invalid {field} in skill record")
        if schema_version == 1:
            item["invocation"] = "both"
        elif item.get("invocation") not in VALID_INVOCATIONS:
            raise ValueError("invalid invocation in registry")
        if "requires" not in item:
            item["requires"] = []
        if not isinstance(item["requires"], list) or any(
            not isinstance(value, str) for value in item["requires"]
        ):
            raise ValueError("invalid requires in registry")
        normalized.append(item)
    return normalized


def load_registry(path: Path | None = None) -> list[dict[str, str]]:
    path = path or ROOT / "data/skills.json"
    try:
        return normalize_registry(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        try:
            display_path = path.relative_to(ROOT)
        except ValueError:
            display_path = path
        raise ValueError(f"invalid registry {display_path}: {exc}") from exc


def load_bundle_map() -> dict[str, set[str]]:
    bundles = load_and_validate_bundles(collect())
    return {bundle["id"]: set(bundle["skills"]) for bundle in bundles}


def tokens(value: str) -> set[str]:
    return set(TOKEN_RE.findall(value.lower()))


def score(record: dict[str, str], query_tokens: set[str]) -> int:
    if not query_tokens:
        return 0
    name_tokens = tokens(record["name"])
    subject_tokens = tokens(record["subject"])
    category_tokens = tokens(record["category"])
    scope_tokens = tokens(record["scope"])
    description_tokens = tokens(record["description"])
    searchable = name_tokens | subject_tokens | category_tokens | scope_tokens | description_tokens
    matched = query_tokens & searchable
    if not matched:
        return -1
    value = len(matched) * 10
    value += len(query_tokens & name_tokens) * 45
    value += len(query_tokens & subject_tokens) * 30
    value += len(query_tokens & category_tokens) * 20
    value += len(query_tokens & scope_tokens) * 15
    value += len(query_tokens & description_tokens) * 5
    if query_tokens <= name_tokens:
        value += 100
    return value


def discover(args: argparse.Namespace) -> list[dict[str, object]]:
    query_tokens = tokens(" ".join(args.query))
    bundle_members = None
    if args.bundle:
        bundle_members = load_bundle_map().get(args.bundle)
        if bundle_members is None:
            raise ValueError(f"unknown bundle: {args.bundle}")
    candidates = []
    registry_path = getattr(args, "registry", None)
    for record in load_registry(registry_path):
        if bundle_members is not None and record["id"] not in bundle_members:
            continue
        if args.category and record["category"] != args.category:
            continue
        if args.scope and record["scope"] != args.scope:
            continue
        if args.status and record["status"] != args.status:
            continue
        if args.invocation and record["invocation"] != args.invocation:
            continue
        ranking = score(record, query_tokens)
        if query_tokens and ranking < 0:
            continue
        candidates.append({**record, "score": ranking})
    candidates.sort(key=lambda item: (-item["score"], item["category"], item["subject"], item["name"]))
    return candidates[: max(args.limit, 0)]


def render_markdown(
    candidates: list[dict[str, object]], query: str, bundle: str | None = None
) -> str:
    lines = [
        "# Skill candidates",
        "",
        f"Query: `{query or '(all)'}`",
        f"Bundle: `{bundle or '(all)'}`",
        "",
        "| ID | Description | Scope | Status | Invocation | Score |",
        "| --- | --- | --- | --- | --- | ---: |",
    ]
    for item in candidates:
        description = str(item["description"]).replace("|", "\\|")
        lines.append(
            f"| `{item['id']}` | {description} | `{item['scope']}` | `{item['status']}` | `{item['invocation']}` | {item['score']} |"
        )
    if not candidates:
        lines.append("| — | No matching skills. | — | — | — |")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    if args.limit < 0:
        print("error: --limit must be non-negative", file=sys.stderr)
        return 2
    try:
        candidates = discover(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.format == "json":
        print(
            json.dumps(
                {
                    "query": " ".join(args.query),
                    "bundle": args.bundle,
                    "skills": candidates,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(render_markdown(candidates, " ".join(args.query), args.bundle), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
