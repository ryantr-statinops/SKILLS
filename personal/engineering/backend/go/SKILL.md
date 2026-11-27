---
name: go
description: Apply Ryan's preferred workflow for designing, implementing, testing, and operating Go backend services.
category: personal
subject: engineering
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# Go backend

## When to use
Use for Go service design or implementation in personal workflows.

## When not to use
Do not impose Go when the project requirements favor another runtime.

## Personal principles
Prefer explicit packages, simple interfaces, standard tooling, and observable behavior.

## Workflow
Define contracts, inspect existing conventions, implement a thin vertical path, test boundaries, and verify build/runtime behavior.

## Decision rules
Avoid abstraction before a second concrete use case exists.

## Constraints
Keep dependency and concurrency choices explainable.

## Failure modes
If performance or concurrency is assumed, measure or state the assumption.

## Expected output
Provide maintainable Go code, tests, and operational notes.

## Validation
Formatting, tests, static checks, and build pass for the target environment.
