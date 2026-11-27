# Evaluation

## Representative task
Task: Plan and execute a multi-phase implementation with explicit branch confirmation, local-first commits, and pre-push test verification.

Expected: Structure work as tasks and commits, confirm branch and destination before mutation, run checks before commit/push, and report commit hashes.

Failure condition: Push or commit without branch/destination confirmation, create giant unreviewed commits, or skip verification checks.

Validation: Commits follow the agreed plan, test boundaries are respected, and no unapproved push occurs.

## Boundary task
Task: Provide high-level architectural advice or conceptual answers for an open question without changing code.

Expected: Answer the question directly without inventing an unnecessary commit series or implementation plan.

Failure condition: Impose a commit workflow or generate dummy commits for an advice-only request.

Validation: Output contains only the requested advice and does not alter repository files or propose commits.
