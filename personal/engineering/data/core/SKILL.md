---
name: core
description: Apply personal data engineering foundations for contracts, lineage, quality, storage, reproducibility, and recoverable workflows.
category: personal
subject: data
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# Data engineering foundations

Use this skill to design the data lifecycle before selecting a pipeline framework, database, warehouse, or scheduler. The goal is trustworthy, inspectable, rerunnable data rather than infrastructure for its own sake.

## When to use

Use when a task involves the meaning, ownership, movement, quality, storage, or operational recovery of data. See [the storage, pipelines & orchestration reference](references/databases-pipelines-orchestration.md) for detailed checklists. Route to `personal/statistics` for deeper probability, inference, regression, or time-series reasoning.

## Personal principles

- Prefer inspectable local-first systems until workload and operational requirements justify more infrastructure.
- Define data semantics and ownership before selecting tools.
- Preserve source data and make transformations, checkpoints, and failures visible.
- Treat data quality as a measurable contract, not a final manual check.
- Make reruns, recovery, and lineage part of the design.

## Foundation workflow

1. Define the business or analytical question, grain, unit of observation, and output.
2. Identify source ownership, freshness, timestamps, retention, and access boundaries.
3. Inspect source shape, schema, missingness, duplicates, outliers, and distribution risks.
4. Specify the data contract: fields, types, nullability, keys, allowed values, time semantics, and compatibility policy.
5. Define quality checks for completeness, uniqueness, validity, consistency, freshness, and volume.
6. Map lineage from source through transformations to consumers.
7. Choose storage and processing patterns from workload, consistency, scale, cost, and recovery needs.
8. Design checkpoints, idempotency, rerun behavior, failure handling, and observability.
9. Validate with representative data and document assumptions and known limitations.

## Core concepts

Reason explicitly about:

- Batch versus streaming and bounded versus unbounded inputs.
- Full refresh versus incremental processing.
- Idempotency, checkpoints, late data, and backfills.
- Schema evolution and compatibility.
- Data freshness and downstream service-level expectations.
- Lineage, ownership, metadata, and auditability.
- Storage durability, access patterns, partitioning, and cost.
- Recovery point, recovery time, and safe failure behavior.

## Statistical data-quality connections

Use statistical ideas at the application level without turning this skill into a statistics textbook. Check for missingness, duplicates, outliers, sampling bias, measurement quality, label leakage, and distribution shift when they affect downstream decisions. State when a quality check is a heuristic rather than proof of correctness.

## Decision rules

- Do not introduce distributed infrastructure before measuring workload, data volume, latency, concurrency, and operational needs.
- Do not transform data before its grain, ownership, and timestamp semantics are understood.
- Do not overwrite raw source data when preservation is feasible.
- Do not call a workflow reliable unless rerun and recovery behavior are specified.
- Do not hide quality failures behind silent coercion, dropped records, or undocumented defaults.

## Failure modes

Stop or narrow the scope when:

- Data semantics, ownership, or timestamp meaning is unclear.
- The source contract is missing or incompatible.
- Quality failures cannot be measured or traced to affected outputs.
- A transformation is not idempotent and no safe recovery path exists.
- Storage or infrastructure is being selected from fashion rather than workload.

## Expected output

Provide a data contract, source and consumer ownership, data flow and lineage, quality checks, storage/processing rationale, rerun and recovery path, observability plan, and unresolved assumptions.

## Validation

The workflow is rerunnable, source data is preserved or its loss is explicitly justified, output quality can be measured, lineage is inspectable, and failure behavior is observable.
