---
name: code-review
description: Review a code change for correctness, maintainability, security risk, regression risk, and test adequacy.
category: common
subject: engineering
scope: universal
status: experimental
version: 1.0.0
invocation: both
---

# Code review

## When to use
Use after an implementation exists and the requested outcome is an evidence-based review of its diff, patch, pull request, or final readiness before merging or handing off.

## When not to use
Do not use as the implementation workflow, and do not substitute it for a test plan when no change is ready to inspect.

## Workflow
1. Read the requested behavior and inspect the complete diff and surrounding code.
2. Check correctness, edge cases, compatibility, tests, security boundaries, documentation, and maintainability.
3. Identify breaking changes, residual risk, and handoff readiness.
4. Report actionable findings by severity with file/line evidence and a clear handoff recommendation.

## Decision rules
- Prioritize concrete defects and security/compatibility blockers over style preferences.
- Verify changed behavior instead of trusting a green unrelated test suite.
- Report no issue when the evidence supports correctness; do not invent concerns.
- Choose this skill when findings, severity, file-level evidence, or a handoff decision are the requested output.

## Failure modes
If context or tests are missing, state the review limitation explicitly.

## Expected output
Return actionable findings first, followed by residual risks and summary.

## Validation
Every finding has evidence, impact, and a clear remediation direction.

## Agent handoff

- Selected when: Use the activation boundary and outcome described in this skill.
- Do not activate when: The task matches the stated exclusion or a narrower skill.
- Expected output: Produce the observable result and validation described by the workflow.
- User-facing report: Summarize scope, result, checks, and unresolved risks.
- Confirmation boundary: Ask before destructive, external, or irreversible actions.
