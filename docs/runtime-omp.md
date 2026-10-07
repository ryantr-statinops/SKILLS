# oh-my-pi (omp) integration

`omp`, the oh-my-pi coding agent, discovers project skills from both
`.agent/skills` and `.agents/skills`, walking up from the working directory to
the repository root, plus user-level `~/.agent[s]/skills`. Each skills root is
scanned exactly one level deep: only `<root>/<entry>/SKILL.md` entries load.
The nested portable tree (`common/workflow/...`) is therefore invisible to
`omp` directly; generate the flat `.agents/skills/` adapter, whose entries are
single-level directories the scanner reads.

## Install selected skills

Run these commands from the SKILLS checkout. Replace the project path with the
consumer repository:

```bash
python3 scripts/sync_skills.py --bundle feature-delivery --check /path/to/project/.agent/skills
python3 scripts/sync_skills.py --bundle feature-delivery /path/to/project/.agent/skills
python3 scripts/export_runtime_adapter.py --check /path/to/project/.agent/skills /path/to/project/.agents/skills
python3 scripts/export_runtime_adapter.py /path/to/project/.agent/skills /path/to/project/.agents/skills
```

Review each `--check` result before applying. If `.agent/skills/` already has a
sync manifest, use `--update` with the complete intended selection; a normal
install is rejected to protect manifest ownership. If a native destination
conflicts, stop and follow [the reviewed cutover procedure](integration.md#cut-over-an-existing-native-skill-root).

## Verify local discovery

In the project, list discovered skills exactly as a session would see them:

```bash
omp skill list
```

Confirm each installed skill appears with a `filePath` under the project's
`.agents/skills/` directory. The listing merges project-level and user-level
skills, so distinguish entries by path rather than by name alone. This proves
local discovery; it makes no claim about model selection, reasoning quality,
or whether the skill was followed.

## Name collisions

Skills that share a frontmatter `name` are not dropped: the first-admitted
skill keeps the bare name and later ones are namespaced as
`<namespace>/<name>` (a `~N` suffix when that slot is taken). Within the agent
provider, project-level entries are admitted before user-level ones, so a
project skill keeps the bare name over a same-named user skill. This library
has repeated display names (four skills named `core`, two named `research`),
so install the smallest useful set and use `omp skill list --json` to confirm
which `filePath` holds each bare name and which entries were namespaced.

## Updating and recovery

Edit or update skills in `.agent/skills/`; existing native symlinks expose
those changes (`omp` follows the adapter links). Re-run the exporter after
adding skills. It is additive: removed source skills leave links behind, and
existing conflicts are not overwritten. Preserve user-managed files in
`.agents/skills/`; see [integration recovery](integration.md#recovering-an-installation-mismatch)
and [adapter lifecycle](integration.md#adapter-lifetime-and-ownership).

## Evidence boundary

Record the `omp` version, project root, the `filePath` values reported by
`omp skill list`, and whether any model-backed task was run. A skill listing
is static evidence only. To assess behavior, run a representative task and a
nearby boundary task through normal `omp` use only when model use is
authorized, then inspect the resulting artifacts.