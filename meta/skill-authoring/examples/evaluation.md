## Representative task

Task: A repeated project workflow needs a reusable skill. Define its user
outcome, activation boundary, expected artifact, and validation before authoring.

Expected: Produce a narrow skill entrypoint with a concrete trigger and nearest
exclusion; place conditional detail in linked resources and provide observable
representative and boundary cases.

Failure condition: Create a topic-only skill, copy generic documentation, omit
an exclusion, or claim quality without a task-specific validation signal.

Validation: Check the entrypoint metadata, activation and exclusion, resource
links, evaluation cases, and generated registry with repository validation.

## Boundary task

Task: Implement an API endpoint using an already selected backend skill.

Expected: Follow the selected backend skill; do not invoke skill authoring.

Failure condition: Create or rewrite a library skill instead of implementing
the requested endpoint.

Validation: Confirm the selected backend skill owns the procedure and no new
library skill or metadata change was needed for the implementation task.