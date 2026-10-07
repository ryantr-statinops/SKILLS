"""Regression tests for invocation-aware natural discovery."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from discover_skills import discover, normalize_registry  # noqa: E402
from generate_skill_index import collect  # noqa: E402


def args_for(query: str, invocation: str | None = None, bundle: str | None = None):
    return type(
        "Args",
        (),
        {
            "query": query.split(),
            "category": None,
            "scope": None,
            "status": None,
            "invocation": invocation,
            "bundle": bundle,
            "limit": 10,
        },
    )()


class DiscoveryBoundaryTests(unittest.TestCase):
    def test_both_skill_is_discoverable_from_natural_query(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "discover_skills.py"),
                "--format",
                "json",
                "--invocation",
                "both",
                "debugging",
                "software",
                "failures",
                "reproduce",
                "isolate",
                "hypothesize",
                "root",
                "cause",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["skills"][0]["id"], "common/engineering/debugging")
        self.assertEqual(payload["skills"][0]["invocation"], "both")

    def test_user_workflow_is_discoverable_from_direct_request(self) -> None:
        results = discover(
            args_for(
                "feature delivery export feature vertical slice tests review",
                invocation="user",
            )
        )
        self.assertTrue(results)
        self.assertEqual(results[0]["id"], "common/workflow/feature-delivery")
        self.assertEqual(results[0]["invocation"], "user")

    def test_unfiltered_ranking_is_stable_after_bundle_filtering(self) -> None:
        query = "feature delivery export feature vertical slice tests review"
        before = [item["id"] for item in discover(args_for(query))]
        discover(args_for(query, invocation="user", bundle="feature-delivery"))
        after = [item["id"] for item in discover(args_for(query))]
        self.assertEqual(before, after)

    def test_model_invocation_is_reserved(self) -> None:
        self.assertNotIn("model", {record["invocation"] for record in collect()})

    def test_registry_container_shape_is_validated(self) -> None:
        invalid_registries = [
            [],
            {"schema_version": 3},
            {"schema_version": 3, "skills": {}},
        ]
        for registry in invalid_registries:
            with self.subTest(registry=registry), self.assertRaises(ValueError):
                normalize_registry(registry)

    def test_incomplete_and_wrongly_typed_skill_records_are_rejected(self) -> None:
        incomplete = dict(collect()[0])
        incomplete.pop("name")
        wrong_type = dict(collect()[0])
        wrong_type["name"] = ["not", "a string"]
        for record in (incomplete, wrong_type):
            with self.subTest(record=record), self.assertRaises(ValueError):
                normalize_registry({"schema_version": 3, "skills": [record]})

if __name__ == "__main__":
    unittest.main()
