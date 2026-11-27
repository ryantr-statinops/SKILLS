"""Regression tests for context fallback and confirmation boundaries."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class WorkflowBehaviorTests(unittest.TestCase):
    def test_behavior_fixture_matches_workflow_contracts(self) -> None:
        cases = json.loads(
            (ROOT / "tests/fixtures/workflow-behavior.json").read_text(encoding="utf-8")
        )
        context = (ROOT / "templates/CONTEXT.md").read_text(encoding="utf-8")
        for case in cases:
            workflow_path = ROOT / case["workflow"] / "SKILL.md"
            workflow = workflow_path.read_text(encoding="utf-8")
            self.assertIn(case["artifact_root"], context, case["name"])
            for term in case["required_terms"]:
                self.assertIn(term, workflow, case["name"])

    def test_context_template_documents_default_and_override_behavior(self) -> None:
        context = (ROOT / "templates/CONTEXT.md").read_text(encoding="utf-8")
        self.assertIn("Override these paths", context)
        self.assertIn("If this section is left unchanged", context)
        self.assertIn("docs/agent/", context)


if __name__ == "__main__":
    unittest.main()
