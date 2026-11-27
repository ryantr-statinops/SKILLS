---
name: context-management
description: Load only the context needed for a task while preserving the evidence required for correct decisions.
category: common
subject: foundation
scope: universal
status: stable
version: 1.0.0
invocation: both
---

# Context management

## When to use
Use when a repository, specification, or task spans more files, skills, references, or tools than the current work requires.

## Workflow
1. Identify the requested outcome and relevant subsystem.
2. Read `CONTEXT.md` when present, especially its vocabulary, architecture boundaries, test seams, constraints, and artifact paths.
3. Read entrypoints, instructions, schemas, and tests before deep implementation files.
4. Select the narrowest relevant skill and load conditional resources only when a decision requires them.
5. Keep a concise evidence summary and discard unrelated detail.
6. Re-check source files when assumptions become uncertain.

## Decision rules
- Prefer primary project artifacts over summaries.
- Do not load an entire category when one skill answers the task.
- Expand context only in response to a concrete unknown or failure.
- Treat project-defined artifact paths as the source of truth; when they are
  absent, use `docs/agent/` with `specs/`, `diagnostics/`, `decisions/`,
  `reports/`, and `handoffs/` subdirectories.

## Failure modes
If context is insufficient, state exactly which artifact or decision is missing.
If `CONTEXT.md` is absent, continue with repository evidence and report the
default assumptions used for artifact paths and terminology.

## Expected output
Maintain a task-focused context map rather than a repository dump.

## Validation
Confirm that each loaded artifact supports a stated decision or verification step.
