"""Unit tests for direct skills installer scripts/install_skills.py."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/install_skills.py"


class InstallSkillsTests(unittest.TestCase):
    def test_list_bundles(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--list-bundles"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("engineering-core", result.stdout)
        self.assertIn("feature-delivery", result.stdout)

    def test_check_project_mode_does_not_create_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_dir = Path(temp) / "my_project"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--bundle", "research-decision", "--project", str(project_dir), "--check"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("[check] copy", result.stdout)
            self.assertIn("common-workflow-research-decision", result.stdout)
            self.assertFalse(project_dir.exists())

    def test_install_project_mode_copies_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_dir = Path(temp) / "my_project"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--bundle", "research-decision", "--project", str(project_dir)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            dest = project_dir / ".agents/skills"
            self.assertTrue((dest / "common-workflow-research-decision/SKILL.md").is_file())
            self.assertTrue((dest / "common-research-research/SKILL.md").is_file())

    def test_install_global_mode_creates_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target_dir = Path(temp) / "global_skills"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "common/engineering/debugging", "--target", str(target_dir), "--global"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            link = target_dir / "common-engineering-debugging"
            self.assertTrue(link.is_symlink())
            self.assertTrue((link / "SKILL.md").is_file())

    def test_unknown_bundle_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_dir = Path(temp) / "my_project"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--bundle", "non-existent-bundle", "--project", str(project_dir)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unknown bundle: non-existent-bundle", result.stderr)


if __name__ == "__main__":
    unittest.main()
