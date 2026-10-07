#!/usr/bin/env python3
"""Check skill evaluation contracts and emit a JSON or Markdown report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ("common", "personal")
CASE_SECTIONS = ("## Representative task", "## Boundary task")
CASE_FIELDS = ("Task:", "Expected:", "Failure condition:", "Validation:")
CONFIRMATIONS = {"never", "before_mutation", "before_external"}

# Validation commands are opt-in and exact-match only. New commands must be
# reviewed here before an evaluation file can request their execution.
ALLOWED_COMMANDS = {
    "python3 scripts/validate_skills.py": [sys.executable, "scripts/validate_skills.py"],
    "python3 scripts/generate_skill_index.py --check": [
        sys.executable,
        "scripts/generate_skill_index.py",
        "--check",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="report format printed to stdout (default: markdown)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="optional report file; otherwise the report is printed to stdout",
    )
    parser.add_argument(
        "--run-commands",
        action="store_true",
        help="run exact allowlisted validation commands declared in cases",
    )
    return parser.parse_args()


def case_body(text: str, heading: str) -> str:
    marker = f"{heading}\n"
    if marker not in text:
        return ""
    body = text.split(marker, 1)[1]
    next_heading = body.find("\n## ")
    return body if next_heading == -1 else body[:next_heading]


def declared_commands(text: str) -> list[str]:
    commands = []
    for line in text.splitlines():
        if line.startswith("Validation command:"):
            commands.append(line.split(":", 1)[1].strip())
    return commands


def field_has_value(body: str, field: str) -> bool:
    lines = body.splitlines()
    field_names = set(CASE_FIELDS)
    for index, line in enumerate(lines):
        value = line.strip()
        if not value.startswith(field):
            continue
        if value[len(field):].strip():
            return True
        for continuation in lines[index + 1:]:
            continuation = continuation.strip()
            if not continuation or any(continuation.startswith(name) for name in field_names):
                break
            return True
    return False


def check_case(text: str, heading: str) -> list[str]:
    body = case_body(text, heading)
    errors = []
    if not body:
        errors.append(f"missing {heading}")
        return errors
    for field in CASE_FIELDS:
        if not field_has_value(body, field):
            state = "empty" if any(line.strip().startswith(field) for line in body.splitlines()) else "missing"
            errors.append(f"{state} {field} in {heading}")
    return errors


def registry_records() -> dict[str, dict[str, str]]:
    registry_path = ROOT / "data/skills.json"
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        records = registry["skills"]
        return {record["id"]: record for record in records}
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid generated registry: {registry_path.relative_to(ROOT)}") from exc


def evaluation_skill_files() -> list[Path]:
    paths = {
        skill_file
        for category in CATEGORIES
        for skill_file in (ROOT / category).rglob("SKILL.md")
    }
    promotion_path = ROOT / "data/promoted.json"
    try:
        promoted = json.loads(promotion_path.read_text(encoding="utf-8"))["skills"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid promotion registry: {promotion_path.relative_to(ROOT)}") from exc
    for identifier in promoted:
        if isinstance(identifier, str) and identifier.startswith("meta/"):
            paths.add(ROOT / identifier / "SKILL.md")
    return sorted(paths)


def evaluate_routing(records: dict[str, dict[str, str]]) -> tuple[list[dict[str, object]], int]:
    fixture_path = ROOT / "tests/fixtures/agent-routing.json"
    try:
        fixtures = json.loads(fixture_path.read_text(encoding="utf-8"))
        if not isinstance(fixtures, list):
            raise TypeError("fixture is not a list")
    except (OSError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid routing fixture: {fixture_path.relative_to(ROOT)}") from exc

    results = []
    failures = 0
    for index, fixture in enumerate(fixtures):
        errors = []
        required = ("task", "expected_skill", "boundary_skill", "expected_explanation", "confirmation", "expected_validation")
        if not isinstance(fixture, dict):
            errors.append("fixture case is not an object")
            fixture = {}
        for field in required:
            if field not in fixture:
                errors.append(f"missing {field}")
        expected = fixture.get("expected_skill")
        boundary = fixture.get("boundary_skill")
        confirmation = fixture.get("confirmation")
        if expected not in records:
            errors.append(f"expected skill is absent from registry: {expected}")
        elif records[expected]["status"] == "deprecated":
            errors.append(f"expected skill is deprecated: {expected}")
        if boundary is not None and boundary not in records:
            errors.append(f"boundary skill is absent from registry: {boundary}")
        if confirmation not in CONFIRMATIONS:
            errors.append(f"invalid confirmation: {confirmation}")
        if fixture.get("expected_explanation") is not True:
            errors.append("expected_explanation must be true")
        if fixture.get("expected_validation") is not True:
            errors.append("expected_validation must be true")
        result = {
            "case": index + 1,
            "task": fixture.get("task", ""),
            "expected_skill": expected,
            "boundary_skill": boundary,
            "confirmation": confirmation,
            "status": "passed" if not errors else "failed",
            "errors": errors,
        }
        results.append(result)
        failures += bool(errors)
    return results, failures


def evaluate(run_commands: bool) -> tuple[list[dict[str, object]], list[dict[str, object]], int]:
    records = registry_records()
    ids = set(records)
    results: list[dict[str, object]] = []
    failures = 0
    try:
        skill_files = evaluation_skill_files()
    except ValueError as exc:
        raise ValueError(str(exc)) from exc
    for skill_file in skill_files:
        skill_dir = skill_file.parent
        skill_id = skill_dir.relative_to(ROOT).as_posix()
        evaluation = skill_dir / "examples/evaluation.md"
        errors: list[str] = []
        commands: list[dict[str, str]] = []
        if skill_id not in ids:
            errors.append("skill id is absent from generated registry")
        if not evaluation.is_file():
            errors.append("missing examples/evaluation.md")
        else:
            text = evaluation.read_text(encoding="utf-8")
            for heading in CASE_SECTIONS:
                errors.extend(check_case(text, heading))
            for command in declared_commands(text):
                if command not in ALLOWED_COMMANDS:
                    errors.append(f"command is not allowlisted: {command}")
                    commands.append({"command": command, "status": "rejected"})
                elif not run_commands:
                    commands.append({"command": command, "status": "skipped"})
                else:
                    completed = subprocess.run(
                        ALLOWED_COMMANDS[command],
                        cwd=ROOT,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    status = "passed" if completed.returncode == 0 else "failed"
                    commands.append({"command": command, "status": status})
                    if completed.returncode != 0:
                        errors.append(f"allowlisted command failed: {command}")
        result = {
            "id": skill_id,
            "path": evaluation.relative_to(ROOT).as_posix(),
            "status": "passed" if not errors else "failed",
            "errors": errors,
            "commands": commands,
        }
        results.append(result)
        failures += bool(errors)
    routing_results, routing_failures = evaluate_routing(records)
    return results, routing_results, failures + routing_failures


def render_json(results: list[dict[str, object]], routing: list[dict[str, object]]) -> str:
    failed = sum(r["status"] == "failed" for r in results) + sum(
        r["status"] == "failed" for r in routing
    )
    return json.dumps(
        {
            "schema_version": 2,
            "total": len(results),
            "failed": failed,
            "skills": results,
            "routing_total": len(routing),
            "routing_failed": sum(r["status"] == "failed" for r in routing),
            "routing": routing,
        },
        indent=2,
        ensure_ascii=False,
    ) + "\n"


def render_markdown(results: list[dict[str, object]], routing: list[dict[str, object]]) -> str:
    failed = sum(result["status"] == "failed" for result in results) + sum(
        result["status"] == "failed" for result in routing
    )
    lines = [
        "# Skill evaluation report",
        "",
        "> Generated by `scripts/run_evaluations.py`; the harness checks contracts and registry references.",
        "",
        f"Total skills: **{len(results)}**",
        f"Failed skills: **{failed}**",
        "",
        "| Skill | Evaluation file | Status | Errors |",
        "| --- | --- | --- | --- |",
    ]
    for result in results:
        errors = "; ".join(result["errors"]) or "—"
        lines.append(
            f"| `{result['id']}` | `{result['path']}` | `{result['status']}` | {errors} |"
        )
    lines.extend(["", "## Agent routing fixtures", "", "| Case | Expected skill | Status | Errors |", "| ---: | --- | --- | --- |"])
    for result in routing:
        errors = "; ".join(result["errors"]) or "—"
        lines.append(
            f"| {result['case']} | `{result['expected_skill']}` | `{result['status']}` | {errors} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    try:
        results, routing, failures = evaluate(args.run_commands)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    report = render_json(results, routing) if args.format == "json" else render_markdown(results, routing)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
