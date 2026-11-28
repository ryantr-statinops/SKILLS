## Summary of Changes
<!-- Concise summary of what was added, changed, or fixed -->

## Category
- [ ] `common/` (Reusable skills)
- [ ] `personal/` (Personal workflow & domain skills)
- [ ] `meta/` (Authoring, discovery, and evaluation tooling)
- [ ] `docs/` (Architecture, integration, and guides)
- [ ] `scripts/` or `.github/` (Tooling and CI)

## Pre-merge Verification Checklist
- [ ] Skill structure and metadata valid: `python3 scripts/validate_skills.py`
- [ ] Skill index up to date: `python3 scripts/generate_skill_index.py --check`
- [ ] Local Markdown links valid: `python3 scripts/check_markdown_links.py`
- [ ] Test suites passing: `pytest -q`
- [ ] No whitespace errors: `git diff --check`
- [ ] Conventional Commit format used
