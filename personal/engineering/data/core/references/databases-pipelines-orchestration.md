# Databases, pipelines & orchestration reference

## Databases & storage
- Prefer the simplest storage that makes correctness and inspection easy.
- Define access patterns and data lifecycle, compare storage options, model schema, test representative queries, and include backup/migration/schema evolution.
- Do not introduce distributed storage for an unmeasured local workload.

## Pipelines
- Prefer observable, restartable, local-first pipelines before distributed systems.
- Define grain and contracts, inspect inputs, separate stages, persist checkpoints, validate outputs, and record lineage.
- Make idempotency and failure recovery explicit before scheduling; quarantine invalid records instead of silently dropping them.

## Orchestration
- Prefer simple explicit scheduling until operational complexity is justified.
- Do not hide a fragile script behind an orchestrator; fix its contract first.
- Retries must not duplicate unsafe side effects; surface failed task, partial outputs, and recovery action separately.
