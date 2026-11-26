---
name: data-analysis
description: Structure a data analysis from inspection and data contracts through traceable cleaning, validation, reproducible analysis, and reporting.
category: common
subject: workflow
scope: universal
status: stable
version: 1.1.0
invocation: user
---

# Data analysis

## When to use

Use when the user needs an inspectable analysis that transforms data, answers a
question, and reports assumptions, validation, reproducibility, and limitations.

## When not to use

Do not use for a simple lookup, an application bug without a data-analysis
question, or an unbounded request to produce a chart without defining inputs
and interpretation.

## Workflow

1. Read `CONTEXT.md` when present and define the question, intended decision, and output.
2. Inspect input shape, schema, quality, distributions, time semantics, and provenance before transforming.
3. Define the data contract, including fields, types, keys, nullability, and allowed values.
4. Clean invalid, duplicate, missing, or inconsistent records while preserving traceability and assumptions.
5. Validate the cleaned data and reject incompatible inputs rather than hiding violations.
6. Run a reproducible analysis with explicit inputs, transformations, parameters, and outputs.
7. Report results, validation evidence, uncertainty, assumptions, and limitations.
8. Write the analysis report and handoff artifacts when requested or authorized.

## Decision rules

- Inspect before transforming; do not infer quality from a successful load.
- Separate data preparation from analysis results.
- Preserve the original input or an auditable source reference.
- Treat schema changes and missingness as compatibility decisions.
- Do not claim causality from descriptive or observational analysis without appropriate evidence.
- A user-invoked workflow may read `both` skills but must not silently start another user workflow.

## Failure modes

- If the input or data contract is missing, stop before producing a result.
- If invalid data cannot be resolved without an assumption, report the assumption and its impact.
- If the analysis cannot be reproduced, report the missing command, parameter, or environment detail.
- If distributions or validation reveal a material issue, revise the analysis rather than hiding it.

## Supporting resources

- [`data-checklist.md`](references/data-checklist.md) — detailed inspection, schema validation, cleaning, and reproducibility checklists.
- [`CONTEXT.md` template](../../../templates/CONTEXT.md) — copy into a consumer project when shared context is missing.
- [`data-analysis-report.md`](../../../templates/data-analysis-report.md) — use for analysis output.
- [`handoff.md`](../../../templates/handoff.md) — use for final handoff output.

## Expected output and validation

Provide the question, input contract, transformations, reproduction path,
results, validation status, assumptions, uncertainty, limitations, and next
action. Validate schema, quality checks, reproducibility, and output provenance.

## Agent handoff

- Selected when: The user requests an inspectable data analysis with explicit inputs, transformations, results, and limitations.
- Do not activate when: The task is a simple lookup, an application bug, or chart formatting without an analysis question.
- Expected output: Reproducible analysis report with data contract, validation, results, and limitations.
- User-facing report: Summarize inputs, transformations, findings, checks, assumptions, uncertainty, and follow-up.
- Confirmation boundary: Confirm before external data access, destructive transformations, or writing optional artifacts outside the agreed project layout.
