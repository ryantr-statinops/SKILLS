"""Regression tests for the bundle registry contract."""

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from bundles import validate_skill_dependency_references, validate_bundle_registry  # noqa: E402
from discover_skills import discover  # noqa: E402


def record(
    identifier: str,
    scope: str = "universal",
    status: str = "experimental",
    requires: list[str] | None = None,
) -> dict[str, object]:
    return {
        "id": identifier,
        "scope": scope,
        "status": status,
        "requires": requires or [],
    }


class BundleRegistryTests(unittest.TestCase):
    def test_unbundled_skill_cannot_reference_missing_dependency(self) -> None:
        with self.assertRaisesRegex(ValueError, "skill dependency is missing from registry"):
            validate_skill_dependency_references(
                [record("personal/statistics", requires=["common/not-real"])]
            )

    def test_unbundled_dependency_cycles_are_rejected(self) -> None:
        cycles = [
            [record("personal/statistics", requires=["personal/statistics"])],
            [
                record("personal/a", requires=["personal/b"]),
                record("personal/b", requires=["personal/a"]),
            ],
        ]
        for records in cycles:
            with self.subTest(records=records), self.assertRaisesRegex(ValueError, "cyclic"):
                validate_skill_dependency_references(records)

    def test_empty_registry_is_valid(self) -> None:
        self.assertEqual(
            validate_bundle_registry({"schema_version": 1, "bundles": []}, []), []
        )

    def test_valid_bundle_is_returned(self) -> None:
        bundle = {
            "id": "engineering-core",
            "description": "Reusable engineering skills.",
            "scope": "universal",
            "runtime_target": "portable",
            "allow_deprecated": False,
            "skills": ["common/engineering/testing"],
        }
        result = validate_bundle_registry(
            {"schema_version": 1, "bundles": [bundle]},
            [record("common/engineering/testing")],
        )
        self.assertEqual(result, [bundle])

    def test_missing_skill_is_rejected(self) -> None:
        bundle = {
            "id": "broken",
            "description": "Broken bundle.",
            "scope": "universal",
            "runtime_target": "portable",
            "allow_deprecated": False,
            "skills": ["common/missing"],
        }
        with self.assertRaisesRegex(ValueError, "missing skill"):
            validate_bundle_registry({"schema_version": 1, "bundles": [bundle]}, [])

    def test_universal_bundle_cannot_contain_personal_skill(self) -> None:
        bundle = {
            "id": "broken",
            "description": "Broken bundle.",
            "scope": "universal",
            "runtime_target": "portable",
            "allow_deprecated": False,
            "skills": ["personal/example"],
        }
        with self.assertRaisesRegex(ValueError, "personal skill"):
            validate_bundle_registry(
                {"schema_version": 1, "bundles": [bundle]},
                [record("personal/example", scope="personal")],
            )

    def test_deprecated_skill_requires_explicit_opt_in(self) -> None:
        bundle = {
            "id": "broken",
            "description": "Broken bundle.",
            "scope": "universal",
            "runtime_target": "portable",
            "allow_deprecated": False,
            "skills": ["common/old"],
        }
        with self.assertRaisesRegex(ValueError, "deprecated skill"):
            validate_bundle_registry(
                {"schema_version": 1, "bundles": [bundle]},
                [record("common/old", status="deprecated")],
            )

    def test_bundle_requires_declared_dependencies(self) -> None:
        bundle = {
            "id": "workflow",
            "description": "Workflow bundle.",
            "scope": "universal",
            "runtime_target": "portable",
            "allow_deprecated": False,
            "skills": ["common/workflow/example"],
        }
        with self.assertRaisesRegex(ValueError, "missing skill dependency"):
            validate_bundle_registry(
                {"schema_version": 1, "bundles": [bundle]},
                [record("common/workflow/example", requires=["common/engineering/testing"]), record("common/engineering/testing")],
            )

    def test_bundle_rejects_cyclic_dependencies(self) -> None:
        bundle = {
            "id": "cycle",
            "description": "Cyclic bundle.",
            "scope": "universal",
            "runtime_target": "portable",
            "allow_deprecated": False,
            "skills": ["common/a", "common/b"],
        }
        records = [record("common/a", requires=["common/b"]), record("common/b", requires=["common/a"])]
        with self.assertRaisesRegex(ValueError, "cyclic"):
            validate_bundle_registry({"schema_version": 1, "bundles": [bundle]}, records)

    def test_discovery_filters_to_bundle_members(self) -> None:
        args = type(
            "Args",
            (),
            {
                "query": ["feature"],
                "category": None,
                "scope": None,
                "status": None,
                "invocation": None,
                "bundle": "feature-delivery",
                "limit": 20,
            },
        )()
        results = discover(args)
        self.assertTrue(results)
        self.assertIn("common/workflow/feature-delivery", {item["id"] for item in results})
        self.assertTrue(
            all(
                item["id"]
                in {
                    "common/workflow/feature-delivery",
                    "common/foundation/requirements-analysis",
                    "common/foundation/task-planning",
                    "common/engineering/testing",
                    "common/engineering/code-review",
                    "common/delivery/change-review",
                }
                for item in results
            )
        )


if __name__ == "__main__":
    unittest.main()
