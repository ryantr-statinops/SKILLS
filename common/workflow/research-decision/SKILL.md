---
name: research-decision
description: Turn a research question into an evidence-backed decision by defining criteria, comparing alternatives, and recording uncertainty.
category: common
subject: workflow
scope: universal
status: stable
version: 1.1.0
invocation: user
requires: [common/research/research]
---

# Research decision

## When to use

Use when the user needs evidence to choose among technical or operational
alternatives and the decision should remain inspectable after the conversation.

## When not to use

Do not use for implementation planning without an open decision, casual factual
questions, or personal preference decisions that need no external evidence.

## Workflow

1. Read `CONTEXT.md` when present and define the question, scope, and decision owner.
2. State the decision the research will inform and the criteria for choosing.
3. Identify high-trust primary sources and date-sensitive claims.
4. Gather evidence while separating facts, source-supported claims, inferences, and uncertainty.
5. Compare alternatives against the agreed criteria rather than listing features.
6. Recommend an option with explicit trade-offs and implementation implications.
7. Record unresolved uncertainty, evidence gaps, and follow-up work.
8. Produce the cited decision artifact and handoff when requested or authorized.

## Decision rules

- Do not present an inference as a sourced fact.
- Prefer primary and authoritative sources for technical or high-stakes claims.
- Match research depth to the decision cost and uncertainty.
- Reject alternatives that fail a stated hard constraint before scoring soft preferences.
- Do not declare a universal winner without a defined context; penalize operational complexity, lock-in, and unverified assumptions.
- A user-invoked workflow may read `both` skills but must not silently start another user workflow.

## Failure modes

- If the question is not decision-shaped, reframe it or route to a narrower research skill.
- If evidence conflicts, show the conflict and explain which source properties affect confidence.
- If current information cannot be verified, state the date boundary and residual uncertainty.
- If criteria are missing, pause before recommending an option.

## Supporting resources

- [`CONTEXT.md` template](../../../templates/CONTEXT.md) — copy into a consumer project when shared context is missing.
- [`research-decision.md`](../../../templates/research-decision.md) — use for the cited decision artifact.
- [`handoff.md`](../../../templates/handoff.md) — use for final handoff output.

## Expected output and validation

Provide the question, decision, criteria, sources, comparison, recommendation,
trade-offs, fact/inference distinctions, uncertainty, and follow-up. Validate
source links, dates, claim scope, and inference labels.

## Agent handoff

- Selected when: The user needs research that will inform a technical or operational choice among alternatives.
- Do not activate when: There is no open decision, the task is implementation-only, or the question is a simple factual lookup.
- Expected output: Cited decision artifact with comparison, recommendation, uncertainty, and follow-up.
- User-facing report: Summarize scope, evidence, recommendation, trade-offs, confidence, and unresolved questions.
- Confirmation boundary: Confirm before external submissions, paid research, or writing optional artifacts outside the agreed project layout.
