---
name: task-planning
description: Create an actionable implementation plan from a confirmed request, including sequencing, interfaces, tests, and risks.
category: common
subject: foundation
scope: universal
status: experimental
version: 1.0.0
invocation: user
---

# Task planning

## When to use
Use before multi-step work, meaningful dependencies, or a change whose implementation sequence needs to be agreed.

## When not to use
Do not create a large plan for a trivial one-file correction.

## Workflow
1. Inspect the current state and relevant code.
2. Break work into independently verifiable units.
3. Define interfaces, data flow, edge cases, and acceptance criteria.
4. Order changes by dependency and risk.
5. State assumptions and the validation sequence.

## Decision rules
- Prefer small reversible steps and the narrowest scope.
- Plan tests alongside behavior, not after implementation.
- Choose this skill when the user needs an executable sequence, interfaces, risks, and acceptance checks before implementation begins.

## Failure modes
If implementation choices depend on unknown facts, mark them as decisions or gather evidence before planning.

## Expected output
Provide a decision-complete plan another agent can execute without guessing.

## Validation
Every plan item must map to a file change, check, or explicit non-change.
