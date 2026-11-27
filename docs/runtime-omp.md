# oh-my-pi (`omp`) integration

`omp` discovers project `.agents/skills`, walking up from working directory to repo root, plus user-level `~/.agents/skills`. Canonical `.agents/skills`, not `.agent/skills`. `scripts/install_skills.py`.

## Install selected

```bash
# Preview
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project --check

# Copy
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project

# Global symlinks
python3 scripts/install_skills.py --bundle feature-delivery --global
```

`feature-delivery` **5 skills**. Safe sync no overwrite. `scripts/sync_skills.py` doesn't exist.

## Verify local discovery

```bash
omp skill list
omp skill list --json
```

Confirm installed skill `filePath` under project `.agents/skills`. Listing merges project + user; distinguish path not name. Local discovery only; no model selection/reasoning/followed. Behavior needs representative + boundary when authorized.

## Name collisions

Same frontmatter `name` not dropped: first-admitted bare name; later namespaced `<namespace>/<name>`; `~N` if slot taken. Project admitted before user; project keeps bare name over same-named user. This library repeats display names (`core`, `research`, etc.). Install smallest set; use `omp skill list --json` confirm `filePath` + namespaced entries. Canonical path IDs/adapter names distinct from display `name`.

## Updating + recovery

Don't edit installed copy as source. Re-sync + confirm; safe stop on conflict; preserve user-managed `.agents/skills`. `omp` follows adapter symlinks for `--global`; verify. Removed source not automatically cleaned. See [integration recovery](integration.md#recovering-an-installation-mismatch) + [adapter lifecycle](integration.md#adapter-lifetime-and-ownership). `.agent/skills` not canonical. Re-run `scripts/install_skills.py`. `.skill-catalog.json` only if provided + verified.

## Evidence boundary

Record `omp` version, project root, `filePath`, model-backed task? Static listing static evidence. No claim model quality/followed.
