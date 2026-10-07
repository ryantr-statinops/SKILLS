# Agent-driven integration

This guide explains how an agent can expose selected SKILLS capabilities to an
existing project or coding-agent runtime. The user provides the desired
outcome; the agent inspects the project, proposes the smallest integration,
performs authorized local changes, validates them, and reports the result.

For the repository model, read [architecture](architecture.md). For the
agent lifecycle, read [agent operating model](agent-operating-model.md).

## Agent integration flow

```text
user intent
  → inspect target project and runtime
  → detect instruction and skill directories
  → choose subtree, selected sync, or copy
  → show scope, conflicts, and side effects
  → request confirmation when required
  → integrate selected skills
  → validate links, metadata, and runtime layout
  → report files, checks, and unresolved risks
```

The agent should integrate the smallest useful set of skills. It should not
copy the whole library merely because the repository exists.

## Inspect before changing

From the SKILLS repository, inspect a target project without mutation:

```bash
python3 scripts/inspect_integration.py /path/to/project
```

The report identifies `.agent/`, `.agents/`, `.codex/`, and `.claude/` paths,
existing `AGENTS.md` or runtime instruction files, existing skill roots,
conflicting paths, and recommended validation commands.

If the runtime is unknown, use `.agent/` as the portable baseline and record
the adapter assumption. A directory name alone does not prove that a runtime
will discover skills.

## Integration options

### Git subtree — recommended for a vendored library

Use a subtree when the target project should keep an integrated copy in its own
history:

```bash
git remote add skills https://github.com/ryantr-statinops/SKILLS.git
git fetch skills main
git subtree add --prefix=.agent/skills skills main --squash
```

For updates:

```bash
git fetch skills main
git subtree pull --prefix=.agent/skills skills main --squash
```

Review the diff, preserve project-specific instructions outside the subtree,
run source validation where available, and test one representative task before
accepting the update. Use a reviewed commit or release tag when the consumer
needs a reproducible snapshot.

Only use subtree push when the target intentionally contributes a portable
change back to SKILLS:

```bash
git subtree push --prefix=.agent/skills skills main
```

Never push project-only instructions, secrets, or private overrides back to the
public library.

### Selected sync — recommended for a small project scope

Validate a selected export before copying:

```bash
python3 scripts/sync_skills.py --check /path/to/project/.agent/skills \
  common/engineering/git-workflow personal/workflow/project-init
```

After review, run the same command without `--check`. The helper preserves the
selected skill directory structure and copies supporting resources with it.
The agent must inspect existing target paths and report any overwrite before
syncing.

When selected skill directories overlap, the parent tree is copied once while
all explicitly selected skill records remain in the installed catalog.

When the project needs a complete workflow, use a named bundle:

```bash
python3 scripts/sync_skills.py --list-bundles
python3 scripts/sync_skills.py --bundle feature-delivery --check /path/to/project/.agent/skills
python3 scripts/sync_skills.py --bundle feature-delivery /path/to/project/.agent/skills
```

For the supported baseline, inspect `data/promoted.json` and record the source
commit or release tag alongside the selected bundle. Promotion is a support
boundary, not a second copy of the skill content.

Bundle sync validates every referenced skill and stops if any target path
already exists. It never overwrites a selected skill implicitly.

Every normal sync writes `.skill-sync.json` (source, bundle, selected skills,
and per-file hashes) and `.skill-catalog.json` (the installed skill metadata).
Once a manifest exists, a normal install into that destination is rejected: it
would replace ownership metadata while leaving old files unmanaged. Use
`--update` with the complete desired selection, not only newly added skills.
Review with `--check --update`; apply with `--update`. Update restores managed
files missing from the consumer and rejects locally edited files for review
instead of overwriting them. On caught copy or metadata-write failures, it
restores prior managed content and ownership metadata and removes new files.
This is not a crash- or power-loss-safe transaction. The catalog is the
preferred discovery input.

### Direct copy or development symlink

Direct copy is appropriate for a one-time, small integration. A symlink can be
used during local skill development when the runtime supports it, but it is not
a portable distribution mechanism and should not be assumed in documentation.

## Runtime adapters

Keep portable skill content under the same internal layout and adapt only the
outer runtime directory:

```text
portable baseline: .agent/skills/
possible adapters: .agents/skills/, .codex/skills/, .claude/skills/
```

Runtime-specific notes, hooks, plugins, and always-on instructions belong in
the adapter or its instruction file. Do not rewrite a portable `SKILL.md` to
fit one runtime when the difference belongs in `AGENTS.md` or an adapter.

The repository can generate a native `.agents/skills/` adapter from an existing
`.agent/skills/` export. Adapter directory names encode the full source ID with
hyphens (for example `common-engineering-debugging`) so repeated leaf names do
not collide. The adapter keeps the portable source content and its relative
resources intact.

