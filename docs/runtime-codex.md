# Codex CLI integration

Codex discovers project skills `.agents/skills/`; user-level `~/.agents/skills/`. Canonical `.agents/skills`, not `.agent/skills`. `scripts/install_skills.py`.

## Install selected

From SKILLS checkout; replace consumer path:

```bash
# Preview no-write
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project --check

# Copy into <project>/.agents/skills
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project

# Global symlinks
python3 scripts/install_skills.py --bundle feature-delivery --global
```

`feature-delivery` **5 skills**. Conflict-safe: `--check` no write; normal sync stops existing target; not overwrite; confirm remove. Installed adapter hyphenated ID. `scripts/sync_skills.py` doesn't exist.

## Verify local discovery

```bash
codex --version
codex debug prompt-input "Inspect the installed skills"
```

`debug prompt-input` prints JSON no model turn. Confirm project skill + root/location under `.agents/skills`. Local prompt construction only; not model selected/loaded/followed. Output includes user-level + bundled; distinguish roots. No `codex exec` static discovery; starts agent + may contact provider. Behavior needs representative + boundary task through normal Codex when model use authorized; inspect artifacts; report CLI version/task/output/limits. Model-free doesn't prove reasoning quality.

## Updating + recovery

Don't edit installed copy as source. Update source skill; for `--project` re-sync after confirming/removing generated target; for `--global` verify symlink source. Re-run safe check. Removed source not automatically cleaned. Existing conflicts not overwritten. Preserve user-managed `.agents/skills`. See [integration recovery](integration.md#recovering-an-installation-mismatch) + [adapter lifecycle](integration.md#adapter-lifetime-and-ownership). `.agent/skills` not canonical. Re-run exporter equivalent `scripts/install_skills.py`, not nonexistent exporter. Correct links manually; markdown file check not anchor check.

## Evidence boundary

Record Codex version, project root, skill path from `debug prompt-input`, whether model-backed task ran. Static discovery only static evidence. No model-free command proves skill reasoning quality.
