# Skill discovery

Skill discovery is the process of selecting the smallest relevant skill for a
user task without loading the whole library into context.

## Routing sequence

```text
task
  → docs/skill-index.md or data/skills.json
  → candidate descriptions and metadata
  → activation boundaries
  → selected SKILL.md
  → conditional references/scripts/assets
  → execution and validation
```

For common skills, begin with [`common/README.md`](../common/README.md) for
quick routing. Codex should also read [`common/CODEX.md`](../common/CODEX.md);
other runtimes should use only the portable skill entrypoint.

The generated index is a routing aid, not a replacement for the skill
entrypoint. After selecting a candidate, read its `SKILL.md` before following
instructions or loading supporting resources.

## Querying the index

Use `docs/skill-index.md` for human review and `data/skills.json` for tooling
when working in this source repository. A consumer installation should use its
`.skill-catalog.json` instead; it contains only the skills that were installed
there and remains usable when the source registry is unavailable.
Installed catalogs use the generated registry schema (currently version 3),
and discovery accepts schema versions 1–3. For older catalogs without `requires`,
discovery defaults dependencies to an empty list; an existing `requires` list is
preserved and validated. Re-sync to write the current catalog schema.
Regenerate both after changing skill metadata.

```bash
python3 scripts/generate_skill_index.py
python3 scripts/generate_skill_index.py --check
```

Agents can search the generated registry without loading skill bodies:

```bash
python3 scripts/discover_skills.py "build a Node.js API"
python3 scripts/discover_skills.py --category personal "data pipeline"
python3 scripts/discover_skills.py --format json "debug failing test"

# Consumer discovery from an installed catalog
python3 scripts/discover_skills.py --registry /path/to/project/.agent/skills/.skill-catalog.json "debug failing test"
```
With an installed catalog, `--bundle <id>` filters using the bundle membership
snapshot saved at sync time. Older catalogs without that snapshot must be
re-synced with the named bundle. Consumer discovery does not fall back to the
source bundle registry.
For personal engineering work, route through `personal/engineering/SKILL.md`
and load `engineering/core` when computational or systems reasoning is shared
across domains. Use `engineering/data`, `engineering/ai`, or
`engineering/backend` for the relevant domain. Use `personal/statistics` for
statistical reasoning and `personal/quant/research` or
`personal/quant/production-workflow` for quantitative engineering work.

The command returns deterministic candidates only. The agent must read the
selected `SKILL.md` before activating any procedure.

Use `--invocation user`, `--invocation both`, or `--invocation model` when the
activation boundary matters. User-invoked skills are explicit workflow entry
points. Skills marked `both` can be selected by the agent when their
description and boundaries match the task. Invocation filtering describes
activation eligibility; it does not define a dependency graph between skills.

## Routing versus execution

Use discovery before implementation when the task has not been assigned to a
relevant skill. Discovery returns candidates and routing reasons; it does not
implement the request. After a skill is selected, read its entrypoint and follow
that workflow rather than repeating discovery as a substitute for execution.
For skill authoring, evaluation, intake, or maintenance, use the corresponding
meta workflow.

## Selection rules

1. Match the desired outcome, not only a technology keyword.
2. Prefer the most specific skill whose description covers the task.
3. Reject skills whose `when not to use` boundary applies.
4. Combine skills only when their responsibilities are distinct.
5. If no skill clearly applies, continue without forcing an unrelated skill.

## Writing discoverable descriptions

A description should say what the skill does and when it applies. Metadata also
provides category, subject, scope, lifecycle status, and version. The
description should be specific enough to distinguish nearby skills and should
include an exclusion when misrouting is likely.

Prefer:

```yaml
description: Debug Python package installation and metadata problems; not for general Python application development.
```

Avoid:

```yaml
description: Python development helper.
```

## Overlap and conflicts

Resolve overlap through narrower scope, explicit exclusions, and clear expected
outputs. If two skills give conflicting procedures, stop and surface the
conflict rather than silently merging them.