```bash
python3 scripts/export_runtime_adapter.py \
  /path/to/project/.agent/skills /path/to/project/.agents/skills
```

Runtime-specific install, verify, and recovery details live in the per-runtime
guides: [Codex CLI](runtime-codex.md), [OpenCode](runtime-opencode.md), and
[oh-my-pi (`omp`)](runtime-omp.md). Each guide records what its local
discovery command proves and where static evidence stops.

### Adapter lifetime and ownership

Adapter entries are symlinks, not copies or snapshots. Edits under the portable
source tree are visible through an existing link; adding a skill requires
another export run. The exporter does not prune links for skills removed from the
source and does not rewrite a link that conflicts with an existing destination.

Keep the portable source at the same relative location for the lifetime of the
adapter. Moving only the source or native root can invalidate links. Run the
exporter's `--check` before changing either path; treat a conflict as a manual
ownership review, not permission to replace the link.

To remove one adapter entry, first confirm it is a symlink created by this
exporter and that its target is the intended source skill. Remove only that link;
never recursively delete the native root. Retain the source tree and any
user-managed entries.

### Cut over an existing native skill root

Keep `.agent/skills/` as the content source and build or update it first with
the selected sync command. Do not point the exporter at an existing native tree
until its contents are reviewed: the exporter refuses any conflicting
destination and does not merge or overwrite files.

1. Inventory `.agents/skills/` and classify each entry as user-managed, direct
   copy, or previously generated adapter. Preserve user-managed and locally
   edited content; do not infer ownership from directory names.
2. Run the exporter with `--check` and inspect every proposed link. If any
   destination already exists with different content, stop. Obtain approval for
   a cutover, then move the reviewed old native root to a unique backup path
   outside `.agents/skills/`. Never remove the backup during installation.
3. Run the exporter without `--check` only after `.agents/skills/` has no
   conflicting entries. Verify each generated link resolves to the intended
   portable source and its resources.
4. Use the runtime's native skill-list/debug command to verify the entrypoint
   path and version, then exercise a representative task and a boundary task.
5. If verification fails, preserve the new adapter and old backup for review.
   Restore the previous root only after a reviewed rollback plan; do not merge
   or overwrite either tree automatically. Remove the backup only after the new
   runtime layout is accepted and the owner explicitly approves cleanup.

The exporter is an additive link creator, not a migration or cleanup tool.

## Bringing in an existing skill

When a user provides a skill from another repository or an existing local
system, inspect it before copying:

1. Read its entrypoint, license, source references, scripts, and resource tree.
2. Check for secrets, private data, destructive actions, hidden dependencies,
   and runtime-specific assumptions.
3. Decide whether to copy, adapt, rebuild, or reject it using
   `meta/skill-intake/SKILL.md`.
4. Classify it as `common`, `personal`, or `meta`.
5. Normalize the frontmatter and portable body without copying generic
   textbook material.
6. Add representative and boundary evaluation cases.
7. Regenerate the registry and run the complete validation flow.

A one-file Markdown skill may only need metadata and boundary adaptation. A
complex skill with references, scripts, examples, or assets must preserve only
resources that are real, reviewed, and linked progressively.

## Post-integration validation

From the source repository, run:

```bash
python3 scripts/validate_skills.py
python3 scripts/generate_skill_index.py --check
python3 scripts/run_evaluations.py --format json
python3 scripts/check_markdown_links.py
```

In the target project, verify that the runtime discovers the selected directory,
relative resources resolve, project instructions do not weaken skill boundaries,
and a representative task plus nearby non-activation task behave as expected.

## Recovering an installation mismatch

Use the portable tree as the content source and the native adapter only as a
discovery view. Diagnose the layer that diverged before reinstalling anything:

1. If selected skills or `.skill-catalog.json` are missing or stale, review the
   complete original selection with `sync_skills.py --check --update`, using the
   same destination and all selected IDs (or the original bundle) recorded in
   `.skill-sync.json`; apply the same command only after reviewing its changes.
   A normal install cannot repair a destination already owned by a sync manifest.
2. If the portable `.agent/skills/` tree is correct but `.agents/skills/` entries
   are missing, run `export_runtime_adapter.py --check` against those roots,
   review the reported additions, then run it without `--check`. The exporter
   refuses a conflicting destination; do not delete or replace that path to
   force an export.
3. If adapter entries exist, inspect their symlink targets and verify the
   relative resource paths resolve from the native view. Re-run the adapter
   check; an empty report means no links need creating, not that the runtime
   loaded them.
4. Ask the target runtime's own skill-list/debug command whether it discovers
   the exact installed entrypoint. Record the runtime version, reported path, and
   result. If the path is correct but discovery fails, treat that runtime/layout
   as unverified rather than changing portable skill content or claiming
   runtime support.

Never replace the whole `.agents/skills/` directory during recovery: it may
contain user-managed files outside this adapter. Preserve conflicting content
for review; only remove a generated link after verifying its target and owner.
