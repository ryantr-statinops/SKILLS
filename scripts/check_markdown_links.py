#!/usr/bin/env python3
"""Check relative Markdown links without requiring network access by default."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen

from markdown_links import extract_markdown_link_targets

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--external",
        action="store_true",
        help="also check HTTP(S) links; may be affected by network changes",
    )
    return parser.parse_args()


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "__pycache__" not in path.parts
    )


def local_target(source: Path, target: str) -> Path | None:
    target = target.strip().strip("<>")
    parsed = urlparse(target)
    if parsed.scheme or target.startswith("//"):
        return None
    path_text = unquote(parsed.path)
    if not path_text:
        return source
    return (source.parent / path_text).resolve()


def external_target(target: str) -> bool:
    parsed = urlparse(target.strip().strip("<>"))
    return parsed.scheme in {"http", "https"}


def check_external(target: str) -> str | None:
    request = Request(target, method="HEAD", headers={"User-Agent": "SKILLS-link-checker/1"})
    try:
        with urlopen(request, timeout=10) as response:
            if response.status >= 400:
                return f"HTTP {response.status}"
    except Exception as exc:  # network checks are explicitly opt-in
        return str(exc)
    return None


def main() -> int:
    args = parse_args()
    failures = 0
    checked = 0
    skipped_external = 0
    for source in markdown_files():
        text = source.read_text(encoding="utf-8")
        for target in extract_markdown_link_targets(text):
            target = target.strip()
            if not target or target.startswith(("mailto:", "tel:")):
                continue
            if external_target(target):
                if not args.external:
                    skipped_external += 1
                    continue
                error = check_external(target)
                checked += 1
                if error:
                    print(f"ERROR: {source.relative_to(ROOT)} -> {target}: {error}")
                    failures += 1
                continue
            resolved = local_target(source, target)
            if resolved is None:
                continue
            checked += 1
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                print(f"ERROR: link escapes repository: {source.relative_to(ROOT)} -> {target}")
                failures += 1
                continue
            if not resolved.exists():
                print(f"ERROR: broken local link: {source.relative_to(ROOT)} -> {target}")
                failures += 1
    print(f"Checked {checked} local link(s); skipped {skipped_external} external link(s).")
    if failures:
        print(f"Link check failed with {failures} issue(s).")
        return 1
    print("Markdown links passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
