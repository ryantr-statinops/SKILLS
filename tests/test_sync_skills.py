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

    def test_update_restores_missing_managed_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            selected = "common/engineering/testing"
            installed = self.run_sync(str(destination), selected)
            self.assertEqual(installed.returncode, 0, installed.stderr)
            target = destination / selected / "SKILL.md"
            target.unlink()
            checked = self.run_sync("--update", "--check", str(destination), selected)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertIn(f"would update {target}", checked.stdout)
            self.assertFalse(target.exists())
            updated = self.run_sync("--update", str(destination), selected)
            self.assertEqual(updated.returncode, 0, updated.stderr)
            self.assertEqual(target.read_bytes(), (ROOT / selected / "SKILL.md").read_bytes())

    def test_update_preflights_non_directory_target_ancestors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            first = self.run_sync(str(destination), "common/engineering/debugging")
            self.assertEqual(first.returncode, 0, first.stderr)
            manifest = (destination / ".skill-sync.json").read_bytes()
            debug_skill = destination / "common/engineering/debugging/SKILL.md"
            debug_content = debug_skill.read_bytes()
            obstruction = destination / "common/engineering/testing"
            obstruction.write_text("unmanaged file", encoding="utf-8")
            checked = self.run_sync(
                "--update", "--check", str(destination),
                "common/engineering/debugging", "common/engineering/testing",
            )
            self.assertEqual(checked.returncode, 2)
            self.assertIn(str(obstruction), checked.stderr)
            self.assertEqual((destination / ".skill-sync.json").read_bytes(), manifest)
            self.assertEqual(debug_skill.read_bytes(), debug_content)
            self.assertEqual(obstruction.read_text(encoding="utf-8"), "unmanaged file")

    def test_update_rejects_directory_at_managed_file_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            installed = self.run_sync(str(destination), "common/engineering/debugging")
            self.assertEqual(installed.returncode, 0, installed.stderr)
            manifest_path = destination / ".skill-sync.json"
            manifest = manifest_path.read_bytes()
            target = destination / "common/engineering/debugging/SKILL.md"
            content = target.read_bytes()
            target.unlink()
            target.mkdir()
            rejected = self.run_sync("--update", str(destination), "common/engineering/debugging")
            self.assertEqual(rejected.returncode, 2)
            self.assertIn(str(target), rejected.stderr)
            self.assertEqual(manifest_path.read_bytes(), manifest)
            self.assertTrue(target.is_dir())
            self.assertEqual(content, (ROOT / "common/engineering/debugging/SKILL.md").read_bytes())

    def test_update_rejects_nonfile_catalog_before_copying_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            installed = self.run_sync(str(destination), "common/engineering/debugging")
            self.assertEqual(installed.returncode, 0, installed.stderr)
            manifest_path = destination / ".skill-sync.json"
            manifest = manifest_path.read_bytes()
            catalog = destination / ".skill-catalog.json"
            catalog.unlink()
            catalog.mkdir()
            rejected = self.run_sync(
                "--update", str(destination),
                "common/engineering/debugging", "common/engineering/testing",
            )
            self.assertEqual(rejected.returncode, 2)
            self.assertIn(str(catalog), rejected.stderr)
            self.assertEqual(manifest_path.read_bytes(), manifest)
            self.assertFalse((destination / "common/engineering/testing/SKILL.md").exists())
            self.assertTrue(catalog.is_dir())

    def test_failed_update_removes_newly_created_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            first = self.run_sync(str(destination), "common/engineering/debugging")
            self.assertEqual(first.returncode, 0, first.stderr)
            manifest_path = destination / ".skill-sync.json"
            catalog_path = destination / ".skill-catalog.json"
            manifest = manifest_path.read_bytes()
            catalog = catalog_path.read_bytes()
            wrapper = """
import pathlib, runpy, shutil, sys
script = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(script.parent))
destination = pathlib.Path(sys.argv[2])
original = shutil.copy2
copies = 0
def fail_during_apply(source, target, *args, **kwargs):
    global copies
    target = pathlib.Path(target)
    if target.is_relative_to(destination):
        copies += 1
        if copies == 2:
            raise OSError("injected copy failure")
    return original(source, target, *args, **kwargs)
shutil.copy2 = fail_during_apply
sys.argv = [str(script), "--update", str(destination),
            "common/engineering/debugging", "common/engineering/testing"]
runpy.run_path(str(script), run_name="__main__")
"""
            failed = subprocess.run(
                [sys.executable, "-c", wrapper, str(SCRIPT), str(destination)],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("injected copy failure", failed.stderr)
            self.assertEqual(manifest_path.read_bytes(), manifest)
            self.assertEqual(catalog_path.read_bytes(), catalog)
            testing = destination / "common/engineering/testing"
            self.assertFalse(list(testing.rglob("SKILL.md")) if testing.exists() else [])

if __name__ == "__main__":
    unittest.main()
