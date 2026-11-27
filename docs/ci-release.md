# CI and release workflow

## Continuous validation

GitHub Actions PR + `main`. Checks skill metadata, generated indexes, evaluation contracts, local Markdown links, whitespace. No network external URLs. Separate Codex workflows PR smoke + nightly: absent `OPENAI_API_KEY`, print `chưa cấu hình OPENAI_API_KEY`, agent behavior unverified. With secret, `openai/codex-action@v1`, Codex CLI **0.154.0**, model `gpt-5.3-codex`; require smoke only after secret. Static validator + deterministic evals don't need key. CI version separate runtime discovery evidence. Model-backed tasks only authorized.

## Local same checks

```bash
pytest -q
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/validate_skills.py
python3 scripts/generate_skill_index.py --check
python3 scripts/run_evaluations.py --format json
python3 scripts/check_observable_evaluations.py --format json
python3 scripts/check_markdown_links.py
git diff --check
```

After metadata/skill changes: `python3 scripts/generate_skill_index.py`, then `--check`. `docs/skill-index.md` generated not manual. `scripts/check_markdown_links.py` checks local file targets, not anchors; verify runtime links manually. Full safe sync tests `python3 -m unittest tests.test_install_skills`.

## Release preparation

CI no tags/publish/push. Release explicit maintainer after reviewed batch:

1. validation green;
2. diff + generated registry;
3. skill SemVer + changelog;
4. compatibility/subtree/breaking notes;
5. create + push `vMAJOR.MINOR.PATCH` only approved;
6. release report commit/tag/skill count/checks/limitations.

No tag/release/publish inferred. No external service changes.

## External URLs

Optional opt-in `python3 scripts/check_markdown_links.py --external`. Network failures not local docs failure. No external check in CI requirement. HEAD checks; report uncertainty.
