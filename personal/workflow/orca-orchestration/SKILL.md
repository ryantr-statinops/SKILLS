---
name: orca-orchestration
description: Coordinate supervised Orca workers when a user asks to dispatch, monitor, wait for, or manage a task DAG; requires the Orca runtime and its version-matched orchestration guide.
category: personal
subject: workflow
scope: personal
status: experimental
version: 1.0.0
invocation: user
---

# Orca orchestration

## When to use

Use when the user explicitly asks to supervise Orca workers, track their progress, wait for results, coordinate a task DAG, or process Orca questions and completion messages.

## When not to use

Do not use for ordinary implementation work, shell or terminal control, worktree management, or a one-way ownership handoff without supervision. Use the separately available Orca CLI skill for an explicit handoff; if it is unavailable, do not invent its workflow. Do not use generic subagents as a substitute when the user requests Orca coordination.

## Scope and prerequisites

This is a personal, Orca-specific workflow. It requires a working Orca installation, its CLI, and the matching runtime guide. The upstream skill at [stablyai/orca](https://github.com/stablyai/orca/tree/main/skills/orchestration) is the source for Orca-specific behavior; this skill provides local routing and safety boundaries, not a copy of the full runtime manual.

Before lifecycle commands, resolve the executable once for this session:

- Use `ORCA_CLI_COMMAND` when set.
- Otherwise use `orca-dev` when `ORCA_DEV_REPO_ROOT` identifies an Orca development checkout.
- Otherwise, on Linux outside an Orca-managed terminal, use `orca-ide`; do not run bare `orca`, which may resolve to the GNOME screen reader.
- Otherwise use `orca`.

Keep using that executable throughout the run. Do not switch to another build after an error, because that could target a different runtime.

## Workflow

1. **Classify the role.** Act as coordinator only for an explicit supervised request. If the live prompt contains Orca Task and Dispatch IDs, follow the dispatched-worker contract. For ordinary terminal work or a handoff-only request, do not create a supervised Run or Dispatch.
2. **Load the authoritative guide.** Run `<resolved-cli> skills get orchestration` before Orca commands. Prefer JSON output and consult only the version-matched reference named by a conditional gate. If `skills get` is unsupported, report that exact limitation; do not guess command syntax.
3. **Confirm runtime state and authority.** Follow the loaded guide for startup, access-denied, remote placement, and recovery. Preserve exact Run, Task, Dispatch, executable, and terminal identifiers from runtime receipts or the live worker preamble. Never reconstruct identifiers or broaden worker arguments.
4. **Specify work before dispatch.** Each task names its target, concrete change, constraints, ownership boundary, and observable acceptance evidence. Use dependencies only for real ordering; dispatch independent work in parallel only when workers will not conflict on shared files or state.
5. **Run the supervised loop from the guide.** Process each delivered question, escalation, and completion report before acknowledging its delivery. Validate each report against the expected active Dispatch and act on its reported outcome, not prose alone.
6. **Settle ownership safely.** A timeout, empty wait, missing terminal, or unverifiable liveness is not proof that a worker exited. Do not stop, abandon, retry, duplicate, or release work without the positive evidence and accepted settlement required by the guide.
7. **Report to the user.** For each task, report its outcome, evidence, and unresolved blocker. State unknown or unverifiable when runtime evidence does not establish a result.

## Decision rules

- Orca lifecycle operations require an explicit supervised request or a live Orca worker preamble.
- The installed binary's version-matched guide is authoritative for command syntax and lifecycle transitions; this skill is not a substitute for it.
- If a runtime operation requires permissions or external side effects beyond the user's authorization, stop at that boundary and request approval; never silently escalate.
- Preserve worker ownership and existing work on any uncertainty. Absence of evidence is not evidence of process exit.

## Failure modes

- **Orca unavailable:** report the executable-resolution or runtime error and stop; never fall back to a generic subagent when Orca provenance was requested.
- **Guide unavailable or CLI syntax differs:** report the exact error. Do not guess flags or use another Orca binary.
- **Timeout or lost contact:** treat it as a checkpoint; use only the recovery path and positive exit evidence from the matching guide.
- **Handoff requested without monitoring:** route to the separate Orca CLI skill when installed; do not create a Run or monitor completion under this skill.

## Expected output and validation

Complete only when every expected Dispatch has a settled, validated outcome, each delivered message has been processed, and the user receives a per-task result with evidence and unresolved blockers. When the runtime cannot prove settlement, report the state as unknown or unverifiable instead of claiming completion.

## Source attribution

Adapted from the Orca orchestration skill by Lovecast Inc. See [the upstream skill](https://github.com/stablyai/orca/blob/main/skills/orchestration/SKILL.md) and the included [MIT license notice](references/orca-license.md). The current Orca binary serves the authoritative, version-matched operational guide.

## Agent handoff

- Selected when: The user explicitly asks to supervise Orca workers, wait for results, monitor progress, or coordinate an Orca task DAG.
- Do not activate when: The user asks for ordinary coding, generic subagent use, terminal/worktree work, or a handoff without Orca supervision.
- Expected output: Settled Orca task outcomes with evidence and explicit unresolved blockers.
- User-facing report: Summarize per-task outcomes, evidence, worker state, and any unknowns.
- Confirmation boundary: Obtain approval before permission escalation or external/destructive lifecycle actions not already authorized by the user.
