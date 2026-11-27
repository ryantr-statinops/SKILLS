---
name: production-workflow
description: Turn a validated quantitative research artifact into a reproducible, observable, recoverable production engineering workflow without authorizing trade execution.
category: personal
subject: quant
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# Quant production workflow

Use this skill when a research result needs to become a reliable data, model, batch, or service workflow. A good backtest is evidence for a research hypothesis, not proof that a production system is ready.

## Production-readiness sequence

```text
Research artifact handoff
→ Data freshness and contract
→ Reproducible feature/run generation
→ Deployment boundary
→ Monitoring and alerting
→ Failure recovery and rollback
→ Human approval and risk gate
```

## Workflow

1. Identify the validated research artifact, version, assumptions, baseline, and known limitations.
2. Define input ownership, data freshness, availability timestamps, feature generation, and quality checks.
3. Version datasets, features, code, configuration, model, and evaluation artifacts sufficiently to reproduce a run.
4. Choose batch or online execution from latency, freshness, reliability, and operational needs.
5. Define configuration, secrets, environment, dependencies, and deployment/release boundaries.
6. Add monitoring for data freshness, schema/quality, drift, performance degradation, latency, cost, and failures.
7. Define retries, idempotency, checkpoints, dead-letter/manual-review paths, rollback, and recovery verification.
8. Add human approval and risk gates before any externally consequential decision or side effect.
9. Document ownership, runbook, audit trail, and the conditions that stop or roll back the workflow.

## Engineering connections

- Use `personal/engineering/data` for ingestion, contracts, lineage, quality, storage, and orchestration.
- Use `personal/engineering/ai` for model/inference, evaluation regression, and AI-specific monitoring.
- Use `personal/engineering/backend` for service/API, queues, authentication, and operational boundaries.
- Use `personal/engineering/core` for performance, concurrency, reliability, and system trade-offs.
- Use `personal/statistics` for uncertainty, diagnostics, drift interpretation, and time-aware evaluation.

## Decision rules

- Do not promote a research artifact without versioned inputs, reproducible runs, and explicit limitations.
- Do not call a workflow production-ready without freshness, quality, observability, and recovery checks.
- Prefer the simplest batch or scheduled workflow that meets freshness and reliability needs.
- Make stale data, schema changes, drift, degraded performance, and missing dependencies fail visibly.
- Separate system readiness from financial or business approval.
- Require explicit human authorization for externally consequential actions.

## Failure modes

Stop or route for review when:

- Research assumptions or artifact versions cannot be reproduced.
- Data freshness, timestamp semantics, or feature availability is unknown.
- Monitoring cannot distinguish data, model, infrastructure, and downstream failures.
- Retry or rollback can duplicate or conceal consequential work.
- The requested workflow crosses into automatic account/order execution.

## Expected output

Provide the research handoff, data and feature contract, versioning plan, batch/online choice, deployment boundary, monitoring, failure/recovery plan, audit trail, risk gate, human approval point, and unresolved production risks.

## Validation

The workflow is reproducible, data freshness and quality are observable, failures are recoverable or fail closed, deployment and rollback are explicit, and no external execution occurs without separate human authorization.
