#!/usr/bin/env python3
"""Check representative and boundary workflow cases using observable text."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/observable-agent-evaluations.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "text"), default="text")
    return parser.parse_args()


def evaluate_cases(cases: list[dict[str, object]]) -> list[dict[str, object]]:
    results = []
    seen_pairs: set[tuple[str, str]] = set()
    for case in cases:
        workflow = case["workflow"]
        case_type = case["case"]
        pair = (workflow, case_type)
        duplicate = pair in seen_pairs
        seen_pairs.add(pair)
        evaluation = ROOT / workflow / "examples/evaluation.md"
        text = evaluation.read_text(encoding="utf-8")
        heading = "## Representative task" if case_type == "representative" else "## Boundary task"
        section = text.split(heading, 1)[1].split("\n## ", 1)[0]
        missing = [term for term in case["required_terms"] if term.lower() not in section.lower()]
        if duplicate:
            missing.append("duplicate workflow/case pair")
        results.append({"name": case["name"], "workflow": workflow, "case": case_type, "status": "passed" if not missing else "failed", "missing": missing})
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
