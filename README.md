# SKILLS

`SKILLS` is a portable Agent Skill Library for engineering, data, AI, quantitative research, and personal workflows.

## What SKILLS provides

Skills encode operational knowledge: when to act, how to act, which decisions matter, and how to validate the result.

Modern coding agents (Codex, OpenCode, `omp`, Claude Code, Antigravity) discover skills in `.agents/skills/<skill-name>/SKILL.md` or user-level `~/.agents/skills/`.

## Quick Start

### 1. Global Installation (Recommended)

Symlink skills into `~/.agents/skills/` so all local projects can access them without checking skills into version control:

```bash
# Preview
python3 scripts/install_skills.py --bundle engineering-core --global --check

# Install
python3 scripts/install_skills.py --bundle engineering-core --global
```

### 2. Project-Local Installation

Copy skills directly into `<project>/.agents/skills/` when a repository needs to be self-contained:

```bash
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project
```

List all available bundles with:

```bash
python3 scripts/install_skills.py --list-bundles
```

## Bundles

| Outcome | Bundle | Purpose |
| --- | --- | --- |
| Agent context & recovery | `portable-agent-baseline` | Establish context, onboarding, requirements, and recovery. |
| General engineering | `engineering-core` | Implementation, testing, debugging, review, and git. |
| Build a feature | `feature-delivery` | Coordinate requirements, planning, testing, review, and handoff. |
| Fix a defect | `bug-fixing` | Reproduce, isolate, fix, regression-test, and review. |
| Research decision | `research-decision` | Compare alternatives with evidence, trade-offs, and uncertainty. |
| Data analysis | `data-analysis` | Inspect, clean, validate, analyze, and report reproducibly. |
| Python backend | `personal-python` | Ryan's Python backend, API, testing, and debugging practices. |

## Repository Structure

```text
common/     reusable engineering, foundation, research, and workflow skills
personal/   Ryan's personal engineering, AI, data, and domain judgment
meta/       skill authoring and intake procedures
data/       generated skills registry and bundle definitions
scripts/    validator, index generator, and installer tooling
docs/       architecture, authoring, and integration guides
templates/  project CONTEXT.md and artifact templates
tests/      test suite
```

## Validation & Quality

Run checks before committing:

```bash
pytest -q
python3 scripts/validate_skills.py
python3 scripts/generate_skill_index.py --check
python3 scripts/check_markdown_links.py
git diff --check
```

## License

See [LICENSE](LICENSE).
