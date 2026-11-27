# Workflow skills

Orchestrate narrow primitive skills around one user outcome. Workflow skills are user-invoked `invocation: user`, `scope: universal`. Not replacement for domain skills. Don't silently trigger another user-invoked workflow.

## Required contract

Every workflow defines:

- activation + exclusion;
- primitive skills read/recommended;
- decision points + optional branches;
- expected artifacts;
- confirmation before side effects;
- failure/recovery;
- terminal validation;
- agent handoff.

## Context + artifacts

Before starting read consumer `CONTEXT.md` when present. Artifact paths from its work-artifact section. Default consumer root:

```text
docs/agent/
├── specs/
├── diagnostics/
├── decisions/
├── reports/
└── handoffs/
```

Present intended artifact path before writing new document unless project already authorized output.

## Supported workflows

- `common/workflow/feature-delivery`: align, plan, implement vertical slices, test, review, handoff.
- `common/workflow/bug-fixing`: reproduce, minimize, hypothesize, fix, regression-test, review, handoff.
- `common/workflow/research-decision`: define decision, gather evidence, compare alternatives, record uncertainty.
- `common/workflow/data-analysis`: inspect, contract, clean, validate, analyze reproducibly, report limitations.

Keep workflow entrypoint concise; link shared artifact templates. No duplicate long formats.
