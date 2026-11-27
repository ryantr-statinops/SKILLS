# oh-my-pi (omp) integration

`omp`, the oh-my-pi coding agent, discovers project skills from `.agents/skills`,
walking up from the working directory to the repository root, plus user-level `~/.agents/skills`.

## Install selected skills

Run these commands from the SKILLS checkout. Replace the project path with the
consumer repository:

```bash
# Preview
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project --check

# Install directly into <project>/.agents/skills
python3 scripts/install_skills.py --bundle feature-delivery --project /path/to/project
```

Or install globally as symlinks into `~/.agents/skills/`:

```bash
python3 scripts/install_skills.py --bundle feature-delivery --global
```

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