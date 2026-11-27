---
name: repository-onboarding
description: Understand an unfamiliar repository before making changes by inspecting its structure, instructions, state, and entrypoints.
category: common
subject: foundation
scope: universal
status: stable
version: 1.0.0
invocation: both
---

# Repository onboarding

## When to use
Use at the start of work in an unfamiliar or recently changed repository.

## When not to use
Do not repeat a full onboarding pass when current project context is already verified.

## Workflow
1. Inspect top-level files and project documentation.
2. Read applicable agent instructions and contribution rules.
3. Check Git state, branch, remote, and recent changes.
4. Locate `CONTEXT.md` or equivalent project vocabulary, architecture, testing,
   issue-tracking, ADR, and artifact-path guidance.
5. Locate the relevant entrypoints, tests, configuration, and build commands.
6. Summarize findings, risks, artifact assumptions, and the smallest next step.

## Decision rules
- Trust repository evidence over assumptions.
- Read only files relevant to the requested task after the initial map.
- Preserve project-defined terminology and artifact paths when handing off to a
  workflow skill.

## Safety constraints
Preserve uncommitted work and do not modify files during inspection.

## Failure modes
If instructions, context, or entrypoints conflict, surface the conflict before
editing.

## Expected output
Return a concise repository map, relevant conventions, current state, and proposed scope.

## Validation
Confirm that the relevant files and commands were identified before proceeding.
