# Agent operating model

Goal: load context, select smallest relevant capability, perform authorized work, validate, report honestly.

## Lifecycle

```text
context loading
  → task classification
  → skill discovery
  → skill selection
  → user-facing explanation
  → confirmation check
  → execution
  → validation
  → final report
```

## Loading order

1. Root `AGENTS.md` and applicable runtime instructions.
2. `local.md` if present; local-only current state, never portable rule or public source.
3. `docs/skill-index.md` or `data/skills.json` for candidate discovery.
4. Category/router `SKILL.md` when one exists.
5. Selected leaf `SKILL.md`.
6. Only required references, scripts, examples, assets.

Do not load every skill. If no skill clearly applies, continue with repository guidance and state no skill activated.

## Selection explanation

Before risky or multi-step tasks, briefly state:

- selected skill ID(s);
- why match outcome;
- assumptions/exclusions;
- mutation or external action requiring confirmation.

This is not manual execution instruction to user.

## Autonomy and confirmation

Agent may inspect, reason, edit in scope, run validation when authorized. Pause before:

- deleting, resetting, overwriting, broad destructive cleanup;
- writing external systems/services;
- pushing, tagging, releasing, publishing when not explicitly requested;
- irreversible or materially scope-expanding decisions.

Preserve unrelated user changes. Stop on unexpected conflicts or remote state. Do not infer permission from skill availability. Safe sync stops before overwriting existing targets; confirm any removal/replacement.

## Final report

Include when relevant:

```text
Selected skill(s):
Reason:
Changed files:
Validation:
Unresolved risks or assumptions:
Next action:
```

Report actual actions and checks; don't claim unrun checks. Keep proportional. Expose uncertainty.
