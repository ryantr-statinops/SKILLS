# Compatibility

`SKILLS` stores skills as plain Markdown plus optional local resources. This
makes the library portable, but each agent runtime may differ in discovery,
directory conventions, symlink support, and script execution. Codex and
OpenCode now have verified discovery layouts; only Codex has an optional model
evaluation job.

## Baseline assumptions

- A skill is a directory containing `SKILL.md`.
- The runtime can read Markdown and follow relative links.
- Optional resources remain next to the skill entrypoint.
- Project-specific instructions live in the selected agent directory's `AGENTS.md`.
- Scripts are not trusted automatically; review them before execution.

## Integration compatibility

When integrating into another runtime, verify:

1. Which directory the runtime scans for agent instructions and skills.
2. Whether the runtime recognizes `SKILL.md` and YAML frontmatter.
3. Whether nested `references/`, `scripts/`, `examples/`, and `assets/` paths are accessible.
4. Whether scripts need a particular interpreter or dependency.
5. How project instructions and skill instructions are prioritized.

Use `python3 scripts/inspect_integration.py /path/to/project` to produce a
read-only report of detected runtime directories, instruction files, skill
roots, conflicts, and recommended integration methods.

## Directory adapters

Use `.agent/` as the portable baseline. Codex and OpenCode can consume the
generated `.agents/skills/` adapter. Generate it with:

```bash
python3 scripts/export_runtime_adapter.py \
  /path/to/project/.agent/skills /path/to/project/.agents/skills
```

The adapter uses symlinked skill directories so portable relative resources
remain valid. A runtime-specific project may map the same payload to another
directory, such as `.claude/` or `.codex/`, but that adapter must be verified
before it is treated as supported.

The directory name alone does not prove that a runtime will discover skills.
Record the tested runtime version, layout, and representative task result.

Do not claim runtime support until a representative task has been tested in
that runtime.

## Portability rules

- Prefer relative links and standard Markdown.
- Avoid runtime-specific metadata unless documented as optional.
- Keep executable helpers self-contained and state their prerequisites.
- Separate portable procedure from personal or runtime-specific integration.

## Change compatibility contract

Changes to the library must preserve existing consumer integrations unless a
breaking change is explicitly documented.

- The generated skill registry is schema version 3. Discovery reads versions 1–3;
  old records without `requires` default to `[]`, while present dependency lists
  are retained and validated. Sync writes the current schema on the next update.
- Other additive metadata fields require a migration path or documented default.
- Future registry schema changes must update the schema version and preserve a
  compatibility reader when older consumers can be supported safely.
- Sync changes must preserve the selected target layout, report conflicts, and
  provide a check or dry-run path before overwriting files.
- A runtime adapter must not change the portable meaning of a `SKILL.md`.
- Runtime support claims require a fixture, tested layout, runtime version,
  representative task, and validation result.

Record confirmed runtime behavior here as evidence accumulates. Keep uncertain
assumptions explicit instead of presenting them as a universal standard.

| Runtime | Layout | Verification | Scope of guarantee |
| --- | --- | --- | --- |
| Codex | `.agents/skills/<path-id>/SKILL.md` | adapter unit test; Codex Action smoke/nightly when `OPENAI_API_KEY` is configured | static discovery always; model behavior only when the CI job runs |
| OpenCode 1.18.31 | `.agents/skills/<path-id>/SKILL.md` | `opencode debug skill --pure` fixture test | discovery and frontmatter loading; no model quality claim |

## Ecosystem research

The current comparison and adoption decisions are recorded in the
[ecosystem matrix](ecosystem-matrix.md) and
[ecosystem decisions](ecosystem-decisions.md). They are research inputs, not
runtime support claims. A runtime becomes supported only after a fixture,
version, layout, representative task, and validation result are recorded.
