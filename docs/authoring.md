# Skill authoring

Create/revise skills in `SKILLS`.

## Outcome

Concrete task + observable result. Avoid topic-label-only skills like `python` or `AI`. Keep narrowly scoped. Reusable parts separate from personal preferences.

## Required entrypoint

Every skill has `SKILL.md` with YAML frontmatter. Required schema in [metadata](metadata.md):

```yaml
---
name: skill-name
description: What the skill does and when it applies.
category: common
subject: foundation
scope: universal
status: experimental
version: 1.0.0
invocation: both
---
```

`name` lowercase local name matching final directory. Canonical ID path-derived; don't duplicate in frontmatter. Optional `requires` canonical skill IDs. Registry validation checks references and cycles. Bundle validation checks transitive dependencies.

Body: activation boundaries, scope, workflow, decisions, constraints, failure modes, validation. Start `meta/SKILL_TEMPLATE.md`; remove empty sections. Concrete activation + nearby exclusion; not generic handoff filler.

## Supporting resources

- `references/`: detailed knowledge for particular modes.
- `scripts/`: deterministic operations materially improving reliability.
- `examples/`: demonstrations, fixtures, evaluation cases.
- `assets/`: reusable templates/output artifacts.

No empty dirs, no copying generic manuals, no duplicate knowledge. Link every resource from relevant instruction.

## Classification

- `common/`: broadly reusable.
- `personal/`: Ryan-specific.
- `meta/`: skill-system.

## Invocation

- `user`: explicit workflow entry point / side-effectful orchestration.
- `both`: user-selectable + agent-discoverable.
- `model`: intentional agent-selected only.
- User-invoked workflow may read `both`; must not silently trigger another user-invoked workflow.

Portable; no runtime plugin/slash-command rules.

## Before committing

1. Check activation/exclusion boundaries.
2. Link supporting resources.
3. `python3 scripts/validate_skills.py`.
4. `python3 scripts/generate_skill_index.py`.
5. `python3 scripts/generate_skill_index.py --check`.
6. `python3 scripts/check_markdown_links.py`.
7. `python3 scripts/run_evaluations.py`.
8. One representative + one nearby boundary task.
9. Keep every agent handoff value nonempty; confirmation boundary explicit.
10. `git diff --check`.
