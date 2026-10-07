---
name: skill-authoring
description: Create or revise a SKILLS library entrypoint by defining its user outcome, activation boundaries, procedure, and validation.
category: meta
subject: skill-system
scope: repository
status: stable
version: 2.0.0
invocation: user
---

# Skill authoring

## When to use

Use when creating a skill in this repository or changing an existing skill's
scope, procedure, activation boundary, supporting resources, or output contract.

## When not to use

Do not use this workflow just to choose a skill for a domain task; use
`meta/skill-discovery`. For an external source that may be adopted, adapted, or
rejected, use `meta/skill-intake` before authoring. To assess behavior without
editing the skill, use `meta/skill-evaluation` or `meta/skill-maintenance` for
the applicable review outcome. Do not substitute this workflow for domain
implementation guidance.

## Workflow

1. Define the user task, desired outcome, and nearest activation boundary.
2. Decide whether required knowledge belongs in `SKILL.md`, a linked reference,
   a deterministic script, an example, or an asset.
3. Write the smallest useful entrypoint using `meta/SKILL_TEMPLATE.md`; remove
   template sections that do not serve this skill's decision or procedure.
4. State decision rules, failure handling, expected output, and observable
   validation.
5. Run the repository validator and test representative and boundary cases.
6. Regenerate the registry and Markdown index after metadata changes.

## Decision rules

- Prefer one skill per coherent outcome, not one skill per technology keyword.
- Keep generic facts out unless they change an agent decision.
- Use references for conditional depth and scripts for deterministic repeated
  work.
- Make descriptions distinguish nearby skills and match the body boundaries.
- Keep runtime-specific behavior in adapters, not portable skill metadata.

## Constraints

Names use lowercase letters, digits, and hyphens. Do not create empty resource
directories or copy external documentation wholesale.

## Failure modes

- Vague description: narrow the trigger and name the nearest exclusion.
- Giant entrypoint: move conditional detail to a linked reference.
- No observable validation: specify a task artifact or deterministic check.
- Overlap with another skill: define distinct ownership or revise the existing
  skill rather than duplicating its procedure.

## Validation

Run `python3 scripts/validate_skills.py`, the relevant evaluation cases, and
`python3 scripts/generate_skill_index.py --check` from the repository root.

## Agent handoff

- Selected when: The requested outcome is creating or changing a skill's content, boundary, resources, or metadata in this repository.
- Do not activate when: The task only selects a skill, evaluates behavior without authoring, or implements a domain feature.
- Expected output: A reviewed skill entrypoint and the required linked resources, evaluation case, and generated registry updates.
- User-facing report: State the outcome and boundary encoded, files/resources changed, validation run, and remaining uncertainty.
- Confirmation boundary: Ask before destructive lifecycle changes, external publication, or copying content with unresolved license terms.
