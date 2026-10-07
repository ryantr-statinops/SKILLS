#!/usr/bin/env python3
"""Check representative and boundary workflow cases using observable text."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/observable-agent-evaluations.json"
WORKFLOWS = (
    "common/workflow/bug-fixing",
    "common/workflow/data-analysis",
    "common/workflow/feature-delivery",
    "common/workflow/research-decision",
)
CASE_TYPES = ("representative", "boundary")
REQUIRED_CASE_PAIRS = {(workflow, case_type) for workflow in WORKFLOWS for case_type in CASE_TYPES}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "text"), default="text")
    return parser.parse_args()


def evaluate_cases(cases: list[dict[str, object]]) -> list[dict[str, object]]:
    results = []
    seen_pairs: set[tuple[str, str]] = set()
    for case in cases:
        if not isinstance(case, dict):
            results.append({"name": "invalid case", "workflow": None, "case": None, "status": "failed", "missing": ["case must be an object"]})
            continue
        workflow = case.get("workflow")
        case_type = case.get("case")
        name = case.get("name", "unnamed case")
        if workflow not in WORKFLOWS:
            results.append({"name": name, "workflow": workflow, "case": case_type, "status": "failed", "missing": ["unknown workflow"]})
            continue
        if case_type not in CASE_TYPES:
            results.append({"name": name, "workflow": workflow, "case": case_type, "status": "failed", "missing": ["invalid case type"]})
            continue
        pair = (workflow, case_type)
        duplicate = pair in seen_pairs
        seen_pairs.add(pair)
        required_terms = case.get("required_terms")
        if not isinstance(required_terms, list) or not required_terms or any(
            not isinstance(term, str) or not term.strip() for term in required_terms
        ):
            missing = ["required_terms must contain nonempty strings"]
            if duplicate:
                missing.append("duplicate workflow/case pair")
            results.append({"name": name, "workflow": workflow, "case": case_type, "status": "failed", "missing": missing})
            continue
        evaluation = ROOT / workflow / "examples/evaluation.md"
        text = evaluation.read_text(encoding="utf-8")
        heading = "## Representative task" if case_type == "representative" else "## Boundary task"
        section = text.split(heading, 1)[1].split("\n## ", 1)[0]
        missing = [term for term in required_terms if term.lower() not in section.lower()]
        if duplicate:
            missing.append("duplicate workflow/case pair")
        results.append({"name": name, "workflow": workflow, "case": case_type, "status": "passed" if not missing else "failed", "missing": missing})
    for workflow, case_type in sorted(REQUIRED_CASE_PAIRS - seen_pairs):
        results.append({
            "name": f"missing {workflow} {case_type}",
            "workflow": workflow,
            "case": case_type,
            "status": "failed",
            "missing": ["required workflow/case pair is missing"],
        })
    return results


def evaluate() -> list[dict[str, object]]:
    cases = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return evaluate_cases(cases)


def main() -> int:
    args = parse_args()
    results = evaluate()
    if args.format == "json":
        print(json.dumps({"total": len(results), "failed": sum(item["status"] == "failed" for item in results), "cases": results}, indent=2))
    else:
        for item in results:
            print(f"{item['status']}: {item['name']}")
    return 1 if any(item["status"] == "failed" for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
