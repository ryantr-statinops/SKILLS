# Evaluation

## Representative task

Task: The user explicitly asks to supervise two Orca workers working on independent tasks, wait for their reports, process any questions, and provide a final evidence-based summary.

Expected: Select `personal/workflow/orca-orchestration`; resolve the Orca executable once; load `skills get orchestration` from that binary before lifecycle commands; use self-contained task specifications; follow the version-matched supervised loop; validate each result against its Dispatch; report per-task outcome and evidence.

Failure condition: Dispatch generic subagents instead of Orca, guess command syntax without loading the guide, or claim a timeout proves worker exit.

Validation: The selected Orca binary provides the guide, every expected Dispatch settles or is reported as unverifiable, and the final report names each outcome and evidence.

## Boundary task

Task: The user asks to hand ownership of one task to another agent/worktree but does not ask to monitor, wait for results, or coordinate a DAG.

Expected: Do not create an Orca Run or Dispatch under this skill. Route to the separately available Orca CLI handoff skill; if it is unavailable, state that prerequisite instead of inventing the handoff procedure.

Failure condition: Start a supervised orchestration loop or silently substitute a generic subagent handoff.

Validation: No orchestration lifecycle is started and the missing handoff capability is explicit if the separate skill is unavailable.
