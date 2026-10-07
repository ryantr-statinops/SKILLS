"""Tests for the native runtime adapter layout."""

import subprocess
import tempfile
import json
import shutil
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/export_runtime_adapter.py"


class RuntimeAdapterTests(unittest.TestCase):
    def test_check_is_non_mutating_and_export_uses_unique_flat_names(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / ".agent/skills"
            (source / "common/engineering/debugging").mkdir(parents=True)
            (source / "personal/debugging").mkdir(parents=True)
            for directory in (source / "common/engineering/debugging", source / "personal/debugging"):
                (directory / "SKILL.md").write_text("---\nname: debugging\n---\n", encoding="utf-8")
            destination = root / ".agents/skills"
            check = subprocess.run(
                ["python3", str(SCRIPT), "--check", str(source), str(destination)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("common-engineering-debugging", check.stdout)
            self.assertFalse(destination.exists())
            subprocess.run(["python3", str(SCRIPT), str(source), str(destination)], check=True)
            rerun = subprocess.run(
                ["python3", str(SCRIPT), str(source), str(destination)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(rerun.stdout, "")
            first = destination / "common-engineering-debugging"
            second = destination / "personal-debugging"
            self.assertTrue(first.is_symlink())
            self.assertTrue(second.is_symlink())
            self.assertTrue((first / "SKILL.md").is_file())
            self.assertEqual(
                subprocess.run(
                    ["python3", str(SCRIPT), "--check", str(source), str(destination)],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout,
                "",
            )

    def test_opencode_cli_discovers_adapter(self) -> None:
        executable = shutil.which("opencode")
        if executable is None:
            self.skipTest("opencode CLI is not installed")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / ".agent/skills/common/engineering/debugging"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text(
                "---\nname: debugging\ndescription: Debug a failing behavior\n---\n# Debugging\n",
                encoding="utf-8",
            )
            portable = root / ".agent/skills"
            native = root / ".agents/skills"
            subprocess.run(["python3", str(SCRIPT), str(portable), str(native)], check=True)
            result = subprocess.run(
                [executable, "debug", "skill", "--pure"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            )
            skills = json.loads(result.stdout)
            discovered = [item for item in skills if item["name"] == "debugging"]
            self.assertEqual(len(discovered), 1)
            self.assertTrue(discovered[0]["location"].endswith(".agents/skills/common-engineering-debugging/SKILL.md"))


if __name__ == "__main__":
    unittest.main()
