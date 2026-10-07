"""Deterministic checks for representative and boundary agent cases."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from check_observable_evaluations import evaluate_cases  # noqa: E402


class ObservableAgentEvaluationTests(unittest.TestCase):
    def test_all_workflow_cases_have_observable_contracts(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/check_observable_evaluations.py", "--format", "json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["total"], 8)
        self.assertEqual(report["failed"], 0)


    def test_duplicate_workflow_case_pair_fails(self) -> None:
        cases = json.loads((ROOT / "tests/fixtures/observable-agent-evaluations.json").read_text(encoding="utf-8"))
        duplicate = dict(cases[0], name="duplicate representative")
        results = evaluate_cases([*cases, duplicate])
        repeated = results[-1]
        self.assertEqual(repeated["status"], "failed")
        self.assertIn("duplicate workflow/case pair", repeated["missing"])

    def test_missing_pairs_and_invalid_case_types_fail(self) -> None:
        fixture = ROOT / "tests/fixtures/observable-agent-evaluations.json"
        cases = json.loads(fixture.read_text(encoding="utf-8"))
        missing_pair = ("common/workflow/data-analysis", "boundary")
        reduced = [
            case for case in cases
            if (case["workflow"], case["case"]) != missing_pair
        ]
        missing_results = evaluate_cases(reduced)
        missing = next(item for item in missing_results if (item["workflow"], item["case"]) == missing_pair)
        self.assertEqual(missing["status"], "failed")
        self.assertIn("required workflow/case pair is missing", missing["missing"])

        invalid = [dict(cases[0], case="borderline"), *cases[1:]]
        invalid_results = evaluate_cases(invalid)
        self.assertEqual(invalid_results[0]["status"], "failed")
        self.assertIn("invalid case type", invalid_results[0]["missing"])

    def test_empty_or_invalid_required_terms_fail(self) -> None:
        cases = json.loads((ROOT / "tests/fixtures/observable-agent-evaluations.json").read_text(encoding="utf-8"))
        for required_terms in ([], [" "] , [None]):
            with self.subTest(required_terms=required_terms):
                invalid = [dict(cases[0], required_terms=required_terms), *cases[1:]]
                result = evaluate_cases(invalid)[0]
                self.assertEqual(result["status"], "failed")
                self.assertIn("required_terms must contain nonempty strings", result["missing"])

if __name__ == "__main__":
    unittest.main()
