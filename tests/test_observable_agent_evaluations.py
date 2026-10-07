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

if __name__ == "__main__":
    unittest.main()
