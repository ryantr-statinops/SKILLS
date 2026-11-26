---
name: core
description: Design personal backend services around boundaries, contracts, persistence, security, failure behavior, testing, and operations.
category: personal
subject: backend
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# Backend foundations

Use this skill before choosing a backend language, framework, service boundary, or persistence strategy. The goal is an explicit, testable, observable service with a small operational surface.

## When to use

Use when a task involves service ownership, APIs, domain logic, persistence, authentication, asynchronous work, or backend operations. See [the API & service architecture reference](references/api-and-architecture.md) for detailed contract and boundary checklists. Route to narrower skills after the foundation is clear:

- `go`, `python`, or `nodejs` for runtime-specific implementation.
- `personal/engineering/core` for lower-level algorithm, systems, or performance trade-offs.

## Personal principles

- Prefer explicit contracts, simple components, observable failures, and testable behavior.
- Separate domain logic from transport, persistence, and infrastructure concerns.
- Make side effects, ownership, consistency, and authorization explicit.
- Start with the smallest vertical path that proves the service boundary.

## Foundation workflow

1. Define the user outcome, consumers, service owner, and system boundary.
2. Specify inputs, outputs, validation, errors, compatibility, and side effects.
3. Separate domain logic from transport, persistence, queues, and external integrations.
4. Define persistence model, transaction/consistency needs, indexes, and migration risks.
5. Define authentication, authorization, sensitive data, secrets, and trust boundaries.
6. Decide synchronous versus asynchronous work, retries, timeouts, and idempotency.
7. Define configuration, health checks, logs, metrics, traces, and operational ownership.
8. Implement a thin vertical path and test both the happy path and failure boundaries.
9. Document deployment, rollback, scaling assumptions, and unresolved risks.

## Core concerns

Reason explicitly about:

- API/protocol boundaries and version compatibility.
- Domain invariants and validation ownership.
- Persistence, transactions, consistency, caching, and migrations.
- Authentication, authorization, input validation, and sensitive output.
- Queues, background jobs, concurrency, timeouts, retries, and idempotency.
- Configuration, secrets, health, logging, metrics, tracing, and alerts.
- Testing at domain, service, integration, and contract boundaries.
- Deployment, reliability, scaling, cost, and recovery.

## Decision rules

- Do not select a framework before the service boundary and contract are clear.
- Do not expose internal persistence models as public contracts by accident.
- Do not retry non-idempotent side effects without an explicit safety design.
- Do not treat authentication as authorization or authorization as input validation.
- Do not hide dependency, timeout, configuration, or queue failures as generic errors.
- Do not add a service split, cache, queue, or distributed component without a workload or ownership reason.

## Constraints

Keep secrets out of source and images. Make side effects explicit, minimize sensitive output, preserve compatibility expectations, and require deliberate approval for destructive or external actions.

## Failure modes

Stop or narrow the implementation when:

- Contract, consumer, ownership, or consistency needs are unclear.
- Security boundaries or side effects are unspecified.
- Failure behavior cannot be observed or tested.
- A retry or async design can duplicate work without an idempotency plan.
- Operational requirements are being deferred until after deployment.

## Expected output

Provide service boundaries, contracts, persistence and consistency decisions, security boundaries, failure behavior, test strategy, operational checks, risks, and a minimal implementation path.

## Validation

The service has a testable boundary, documented failure behavior, observable health and errors, explicit side effects, and a deployment/recovery verification path.

## Agent handoff

- Selected when: Use when the requested outcome matches this skill description and workflow.
- Do not activate when: Do not activate when the task matches the stated exclusion or a narrower skill.
- Expected output: Produce the observable artifact, decision, or result described by the workflow.
- User-facing report: Summarize scope, result, checks, and unresolved risks.
- Confirmation boundary: Ask before destructive, external, or irreversible actions.
