---
name: feature-delivery
description: Lead a feature from clarified outcome through planning, vertical implementation, testing, review, and handoff.
category: common
subject: workflow
scope: universal
status: stable
version: 1.1.0
invocation: user
requires: [common/foundation/requirements-analysis, common/foundation/task-planning, common/engineering/testing, common/engineering/code-review]
---

# Feature delivery

## When to use

Use when the user wants to build or materially change a feature and the work
needs a coordinated plan, implementation path, verification, and review.

## When not to use

Do not use for an isolated bug diagnosis, a research-only question, or a small
edit whose scope and verification are already obvious.

## Workflow

1. Read `CONTEXT.md` when present and inspect repository instructions and state.
2. Use requirements analysis to confirm outcome, users, constraints, and scope.
3. Use task planning to define interfaces, sequencing, risks, and acceptance criteria.
4. Agree on the public seams and tests before implementation.
5. Implement one vertical slice at a time, keeping changes inside the approved scope.
6. Run focused checks during implementation and the full required suite at the end.
7. Review the change for correctness, maintainability, security, regression risk, and test adequacy.
8. Run change review before handoff and report unresolved risks.
9. Write the feature specification and handoff artifacts using the linked templates when requested or authorized.

## Decision rules

- Do not invent requirements to fill an ambiguous gap; surface the decision.
- Prefer a small vertical slice with feedback over a large speculative implementation.
- Do not add unrelated refactoring, dependencies, or infrastructure.
- A user-invoked workflow may read `both` skills but must not silently start another user workflow.

## Failure modes

- If the outcome or public seam is unclear, pause after analysis and ask for the missing decision.
- If tests or checks fail, preserve the evidence, diagnose the failure, and do not claim completion.
- If the requested change exceeds the agreed scope, report the expansion before proceeding.

## Supporting resources

- [`CONTEXT.md` template](../../../templates/CONTEXT.md) — copy into a consumer project when shared context is missing.
- [`feature-spec.md`](../../../templates/feature-spec.md) — use for the feature artifact.
- [`code-review-report.md`](../../../templates/code-review-report.md) — use for review output.
- [`handoff.md`](../../../templates/handoff.md) — use for final handoff output.

## Expected output and validation

Provide the confirmed outcome, plan, changed files, tests and checks, review
result, unresolved risks, and next action. Validate the agreed seams, focused
tests, full required checks, and final diff scope.
