## Representative task

Task: Retire a duplicated skill whose callers still reference its old name.

Expected: Inspect callers, registry entries, links, and evaluation cases; migrate
each known caller to the retained skill, update generated metadata and regression
coverage, then remove the obsolete entry only after the cutover is complete.
Report version and compatibility decisions.

Failure condition: Delete the old entry before migrating callers, leave a stale
link/alias, or claim retirement is safe based only on an empty search result.

Validation: Show old-name references are gone from active callers, generated
registry/index checks pass, and representative/boundary cases for the retained
skill pass.

## Boundary task

Task: Create a first draft of a new skill entrypoint and its activation
boundaries.

Expected: Route to `meta/skill-authoring`; maintenance applies only after the
entry is accepted and changes are needed.

Failure condition: Apply lifecycle/versioning steps to an initial draft or alter
unrelated skills without evidence.

Validation: Confirm authoring owns the task and no unrelated lifecycle change is
made.