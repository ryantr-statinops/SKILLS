---
name: core
description: Analyze and improve software systems using computational thinking, complexity, measurement, and explicit engineering trade-offs before choosing an implementation.
category: personal
subject: engineering
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# Engineering foundations

Use this skill as the shared foundation for personal data, AI, and backend engineering work. It focuses on how to reason about computation and systems, not on a particular language, framework, or product domain.

## When to use

Use before selecting an algorithm, data structure, system boundary, runtime, or optimization strategy when the decision depends on workload, correctness, performance, reliability, or future change cost.

## Computational thinking

- Define the problem, inputs, outputs, invariants, and acceptance criteria.
- Separate correctness, performance, maintainability, security, and operability concerns.
- Make workload and environmental constraints explicit before choosing a solution.
- Compare at least the simplest viable approach with any more complex alternative.

## Algorithms and data structures

Reason about time and space complexity, but also account for allocation, cache behavior, I/O, serialization, contention, and operational complexity. Choose arrays, maps, trees, heaps, queues, graphs, indexes, sorting, caching, precomputation, streaming, or materialization according to the access pattern and workload rather than habit.

## Optimization workflow

```text
Define workload
→ Measure baseline
→ Identify bottleneck
→ Form hypothesis
→ Change the smallest relevant part
→ Benchmark
→ Verify correctness
→ Compare trade-offs
```

Do not optimize from intuition alone or treat a better asymptotic bound as sufficient evidence. Preserve a correctness check and record the workload, measurement method, and environmental assumptions.

## Systems foundations

Use the following concepts as shared foundations:

- Processes, threads, concurrency, and parallelism.
- Memory, persistence, filesystems, and resource limits.
- Networking, HTTP, RPC, and failure boundaries.
- Databases, storage, consistency, and durability.
- Testing, debugging, observability, reliability, and security.

## Decision framework

Compare candidate approaches using:

- Correctness and invariant preservation.
- Complexity and cognitive load.
- Measured performance and resource use.
- Reliability and failure recovery.
- Security and access boundaries.
- Operational simplicity and cost.
- Future change cost.

## Boundaries

Do not use this skill for detailed ETL or warehouse design, model training, framework-specific API implementation, language syntax, trading strategies, or deep statistical derivations. Route those requests to the relevant data, AI, backend, statistics, or quant skill after using this foundation when appropriate.

## Expected output

Provide a problem model, workload and constraints, candidate solutions, complexity and performance risks, a recommendation, a measurement/validation plan, and explicit trade-offs.

## Validation

The selected approach has a stated correctness check, a baseline or measurable rationale, and a verification path appropriate to the risk.
