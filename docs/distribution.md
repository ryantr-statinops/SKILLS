# Skill distribution

Canonical installed runtime root `.agents/skills`. Source repo `common/`, `personal/`, `meta/`. `.agent/skills` not canonical.

## Direct install

Prefer `scripts/install_skills.py` for selected export:

```bash
python3 scripts/install_skills.py --list-bundles
python3 scripts/install_skills.py --bundle bug-fixing --project /path/to/project --check
python3 scripts/install_skills.py --bundle bug-fixing --project /path/to/project
```

`--check` no write. Normal safe sync stops when target exists. Review/remove existing target deliberately before retrying; confirm. `--global` symlink source; `--project` copy. Removed source not automatically cleaned. `.skill-catalog.json` only if provided by consumer sync; `scripts/install_skills.py` doesn't write it.

## Git subtree vendoring

For vendoring reviewed source library, subtree prefix is consumer-specific. Source repo root contains `common/`, `personal/`, `meta/`, not pre-installed `.agents/skills`. Don't confuse vendored source layout with runtime output. Example only; verify source layout:

```bash
git fetch skills main
git subtree pull --prefix=<subtree-prefix> skills main --squash
```

Use `main` for deliberate latest; reviewed commit/tag for reproducible snapshot. Don't silently update production to moving branch. Record source commit/tag. Review diff, run source checks, representative consumer task. Review subtree conflicts manually, especially `SKILL.md`, references, scripts, evaluation files. No destructive cleanup. Prefer changing source repo + pulling reviewed snapshot over editing vendored files as local overrides.

## Consumer boundaries

- Keep project-specific instructions outside installed skills/subtree.
- Preserve relative resource paths.
- Keep secrets/private data/project-only procedures out.
- No push/tag/release/publish without explicit request.
- Contributing back via subtree push only intentional portable changes; project-specific stays consumer.

## Change compatibility

Adding additive; removing/changing member/layout distribution change; record changelog/release notes. Registry schema version 3; discovery accepts 1–3; old `requires` defaults `[]`; re-sync writes current. Safe sync preserves conflicts + check/no-write path. See [compatibility](compatibility.md), [versioning](versioning.md).
