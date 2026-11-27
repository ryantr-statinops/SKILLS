# Agent-driven integration

This guide explains how to expose selected SKILLS capabilities to a project or coding-agent runtime.

## Core Integration Architecture

Modern runtimes (Codex, OpenCode, `omp`, Claude Code, Antigravity) look for skills in `.agents/skills/<skill-name>/SKILL.md` (or user-level `~/.agents/skills/`).

SKILLS supports two direct installation modes via `scripts/install_skills.py`:

```text
SKILLS Repository
   ├── --global   ──> symlink into ~/.agents/skills/<adapter-name>
   └── --project  ──> copy into <project>/.agents/skills/<adapter-name>
```

---

## 1. Global Installation (Recommended for Local Workstation)

Install skills once at the user level. Any project opened on your machine can access the skills without adding files to the project repository:

```bash
# Preview links
python3 scripts/install_skills.py --bundle engineering-core --global --check

# Install as symlinks into ~/.agents/skills
python3 scripts/install_skills.py --bundle engineering-core --global
```

To link into another runtime directory (e.g. `~/.codex/skills/`):

```bash
python3 scripts/install_skills.py --bundle feature-delivery --target ~/.codex/skills --global
```

---

## 2. Project-Local Installation (When Repository Needs to Self-Contain)

Copy specific skills or bundles directly into a project's `.agents/skills` directory:

```bash
# Preview copy
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project --check

# Copy skills
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project
```

This creates:
```text
/path/to/project/.agents/skills/
├── common-workflow-feature-delivery/SKILL.md
├── common-foundation-requirements-analysis/SKILL.md
├── common-foundation-task-planning/SKILL.md
├── common-engineering-testing/SKILL.md
└── common-engineering-code-review/SKILL.md
```

---

## 3. Bundles Overview

List available bundles:

```bash
python3 scripts/install_skills.py --list-bundles
```

| Bundle | Purpose |
| --- | --- |
| `portable-agent-baseline` | Basic context, recovery, requirements, and onboarding |
| `engineering-core` | Implementation, testing, debugging, review, and git |
| `feature-delivery` | Full lifecycle for building features |
| `bug-fixing` | Reproducing, fixing, regression-testing defects |
| `research-decision` | Evidence-backed trade-offs and tech selection |
| `data-analysis` | End-to-end data validation and reproducible analysis |
| `personal-python` | Ryan's Python backend foundation and API practices |

---

## 4. Shared Project Context

In consumer projects, copy [`templates/CONTEXT.md`](../templates/CONTEXT.md) into the project root. This file provides project-specific domain vocabulary, architecture boundaries, test seams, and artifact locations without polluting portable skills.
