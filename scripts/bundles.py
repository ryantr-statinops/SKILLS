#!/usr/bin/env python3
"""Load and validate the repository's bundle registry."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUNDLE_SCHEMA_VERSION = 1
BUNDLE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VALID_SCOPES = {"universal", "personal"}
VALID_RUNTIME_TARGETS = {"portable"}
BUNDLE_REQUIRED_FIELDS = {
    "id",
    "description",
    "scope",
    "runtime_target",
    "allow_deprecated",
    "skills",
}

def validate_skill_dependency_references(
    skill_records: list[dict[str, Any]],
) -> None:
    skill_ids = {record["id"] for record in skill_records}
    for record in skill_records:
        for required in record.get("requires", []):
            if required not in skill_ids:
                raise ValueError(
                    f"skill dependency is missing from registry: {record['id']}: {required}"
                )


def load_bundle_registry(path: Path | None = None) -> dict[str, Any]:
    registry_path = path or ROOT / "data/bundles.json"
    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid bundle registry: {registry_path}") from exc
    if not isinstance(data, dict):
        raise ValueError("bundle registry must be an object")
    return data


def validate_bundle_registry(
    data: dict[str, Any], skill_records: list[dict[str, str]]
) -> list[dict[str, Any]]:
    if data.get("schema_version") != BUNDLE_SCHEMA_VERSION:
        raise ValueError(
            f"unsupported bundle schema version: {data.get('schema_version')}"
        )
    bundles = data.get("bundles")
    if not isinstance(bundles, list):
        raise ValueError("bundle registry bundles must be a list")

    skills_by_id = {record["id"]: record for record in skill_records}
    seen_bundle_ids: set[str] = set()
    validated: list[dict[str, Any]] = []

    for bundle in bundles:
        if not isinstance(bundle, dict):
            raise ValueError("bundle entry must be an object")
        missing = sorted(BUNDLE_REQUIRED_FIELDS - bundle.keys())
        if missing:
            raise ValueError(
                f"bundle is missing required fields: {', '.join(missing)}"
            )

        identifier = bundle["id"]
        if not isinstance(identifier, str) or not BUNDLE_ID_RE.fullmatch(identifier):
            raise ValueError(f"invalid bundle id: {identifier}")
        if identifier in seen_bundle_ids:
            raise ValueError(f"duplicate bundle id: {identifier}")
        seen_bundle_ids.add(identifier)

        if not isinstance(bundle["description"], str) or not bundle["description"].strip():
            raise ValueError(f"invalid bundle description: {identifier}")
        if bundle["scope"] not in VALID_SCOPES:
            raise ValueError(f"invalid bundle scope: {identifier}")
        if bundle["runtime_target"] not in VALID_RUNTIME_TARGETS:
            raise ValueError(f"invalid bundle runtime target: {identifier}")
        if not isinstance(bundle["allow_deprecated"], bool):
            raise ValueError(f"invalid deprecated policy: {identifier}")

        members = bundle["skills"]
        if not isinstance(members, list) or not members:
            raise ValueError(f"bundle must contain at least one skill: {identifier}")
        if any(not isinstance(member, str) for member in members):
            raise ValueError(f"bundle skill IDs must be strings: {identifier}")
        if len(set(members)) != len(members):
            raise ValueError(f"duplicate skill in bundle: {identifier}")

        for member in members:
            record = skills_by_id.get(member)
            if record is None:
                raise ValueError(f"bundle references missing skill: {identifier}: {member}")
            if record["status"] == "deprecated" and not bundle["allow_deprecated"]:
                raise ValueError(f"bundle references deprecated skill: {identifier}: {member}")
            if bundle["scope"] == "universal" and record["scope"] == "personal":
                raise ValueError(f"universal bundle references personal skill: {identifier}: {member}")

        member_set = set(members)
        for member in members:
            record = skills_by_id[member]
            for required in record.get("requires", []):
                if required not in skills_by_id:
                    raise ValueError(
                        f"skill dependency is missing from registry: {member}: {required}"
                    )
                if required not in member_set:
                    raise ValueError(
                        f"bundle is missing skill dependency: {identifier}: {member}: {required}"
                    )

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(skill_id: str) -> None:
            if skill_id in visiting:
                raise ValueError(f"cyclic skill dependency: {identifier}: {skill_id}")
            if skill_id in visited:
                return
            visiting.add(skill_id)
            for required in skills_by_id[skill_id].get("requires", []):
                visit(required)
            visiting.remove(skill_id)
            visited.add(skill_id)

        for member in members:
            visit(member)

        validated.append(bundle)

    return validated


def load_and_validate_bundles(
    skill_records: list[dict[str, str]], path: Path | None = None
) -> list[dict[str, Any]]:
    return validate_bundle_registry(load_bundle_registry(path), skill_records)
