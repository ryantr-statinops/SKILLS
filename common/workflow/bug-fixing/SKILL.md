---
name: bug-fixing
description: Diagnose and fix a software defect through reproduction, isolation, evidence, regression testing, review, and handoff.
category: common
subject: workflow
scope: universal
status: stable
version: 1.1.0
invocation: user
requires: [common/engineering/debugging, common/engineering/testing, common/engineering/refactoring, common/engineering/code-review, common/agent/failure-recovery]
---

# Bug fixing

## When to use

Use when the user reports a failure, regression, inconsistent behavior, or
performance problem that needs diagnosis and a verified fix.

## When not to use

Do not use for a new feature, research-only decision, or data analysis without
a software defect to reproduce.

## Workflow

1. Read `CONTEXT.md` when present and capture the exact symptom, environment, and expected behavior.
2. Reproduce the failure before changing code when possible.
3. Minimize the failure to the smallest useful case and identify the observed boundary.
4. Form evidence-based hypotheses and instrument only what helps distinguish them.
5. Apply the smallest safe root-cause fix.
6. Add or update a regression test at the agreed public seam.
7. Run the original reproduction and relevant boundary checks.
8. Review the change for correctness, regression risk, security, and maintainability.
9. Write diagnosis and handoff artifacts when requested or authorized.

## Decision rules

- Do not claim a root cause from a hypothesis without evidence.
- If reproduction is unavailable, document uncertainty and add observability before guessing.
- Refactoring is allowed only when it directly supports the verified fix.
- Do not broaden a bug fix into feature work without an explicit decision.
- A user-invoked workflow may read `both` skills but must not silently start another user workflow.

## Failure modes

- If the failure cannot be reproduced, report the missing conditions and the next observation needed.
- If hypotheses conflict, preserve the evidence and test one relevant variable at a time.
- If the fix passes the new test but not the original reproduction, do not report completion.
- If the regression surface is unclear, add boundary checks before handoff.

## Supporting resources

- [`CONTEXT.md` template](../../../templates/CONTEXT.md) — copy into a consumer project when shared context is missing.
- [`bug-diagnosis.md`](../../../templates/bug-diagnosis.md) — use for diagnosis output.
- [`code-review-report.md`](../../../templates/code-review-report.md) — use for review output.
- [`handoff.md`](../../../templates/handoff.md) — use for final handoff output.

## Expected output and validation

Provide the symptom, reproduction status, evidence, root cause, fix, regression
test, verification result, review result, unresolved risks, and next action.

## Agent handoff

- Selected when: The user requests diagnosis and repair of a software failure, regression, or unexpected behavior.
- Do not activate when: The task is a new feature, research decision, or data analysis without a software defect.
- Expected output: Verified fix, regression evidence, review result, and optional diagnosis/handoff artifacts.
- User-facing report: Summarize symptom, cause, fix, tests, checks, risks, and remaining uncertainty.
- Confirmation boundary: Confirm before destructive recovery, external actions, material scope expansion, or writing optional artifacts outside the agreed project layout.
