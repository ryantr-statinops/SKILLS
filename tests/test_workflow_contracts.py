"""Regression tests for workflow, context, artifact, and bundle contracts."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


WORKFLOWS = {
    "feature-delivery": "feature-spec.md",
    "bug-fixing": "bug-diagnosis.md",
    "research-decision": "research-decision.md",
    "data-analysis": "data-analysis-report.md",
}


class WorkflowContractTests(unittest.TestCase):
    def test_workflows_have_contract_sections_and_evaluations(self) -> None:
        required_sections = (
            "## When to use",
            "## When not to use",
            "## Workflow",
            "## Decision rules",
            "## Failure modes",
            "## Expected output and validation",
        )
        for name, artifact in WORKFLOWS.items():
            directory = ROOT / "common/workflow" / name
            skill = (directory / "SKILL.md").read_text(encoding="utf-8")
            evaluation = directory / "examples/evaluation.md"
            self.assertIn("invocation: user", skill)
            self.assertIn("scope: universal", skill)
            for section in required_sections:
                self.assertIn(section, skill, name)
            self.assertIn(artifact, skill)
            self.assertTrue(evaluation.is_file())

    def test_context_template_has_default_artifact_layout(self) -> None:
        context = (ROOT / "templates/CONTEXT.md").read_text(encoding="utf-8")
        for field in (
            "Domain vocabulary",
            "Architecture boundaries",
            "Testing and verification",
            "Issue tracking and decisions",
            "Artifact root: `docs/agent/`",
            "Feature specifications: `docs/agent/specs/`",
            "Bug diagnostics: `docs/agent/diagnostics/`",
            "Research decisions: `docs/agent/decisions/`",
            "Analysis reports: `docs/agent/reports/`",
            "Handoffs: `docs/agent/handoffs/`",
        ):
            self.assertIn(field, context)

    def test_all_workflow_bundles_include_the_matching_workflow(self) -> None:
        registry = json.loads((ROOT / "data/bundles.json").read_text(encoding="utf-8"))
        bundles = {bundle["id"]: set(bundle["skills"]) for bundle in registry["bundles"]}
        for name in WORKFLOWS:
            self.assertIn(f"common/workflow/{name}", bundles[name])

    def test_universal_bundles_do_not_include_personal_skills(self) -> None:
        registry = json.loads((ROOT / "data/bundles.json").read_text(encoding="utf-8"))
        for bundle in registry["bundles"]:
            if bundle["scope"] == "universal":
                self.assertFalse(any(skill.startswith("personal/") for skill in bundle["skills"]))


if __name__ == "__main__":
    unittest.main()
