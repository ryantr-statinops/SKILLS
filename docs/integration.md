# Agent-driven integration

Expose selected SKILLS capabilities to project/coding-agent runtime.

## Canonical layout

Modern runtimes discover `.agents/skills/<hyphenated-id>/SKILL.md`, user-level `~/.agents/skills/`. Canonical installed root **`.agents/skills/`**, not `.agent/skills`. Source repo `common/`, `personal/`, `meta/` separate. Installed adapter name hyphenated canonical ID, e.g. `common-workflow-feature-delivery`. `scripts/install_skills.py` converts `common/workflow/feature-delivery` → `common-workflow-feature-delivery`.

## Installer

```text
SKILLS repository
   ├── --global   → symlink into ~/.agents/skills/<hyphenated-id> (or --target)
   └── --project  → copy into <project>/.agents/skills/<hyphenated-id>
```

```bash
# Preview no-write
python3 scripts/install_skills.py --bundle engineering-core --global --check
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project --check

# Install
python3 scripts/install_skills.py --bundle engineering-core --global
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project

# Custom target
python3 scripts/install_skills.py --bundle feature-delivery --target ~/.codex/skills --global

# List bundles
python3 scripts/install_skills.py --list-bundles
```

`--project` copies; `--global` symlinks; `--target` overrides destination. `--check` no write. **Conflict-safe:** normal sync stops when selected target exists; existing non-symlinks aren't overwritten; symlinks pointing elsewhere aren't replaced. `--check` reports conflicts. Remove/replace existing target only after explicit confirmation. `scripts/sync_skills.py` doesn't exist; use `scripts/install_skills.py`. `scripts/install_skills.py` doesn't generate `.skill-catalog.json`; don't claim it does.

Project example after `feature-delivery`:

```text
<project>/.agents/skills/
├── common-workflow-feature-delivery/
├── common-foundation-requirements-analysis/
├── common-foundation-task-planning/
├── common-engineering-testing/
└── common-engineering-code-review/
```

## Bundles

`data/bundles.json` source truth. `feature-delivery` currently **5 skills**. See [bundles](bundles.md). No consumer copy of skill content.

## Shared context

Copy `templates/CONTEXT.md` into consumer project root. Provides domain vocabulary, architecture boundaries, test seams, artifact locations without polluting portable skills. Project instructions stay outside installed skills.

## Recovering an installation mismatch

1. Inspect `git status` + consumer `.agents/skills`.
2. Run `scripts/install_skills.py ... --check`.
3. Distinguish project-local vs user-level vs bundled skills.
4. Preserve user-managed files; don't overwrite.
5. Move/remove known generated target only after confirmation; then re-run safe sync.
6. Re-check runtime discovery + representative task.

## Adapter lifetime and ownership

Installed adapters generated from source. Source repo canonical; consumer project instructions outside `.agents/skills`. For `--project`, re-sync after source changes; don't edit installed copy as source. For `--global`, symlink source updates visible if runtime follows symlinks, but verify. Removed source not automatically cleaned; no removed-source cleanup promised. Conflicting target stops sync. Preserve user-managed entries.
