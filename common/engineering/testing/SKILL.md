---
name: testing
description: Design, run, and evaluate tests that verify intended behavior, boundaries, and regression risk.
category: common
subject: engineering
scope: universal
status: experimental
version: 1.0.0
invocation: both
---

# Testing

## When to use
Use when a behavior or contract needs deliberate coverage, including success, boundary, invalid, or regression cases.

## When not to use
Do not use as the primary route for finding an unknown root cause; use `debugging`. Do not use it to coordinate a multi-step feature; use the delivery workflow and load this skill for its test step.

## Workflow
1. Identify the behavior and its public contract.
2. Choose focused unit, integration, or end-to-end coverage.
3. Cover success, boundary, invalid, and failure cases.
4. Run the smallest relevant checks, then the broader suite when justified.
5. Investigate failures instead of weakening assertions.

## Decision rules
- Test observable behavior rather than implementation details.
- Prefer deterministic, fast tests for repeated feedback.
- Choose this skill when the requested outcome includes a test plan, test changes, or an explicit coverage decision.

## Failure modes
Do not report success when tests were skipped, flaky, or unrelated to the changed behavior.

## Expected output
Report tests run, results, coverage of risk, and known limitations.

## Validation
The new or changed behavior has a passing test and an appropriate boundary case.
