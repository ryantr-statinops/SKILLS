"""Regression tests for bundle-based selected sync."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import json

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/sync_skills.py"


class SyncSkillsTests(unittest.TestCase):
    def run_sync(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_list_bundles(self) -> None:
        result = self.run_sync("--list-bundles")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("feature-delivery", result.stdout)
        self.assertIn("personal-python", result.stdout)

    def test_check_mode_does_not_copy_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            result = self.run_sync("--bundle", "feature-delivery", "--check", str(destination))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(destination.exists())
            self.assertFalse((destination / ".skill-sync.json").exists())

    def test_sync_copies_bundle_and_rejects_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            first = self.run_sync("--bundle", "feature-delivery", str(destination))
            self.assertEqual(first.returncode, 0, first.stderr)
            copied = destination / "common/workflow/feature-delivery/SKILL.md"
            self.assertTrue(copied.is_file())
            manifest = destination / ".skill-sync.json"
            self.assertTrue(manifest.is_file())
            self.assertTrue((destination / ".skill-catalog.json").is_file())
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["bundle"], "feature-delivery")
            self.assertTrue(
                any(item["path"].endswith("feature-delivery/SKILL.md") for item in payload["files"])
            )
            for template in (
                "CONTEXT.md",
                "feature-spec.md",
                "code-review-report.md",
                "handoff.md",
            ):
                self.assertTrue((destination / "templates" / template).is_file())

            second = self.run_sync("--bundle", "feature-delivery", str(destination))
            self.assertNotEqual(second.returncode, 0)
            self.assertTrue((destination / "common/workflow/feature-delivery/SKILL.md").is_file())
            self.assertEqual(manifest.read_text(encoding="utf-8"), json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
            self.assertIn("destination is already managed", second.stderr)

    def test_explicit_workflow_sync_includes_declared_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            result = self.run_sync(
                str(destination),
                "common/workflow/feature-delivery",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(
                (destination / "common/foundation/task-planning/SKILL.md").is_file()
            )

    def test_update_check_and_local_modification_guard(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            first = self.run_sync("--bundle", "feature-delivery", str(destination))
            self.assertEqual(first.returncode, 0, first.stderr)
            checked = self.run_sync(
                "--bundle", "feature-delivery", "--update", "--check", str(destination)
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)
            skill = destination / "common/workflow/feature-delivery/SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8") + "\nlocal edit\n", encoding="utf-8")
            rejected = self.run_sync("--bundle", "feature-delivery", "--update", str(destination))
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("modified locally", rejected.stderr)

    def test_rejects_incremental_install_to_managed_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            first = self.run_sync(str(destination), "common/engineering/debugging")
            self.assertEqual(first.returncode, 0, first.stderr)
            manifest = (destination / ".skill-sync.json").read_text(encoding="utf-8")
            catalog = (destination / ".skill-catalog.json").read_text(encoding="utf-8")
            second = self.run_sync(str(destination), "common/engineering/testing")
            self.assertEqual(second.returncode, 2)
            self.assertIn("use --update with the complete selection", second.stderr)
            self.assertTrue((destination / "common/engineering/debugging/SKILL.md").is_file())
            self.assertEqual((destination / ".skill-sync.json").read_text(encoding="utf-8"), manifest)
            self.assertEqual((destination / ".skill-catalog.json").read_text(encoding="utf-8"), catalog)

    def test_overlapping_parent_and_child_selection_installs_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            selected = ("personal/engineering", "personal/engineering/backend/python")
            checked = self.run_sync("--check", str(destination), *selected)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertEqual(checked.stdout.count("would sync personal/engineering ->"), 1)
            self.assertFalse(destination.exists())
            installed = self.run_sync(str(destination), *selected)
            self.assertEqual(installed.returncode, 0, installed.stderr)
            self.assertTrue((destination / "personal/engineering/backend/python/SKILL.md").is_file())
            catalog = json.loads((destination / ".skill-catalog.json").read_text(encoding="utf-8"))
            catalog_ids = {skill["id"] for skill in catalog["skills"]}
            self.assertTrue(set(selected).issubset(catalog_ids))
            manifest = json.loads((destination / ".skill-sync.json").read_text(encoding="utf-8"))
            paths = [item["path"] for item in manifest["files"]]
            self.assertEqual(len(paths), len(set(paths)))

if __name__ == "__main__":
    unittest.main()
