---
name: python
description: Apply Ryan's preferred workflow for maintainable Python backend services, tooling, and APIs.
category: personal
subject: engineering
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# Python backend

## When to use
Use for Python service, API, automation, or backend implementation work.

## When not to use
Do not add a framework or package without a concrete project need.

## Personal principles
Prefer clear modules, typed boundaries where useful, explicit configuration, and testable functions.

## Workflow
Inspect project tooling, define API/data contracts, implement a small path, test errors, and verify packaging/runtime behavior.

## Decision rules
Prefer standard library or existing project dependencies before introducing a new package.

## Constraints
Keep environment-specific settings out of source and secrets out of the repository.

## Failure modes
If packaging or runtime assumptions are unclear, inspect project metadata before editing.

## Expected output
Provide maintainable Python code, tests, configuration guidance, and verification.

## Validation
Formatting, lint/type checks where configured, tests, and documented startup pass.
