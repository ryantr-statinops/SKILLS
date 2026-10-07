"""Regression tests for rendered Markdown link extraction and checking."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from check_markdown_links import main as check_links, markdown_files  # noqa: E402
from markdown_links import extract_markdown_link_targets  # noqa: E402
from validate_skills import validate_skill  # noqa: E402


class MarkdownLinkTests(unittest.TestCase):
    def test_extracts_titled_parenthesized_and_reference_destinations(self) -> None:
        text = (
            '[Guide](guide.md "A title")\n'
            "[Architecture](guide(arch).md)\n"
            "[Missing][missing-guide]\n"
            "[missing-guide]: absent.md\n"
            "`[inline code](not-a-link.md)`\n"
            "```markdown\n[code sample](not-a-link-either.md)\n```\n"
        )
        self.assertEqual(
            extract_markdown_link_targets(text),
            ["absent.md", "guide.md", "guide(arch).md"],
        )

    def test_checker_ignores_code_but_finds_broken_reference_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            (root / "guide.md").write_text("guide", encoding="utf-8")
            (root / "guide(arch).md").write_text("architecture", encoding="utf-8")
            source.write_text(
                '[Guide](guide.md "A title")\n'
                "[Architecture](guide(arch).md)\n"
                "[Missing][missing-guide]\n"
                "[missing-guide]: absent.md\n"
                "`[code](not-a-link.md)`\n"
                "```markdown\n[example](also-not-a-link.md)\n```\n",
                encoding="utf-8",
            )
            output = StringIO()
            with (
                patch("check_markdown_links.ROOT", root),
                patch("check_markdown_links.markdown_files", return_value=[source]),
                patch.object(sys, "argv", ["check_markdown_links.py"]),
                redirect_stdout(output),
            ):
                result = check_links()
            self.assertEqual(result, 1)
            self.assertIn("broken local link: source.md -> absent.md", output.getvalue())
            self.assertNotIn("not-a-link.md", output.getvalue())
            self.assertNotIn("also-not-a-link.md", output.getvalue())


    def test_skill_validator_uses_shared_rendered_link_parser(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "meta/demo"
            skill.mkdir(parents=True)
            (skill / "guide.md").write_text("guide", encoding="utf-8")
            entrypoint = (
                "---\nname: demo\ndescription: Example demo skill\ncategory: meta\n"
                "subject: testing\nscope: repository\nstatus: stable\nversion: 1.0.0\n"
                "invocation: user\n---\n# Demo\n\n## Agent handoff\n"
                "- Selected when: a demo is needed\n- Do not activate when: it is not\n"
                "- Expected output: a report\n- User-facing report: a summary\n"
                "- Confirmation boundary: before external actions\n\n"
                "[Guide](guide.md \"A title\")\n[Missing][broken]\n"
                "[broken]: absent.md\n`[fake](inline-missing.md)`\n"
                "```markdown\n[fake](fenced-missing.md)\n```\n"
            )
            (skill / "SKILL.md").write_text(entrypoint, encoding="utf-8")
            output = StringIO()
            with patch("validate_skills.ROOT", root), redirect_stdout(output):
                failures = validate_skill(skill)
            self.assertEqual(failures, 1)
            self.assertIn("absent.md", output.getvalue())
            self.assertNotIn("inline-missing.md", output.getvalue())
            self.assertNotIn("fenced-missing.md", output.getvalue())

if __name__ == "__main__":
    unittest.main()
