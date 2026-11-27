# OpenCode integration

OpenCode discovers `.agents/skills/`; user-level `~/.agents/skills`. Canonical `.agents/skills`, not `.agent/skills`. `scripts/install_skills.py`.

## Install selected

```bash
# Preview
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project --check

# Copy into <project>/.agents/skills
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project

# Global symlinks
python3 scripts/install_skills.py --bundle feature-delivery --global
```

`feature-delivery` **5 skills**, not 6. Conflict-safe sync. Installed adapter hyphenated ID.

## Verify local discovery

```bash
opencode --version
opencode debug skill --pure
```

Confirm each installed skill `location` under `.agents/skills`. Local discovery + frontmatter loading; no model selection/reasoning/followed claim. Output includes built-in + user-level; filter project path. Observed OpenCode 1.18.35 with `feature-delivery`, e.g. `.agents/skills/common-workflow-feature-delivery/SKILL.md`, local only.

## Updating + recovery

Don't edit installed copy as source. Re-sync after source changes + confirmation; verify symlink source for `--global`. Safe sync no overwrite; conflicting target stops. Removed source not automatically cleaned. Preserve user-managed `.agents/skills`. See [integration recovery](integration.md#recovering-an-installation-mismatch) + [adapter lifecycle](integration.md#adapter-lifetime-and-ownership). `.agent/skills` not canonical. Re-run `scripts/install_skills.py`, not nonexistent exporter. `scripts/sync_skills.py` doesn't exist. `.skill-catalog.json` only if provided + verified.

## Evidence boundary

Record OpenCode version, project root, `location`, model-backed task? Static listing static evidence. Behavior needs representative + boundary through normal OpenCode when authorized; inspect artifacts.
