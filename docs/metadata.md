# Skill metadata

Every `SKILL.md` uses YAML frontmatter so humans/tools discover skill without reading full body.

## Required schema

```yaml
---
name: skill-name
description: What the skill does and when it applies.
category: meta
subject: skill-system
scope: repository
status: stable
version: 1.0.0
invocation: both
---
```

### Fields

- `name`: lowercase local skill name; match final directory; repeats across scopes allowed; canonical path IDs unique.
- `description`: concise capability + activation boundary.
- `category`: `common`, `personal`, `meta`; match root directory.
- `subject`: lowercase topic grouping.
- `scope`: `universal`, `personal`, `repository`.
- `status`: `draft`, `experimental`, `stable`, `deprecated`.
- `version`: SemVer `MAJOR.MINOR.PATCH`.
- `invocation`: `user`, `model`, `both`.
- `requires`: optional list canonical skill IDs.

`invocation` portable; no Claude/Codex/plugin runtime commands. `user` explicit workflow; `both` user + agent; `model` intentional agent-selected. Canonical ID path-derived, e.g. `meta/skill-authoring`; don't duplicate in frontmatter.

## Generated registry

Source truth frontmatter. `docs/skill-index.md` human-readable; `data/skills.json` machine-readable.

```bash
python3 scripts/generate_skill_index.py
python3 scripts/generate_skill_index.py --check
```

Registry schema version **3**. Discovery accepts **1–3**; old records without `requires` default `[]`; present lists retained + validated. Re-sync writes current schema. Generated registry schema changes update version + compatibility reader when safe. Regenerate after metadata changes; don't manual edit `docs/skill-index.md`.
