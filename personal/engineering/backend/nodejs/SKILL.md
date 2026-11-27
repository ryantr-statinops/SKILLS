---
name: nodejs
description: Apply personal Node.js backend practices for APIs, services, runtime configuration, testing, and operations.
category: personal
subject: backend
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# Node.js backend

## When to use
Use for Node.js service, API, automation, or backend implementation work.

## Personal principles
Prefer explicit boundaries, typed contracts where useful, small modules, and observable async behavior.

## Workflow
Inspect package/runtime conventions, define contracts, implement a thin path, handle async errors, test boundaries, and verify startup/build.

## Decision rules
Prefer existing project tooling before introducing a framework or package.

## Constraints
Keep environment configuration and secrets outside source and images.

## Failure modes
Distinguish application, dependency, event-loop, network, and configuration failures.

## Expected output
Provide maintainable Node.js code, tests, configuration, and run instructions.

## Validation
Install, lint/type-check where configured, test, and documented startup pass.
