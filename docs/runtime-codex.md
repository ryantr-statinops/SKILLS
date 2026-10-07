# Codex CLI integration

Codex CLI can discover project skills from `.agents/skills/`. Keep `.agent/skills/`
as the portable, sync-managed content source and expose it through the native
adapter. The adapter creates flat, source-ID-derived symlink names so distinct
skills with the same leaf name remain separate.

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

In the project, record the CLI version and inspect model-visible prompt inputs:

```bash
codex --version
codex debug prompt-input "Inspect the installed skills"
```

`debug prompt-input` prints JSON without starting a model turn. Confirm the
project skill appears in the skill list and that its root/location points under
`.agents/skills/`. This proves local prompt construction exposed the skill
metadata; it does not prove the model selected, loaded, or followed the skill.
The output may also include user-level and bundled skills, so distinguish their
roots from project-local entries.

To assess behavior, run a representative task and a nearby boundary task through
the normal Codex CLI only when model use is authorized. Inspect the resulting
artifacts and report the CLI version, task, output, and limits of the run. Do not
use `codex exec` as part of a static discovery check: it starts an agent session
and may contact a configured provider.

## Updating and recovery

Edit or update skills in `.agent/skills/`; existing native symlinks expose those
changes. Re-run the exporter after adding skills. It is additive: removed source
skills leave links behind, and existing conflicts are not overwritten. Preserve
user-managed files in `.agents/skills/`; see [integration recovery](integration.md#recovering-an-installation-mismatch)
and [adapter lifecycle](integration.md#adapter-lifetime-and-ownership).

## Evidence boundary

Record the Codex CLI version, project root, skill path shown by
`debug prompt-input`, and whether any model-backed task was run. A local prompt
inspection is static discovery evidence only. Codex does not expose a
model-free command that proves skill reasoning quality.