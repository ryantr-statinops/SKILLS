## Representative task

Task: Assess a changed engineering skill using its representative task and
boundary task before approving the revision.

Expected: Inspect the entrypoint and cases, run available static checks and
local task exercises, compare observed artifacts with expected behavior, and
report evidence limits separately from conclusions.

Failure condition: Treat validator success as proof of agent behavior, omit the
boundary case, or recommend promotion without observed evidence.

Validation: Produce a per-case pass/fail record with artifacts, checks, runtime
when exercised, concrete failures, and unresolved uncertainty.

## Boundary task

Task: Create a new skill entrypoint and define its activation boundaries.

Expected: Route to skill authoring; use evaluation only after a reviewable
entrypoint and expected behavior exist.

Failure condition: Substitute evaluation for authoring or claim that a static
contract check tested a skill's runtime behavior.

Validation: Confirm the authoring outcome owns the task and no behavioral
quality claim is made without observed task output.