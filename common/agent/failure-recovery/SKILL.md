---
name: failure-recovery
description: Recover safely from failed commands, tools, scripts, partial changes, and uncertain agent execution state.
category: common
subject: agent
scope: universal
status: stable
version: 1.0.0
invocation: both
---

# Failure recovery

## When to use
Use after a command, tool, test, integration, or multi-step operation fails or partially completes.

## Workflow
1. Capture the exact error, current state, and completed side effects.
2. Determine whether the failure is transient, environmental, input-related, or a logic defect.
3. Preserve recoverable work and choose the smallest safe next action.
4. Retry only when the operation is understood and idempotent or its effects are known.
5. Verify final state independently and report remaining uncertainty.

## Decision rules
- Do not repeat an unknown failure blindly.
- Stop before retries that could duplicate external or destructive side effects.

## Failure modes
If state cannot be determined, pause and request inspection or user guidance.

## Expected output
Report failure cause, preserved work, recovery action, verification, and blockers.

## Validation
The final state is inspected and no partial failure is presented as completion.
