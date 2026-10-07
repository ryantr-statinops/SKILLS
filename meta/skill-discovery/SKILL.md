---
name: skill-discovery
description: Route an uncategorized agent task to the narrowest SKILLS capability using activation boundaries and an installed catalog.
category: meta
subject: skill-system
scope: universal
status: stable
version: 2.0.0
invocation: both
---

# Skill discovery

## When to use

Use before implementation when an agent must choose one or more relevant skills
for a user outcome. This includes a consumer project with an installed skill
catalog as well as work inside the SKILLS repository.

## When not to use

Do not use this workflow to implement a domain task after the relevant skill has
already been selected. Follow that skill's procedure instead. For creating,
evaluating, importing, or maintaining library skills, use the corresponding
meta skill rather than treating routing as the whole task.

## Workflow

1. Extract the requested outcome, domain, artifacts, and risk.
2. Use the source repository index for repository work; use the installed
   `.skill-catalog.json` or runtime skill list for consumer work. Do not depend
   on an unavailable source checkout.
3. Scan descriptions and metadata; narrow candidates by outcome and scope.
4. Reject candidates whose activation exclusion applies.
5. Select the narrowest applicable skill; combine skills only for distinct
   responsibilities.
6. Report selected IDs, routing reasons, nearby rejected candidates, and
   resources to read.
7. Read selected `SKILL.md` files before following their procedures.

## Decision rules

- Specific scope beats broad scope; a technology mention alone is insufficient.
- User-outcome workflow skills are entry points; supporting skills do not
  silently replace their orchestration.
- If no skill clearly applies, say so and proceed without forcing an unrelated
  skill.
- If procedures conflict, surface the conflict instead of silently merging them.

## Failure modes

- Too many candidates: narrow by desired artifact and exclusions.
- Missing consumer catalog: use the runtime's available skill listing; if none
  is available, report the evidence limit rather than assuming source access.
- Missing project context that changes the route: inspect the repository first
  and request only information that cannot be discovered locally.

## Expected output and validation

Return the selected skill IDs, why they match the outcome, the nearest rejected
alternative and its boundary, and linked resources needed for execution. Confirm
the selected entrypoints exist in the chosen registry before activating them.

## Agent handoff

- Selected when: A task has not yet been routed to SKILLS capabilities and needs an outcome-based selection.
- Do not activate when: Domain implementation already has an applicable selected skill, or the task is authoring/evaluation/intake/maintenance of the library.
- Expected output: Skill IDs, routing rationale, exclusions, and required entrypoints/resources.
- User-facing report: State the chosen route, why alternatives were rejected, and the validation of registry entries.
- Confirmation boundary: Discovery is read-only. Ask before installing, removing, or otherwise mutating consumer skills.
