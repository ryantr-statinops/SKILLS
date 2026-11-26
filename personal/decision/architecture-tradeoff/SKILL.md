---
name: architecture-tradeoff
description: Select technologies, review architecture fit, and evaluate trade-offs for personal systems across simplicity, performance, reliability, cost, and changeability.
category: personal
subject: decision
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# Architecture trade-offs

## When to use
Use when choosing a language, framework, database, or architecture option, or reviewing an existing architecture for fit, simplicity, and future change cost.

## Personal principles
Prefer understandable, inspectable, reversible decisions and visible operational complexity maintainable by one person.

## Workflow
1. State the decision, workload, constraints, and weighted criteria.
2. Map components, data flow, failure modes, ownership, lock-in, and learning cost.
3. Compare viable candidates and short-term vs long-term maintenance costs.
4. Choose a default, record rationale, and define a revisit trigger.

## Decision rules
Do not choose popularity as a substitute for fit; do not introduce distributed infrastructure or optimize for hypothetical scale over current learning.

## Constraints
Include maintenance, operations, and debugging cost, not only performance; separate current requirements from speculative scale.

## Failure modes
If trade-offs cannot be measured, propose a bounded experiment.

## Expected output
Return options, trade-off matrix, decision, risks, and revisit conditions.

## Validation
The chosen design has an explicit reason and a way to detect when it no longer fits.

## Agent handoff

- Selected when: Use when the requested outcome matches this skill description and workflow.
- Do not activate when: Do not activate when the task matches the stated exclusion or a narrower skill.
- Expected output: Produce the observable artifact, decision, or result described by the workflow.
- User-facing report: Summarize scope, result, checks, and unresolved risks.
- Confirmation boundary: Ask before destructive, external, or irreversible actions.
