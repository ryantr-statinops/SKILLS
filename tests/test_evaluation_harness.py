#!/usr/bin/env python3
"""Regression tests for the deterministic evaluation harness."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from run_evaluations import CASE_FIELDS, CASE_SECTIONS, check_case  # noqa: E402


class EvaluationHarnessTests(unittest.TestCase):
    def test_repository_evaluation_report_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "run_evaluations.py"), "--format", "json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["failed"], 0)
        self.assertEqual(report["routing_failed"], 0)

    def test_case_requires_both_sections_and_all_fields(self) -> None:
        text = "## Representative task\nTask: one\nExpected: two\n"
        errors = []
        for section in CASE_SECTIONS:
            errors.extend(check_case(text, section))
        self.assertIn("missing ## Boundary task", errors)
        self.assertIn("missing Failure condition: in ## Representative task", errors)
        self.assertIn("missing Validation: in ## Representative task", errors)

    def test_contract_field_list_is_explicit(self) -> None:
        self.assertEqual(
            CASE_FIELDS,
            ("Task:", "Expected:", "Failure condition:", "Validation:"),
        )


if __name__ == "__main__":
    unittest.main()
