## Representative task

Task: In a consumer project with an installed `.skill-catalog.json`, route a
request to deliver a feature before implementation begins.

Expected: Select `common/workflow/feature-delivery`, name its relevant supporting
skills and nearby exclusions, and list only resources needed to start.

Failure condition: Choose an unrelated skill, load the whole library, omit the
consumer catalog, or begin implementing the feature during routing.

Validation: Confirm every selected ID exists in the installed catalog and explain
why a nearby domain implementation skill is not the workflow entry point.

## Boundary task

Task: The user has already selected `common/engineering/testing` and asks to add
a regression test for an existing feature.

Expected: Exclude repository-level skill discovery and follow the selected
engineering skill's procedure.

Failure condition: Re-run catalog routing as a substitute for implementation or
activate the skill-library authoring workflow.

Validation: Confirm the selected engineering skill owns the work and discovery
does not emit an alternative implementation procedure.
