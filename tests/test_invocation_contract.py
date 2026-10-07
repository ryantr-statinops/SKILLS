"""Regression tests for invocation metadata, registry, and discovery."""

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from discover_skills import normalize_registry  # noqa: E402
from generate_skill_index import REGISTRY_SCHEMA_VERSION, collect, render_json  # noqa: E402
from migrate_invocation_metadata import expected_invocation, migrate_text  # noqa: E402
from validate_skills import HANDOFF_FIELDS, activation_contract_errors, handoff_contract_errors  # noqa: E402


class InvocationContractTests(unittest.TestCase):
    def test_all_skills_have_expected_invocation(self) -> None:
        records = collect()
        self.assertEqual({record["invocation"] for record in records}, {"user", "both"})
        for record in records:
            self.assertEqual(record["invocation"], expected_invocation(record["id"]))

    def test_migration_inserts_invocation_after_version(self) -> None:
        source = (
            "---\n"
            "name: task-planning\n"
            "version: 1.0.0\n"
            "---\n"
            "\n"
            "# Task planning\n"
        )
        migrated = migrate_text(source, "common/foundation/task-planning")
        self.assertIn("version: 1.0.0\ninvocation: user\n---\n", migrated)
        self.assertEqual(
            migrate_text(migrated, "common/foundation/task-planning"), migrated
        )

    def test_unknown_skill_requires_an_explicit_mapping(self) -> None:
        with self.assertRaises(ValueError):
            expected_invocation("common/new-skill")

    def test_registry_uses_schema_v3_and_exposes_dependencies(self) -> None:
        registry = json.loads(render_json(collect()))
        self.assertEqual(registry["schema_version"], REGISTRY_SCHEMA_VERSION)
        self.assertTrue(all("invocation" in item for item in registry["skills"]))
        self.assertTrue(all("requires" in item for item in registry["skills"]))

    def test_schema_v1_defaults_legacy_records_to_both(self) -> None:
        record = dict(collect()[0])
        record.pop("invocation")
        record.pop("requires")
        records = normalize_registry({"schema_version": 1, "skills": [record]})
        self.assertEqual(records[0]["invocation"], "both")

    def test_schema_v2_rejects_invalid_invocation(self) -> None:
        record = dict(collect()[0])
        record["invocation"] = "implicit"
        with self.assertRaises(ValueError):
            normalize_registry({"schema_version": 2, "skills": [record]})

    def test_schema_v2_defaults_dependencies(self) -> None:
        record = dict(collect()[0])
        record.pop("requires")
        records = normalize_registry({"schema_version": 2, "skills": [record]})
        self.assertEqual(records[0]["requires"], [])

    def test_model_invocation_requires_activation_contract(self) -> None:
        incomplete = "## When to use\n\nUse this skill.\n"
        errors = activation_contract_errors(incomplete, "model")
        self.assertIn("## Do not activate when", " ".join(errors))
        self.assertIn("## Expected output", " ".join(errors))
        self.assertIn("## Validation", " ".join(errors))

    def test_complete_model_activation_contract_is_accepted(self) -> None:
        complete = "\n".join(
            (
                "## When to use",
                "## Do not activate when",
                "## Expected output",
                "## Validation",
                "## Agent handoff",
            )
        )
        self.assertEqual(activation_contract_errors(complete, "model"), [])

    def test_non_model_invocation_does_not_require_model_contract(self) -> None:
        self.assertEqual(activation_contract_errors("", "both"), [])


    def test_handoff_contract_rejects_empty_values(self) -> None:
        empty = "## Agent handoff\n" + "\n".join(HANDOFF_FIELDS)
        errors = handoff_contract_errors(empty)
        self.assertEqual(len(errors), len(HANDOFF_FIELDS))
        self.assertTrue(all(message.startswith("empty agent handoff field:") for message in errors))

        valid = "## Agent handoff\n" + "\n".join(
            f"{field} a concrete contract value" for field in HANDOFF_FIELDS
        )
        self.assertEqual(handoff_contract_errors(valid), [])

if __name__ == "__main__":
    unittest.main()
