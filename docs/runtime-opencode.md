# OpenCode integration

OpenCode discovers project skills from the `.agents/skills/` layout (or user-level `~/.agents/skills/`).

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

In the project, record the CLI version and list discovered skills without
starting a model turn:

```bash
opencode --version
opencode debug skill --pure
```

Confirm each installed skill appears with a `location` under the project's
`.agents/skills/` directory. This proves local discovery and frontmatter
loading; it makes no claim about model selection, reasoning quality, or whether
the skill was followed. The output also includes built-in and user-level
skills, so filter by the project path when checking.

Observed locally: OpenCode 1.18.35 discovered all six `feature-delivery`
bundle skills through the adapter (for example
`.agents/skills/common-workflow-feature-delivery/SKILL.md`).

## Updating and recovery

Edit or update skills in `.agent/skills/`; existing native symlinks expose
those changes. Re-run the exporter after adding skills. It is additive:
removed source skills leave links behind, and existing conflicts are not
overwritten. Preserve user-managed files in `.agents/skills/`; see
[integration recovery](integration.md#recovering-an-installation-mismatch)
and [adapter lifecycle](integration.md#adapter-lifetime-and-ownership).

## Evidence boundary

Record the OpenCode version, project root, the `location` paths reported by
`debug skill --pure`, and whether any model-backed task was run. A discovery
listing is static evidence only. To assess behavior, run a representative task
and a nearby boundary task through normal OpenCode use only when model use is
authorized, then inspect the resulting artifacts.