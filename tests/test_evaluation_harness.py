#!/usr/bin/env python3
"""Regression tests for the deterministic evaluation harness."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from run_evaluations import CASE_FIELDS, CASE_SECTIONS, check_case, evaluate_routing  # noqa: E402


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

    def test_case_rejects_empty_values_and_accepts_continuations(self) -> None:
        empty = (
            "## Representative task\nTask:\n\nExpected:\n\n"
            "Failure condition:\n\nValidation:\n"
        )
        errors = check_case(empty, CASE_SECTIONS[0])
        for field in CASE_FIELDS:
            self.assertIn(f"empty {field} in {CASE_SECTIONS[0]}", errors)

        multiline = (
            "## Representative task\nTask:\n  Add a retry limit.\n"
            "Expected: retries stop at the configured limit.\n"
            "Failure condition: another retry occurs.\n"
            "Validation: assert the call count.\n"
        )
        self.assertEqual(check_case(multiline, CASE_SECTIONS[0]), [])

    def test_fields_in_representative_case_do_not_satisfy_boundary_case(self) -> None:
        text = (
            "## Representative task\n"
            "Task: a representative request\n"
            "Expected: observable result\n"
            "Failure condition: unsafe result\n"
            "Validation: inspect the artifact\n\n"
            "## Boundary task\nTask: nearby excluded request\n"
        )
        errors = check_case(text, CASE_SECTIONS[1])
        self.assertIn("missing Expected: in ## Boundary task", errors)
        self.assertIn("missing Failure condition: in ## Boundary task", errors)
        self.assertIn("missing Validation: in ## Boundary task", errors)

    def test_empty_routing_fixture_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "tests/fixtures/agent-routing.json"
            fixture.parent.mkdir(parents=True)
            fixture.write_text("[]\n", encoding="utf-8")
            with patch("run_evaluations.ROOT", root), self.assertRaisesRegex(
                ValueError, "routing fixture must not be empty"
            ):
                evaluate_routing({})

    def test_routing_fixture_requires_nonempty_task(self) -> None:
        fixture = {
            "task": "   ",
            "expected_skill": "common/engineering/testing",
            "boundary_skill": None,
            "expected_explanation": True,
            "confirmation": "never",
            "expected_validation": True,
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture_path = root / "tests/fixtures/agent-routing.json"
            fixture_path.parent.mkdir(parents=True)
            fixture_path.write_text(json.dumps([fixture]), encoding="utf-8")
            records = {"common/engineering/testing": {"status": "experimental"}}
            with patch("run_evaluations.ROOT", root):
                results, failures = evaluate_routing(records)
            self.assertEqual(failures, 1)
            self.assertIn("task must be a nonempty string", results[0]["errors"])

if __name__ == "__main__":
    unittest.main()
