"""Smoke-test a portable Codex-compatible consumer project."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/codex-consumer-project"
INSPECT = ROOT / "scripts/inspect_integration.py"
SYNC = ROOT / "scripts/sync_skills.py"
DISCOVER = ROOT / "scripts/discover_skills.py"


class ConsumerSmokeTests(unittest.TestCase):
    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_fixture_inspection_bundle_sync_and_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "consumer"
            shutil.copytree(FIXTURE, project)
            skills_root = project / ".agent/skills"

            inspected = self.run_script(INSPECT, str(project), "--format", "json")
            self.assertEqual(inspected.returncode, 0, inspected.stderr)
            report = json.loads(inspected.stdout)
            self.assertEqual(report["recommended_method"], "selected-sync")
            self.assertEqual(report["recommended_destination"], ".agent/skills")
            self.assertIn("AGENTS.md", report["instruction_files"])

            checked = self.run_script(
                SYNC,
                "--bundle",
                "portable-agent-baseline",
                "--check",
                str(skills_root),
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertEqual(
                list(skills_root.rglob("SKILL.md")),
                [],
                "check mode must not copy skills",
            )

            synced = self.run_script(
                SYNC,
                "--bundle",
                "portable-agent-baseline",
                str(skills_root),
            )
            self.assertEqual(synced.returncode, 0, synced.stderr)
            self.assertGreaterEqual(len(list(skills_root.rglob("SKILL.md"))), 1)
            self.assertTrue(
                (skills_root / "common/foundation/repository-onboarding/SKILL.md").is_file()
            )

            conflict = self.run_script(
                SYNC,
                "--bundle",
                "portable-agent-baseline",
                str(skills_root),
            )
            self.assertNotEqual(conflict.returncode, 0)
            self.assertIn("destination is already managed", conflict.stderr)

            discovered = self.run_script(
                DISCOVER,
                "--format",
                "json",
                "build",
                "a",
                "feature",
            )
            self.assertEqual(discovered.returncode, 0, discovered.stderr)
            results = json.loads(discovered.stdout)["skills"]
            self.assertEqual(results[0]["id"], "common/workflow/feature-delivery")

            catalog_discovered = self.run_script(
                DISCOVER,
                "--registry",
                str(skills_root / ".skill-catalog.json"),
                "--format",
                "json",
                "repository",
            )
            self.assertEqual(catalog_discovered.returncode, 0, catalog_discovered.stderr)
            self.assertEqual(
                json.loads(catalog_discovered.stdout)["skills"][0]["id"],
                "common/foundation/repository-onboarding",
            )

            boundary = self.run_script(
                DISCOVER,
                "--format",
                "json",
                "investigate",
                "software",
                "failure",
                "reproduce",
                "isolate",
                "root",
                "cause",
            )
            self.assertEqual(boundary.returncode, 0, boundary.stderr)
            boundary_results = json.loads(boundary.stdout)["skills"]
            self.assertTrue(boundary_results)
            self.assertEqual(boundary_results[0]["id"], "common/engineering/debugging")
            self.assertNotEqual(
                boundary_results[0]["id"], "common/workflow/feature-delivery"
            )

            consumer_test = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                cwd=project,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(consumer_test.returncode, 0, consumer_test.stderr)


if __name__ == "__main__":
    unittest.main()
