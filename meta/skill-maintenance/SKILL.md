---
name: skill-maintenance
description: Maintain an existing SKILLS library entry through focused changes, migrations, compatibility checks, or retirement.
category: meta
subject: skill-system
scope: repository
status: stable
version: 2.0.0
invocation: user
---

# Skill maintenance

## When to use

Use when an existing skill becomes stale, overlaps another skill, needs a
versioned change or migration, or should be merged, split, or retired. Include
the affected callers and repository metadata in the maintenance scope.

## When not to use

Do not use to create an initially accepted skill; use `meta/skill-authoring`.
Use `meta/skill-intake` to decide whether a new external or recurring capability
belongs in the library, `meta/skill-discovery` to select a skill for a task, and
`meta/skill-evaluation` to assess behavior. Do not use as domain implementation
guidance.

## Workflow

1. Inspect the skill, metadata, evaluation cases, links, dependent skills,
   registry entries, and all known callers.
2. Classify the issue: activation, scope, procedure, resource/reference,
   validation, compatibility, or lifecycle.
3. Define the smallest coherent target behavior and enumerate affected artifacts
   and consumers before editing.
4. Update callers, references, examples, cases, and generated metadata in the
   same migration; remove obsolete aliases or paths when the cutover is complete.
5. Bump the skill version when behavior or activation changes; document breaking
   migrations before removing old behavior.
6. Run structural validation and representative/boundary regression cases;
   inspect changed runtime behavior rather than treating metadata checks as proof.

## Decision rules

- Prefer a narrow correction over accumulating universal rules.
- Split only when the outcomes or activation conditions are genuinely independent.
- Merge only when outcomes, boundaries, and validation are the same; migrate all
  callers to the retained entry before removing the retired entry.
- Retire duplicated or unused skills when evidence supports retirement, not for
  aesthetics.
- Treat activation or expected-output changes as compatibility changes.
- Preserve unrelated user work. Ask before destructive deletion, publication,
  or irreversible lifecycle actions.

## Failure modes

- Stale reference: update or remove the link and validate local destinations.
- Routing drift: correct description and exclusions before procedure.
- Breaking change without migration: restore compatibility until callers migrate
  or document an approved clean cutover.
- Empty usage evidence: report uncertainty rather than claiming a skill is unused.

## Expected output and validation

Report the issue classification, affected callers/artifacts, version or migration
decision, validations exercised, and residual compatibility risk. Every
maintenance change must pass repository validation and at least one relevant
representative or regression case.

## Agent handoff

- Selected when: An existing skill needs a scoped change, caller migration, compatibility review, or lifecycle decision.
- Do not activate when: The task is initial skill authoring, new-capability intake, routine routing, evaluation-only, or domain implementation.
- Expected output: A scoped maintenance change with migrated callers, version decision, and observed checks.
- User-facing report: Name affected skills/callers, changes, validations, migration outcome, and remaining risk.
- Confirmation boundary: Ask before destructive deletion, external writes, publication, or irreversible lifecycle changes.
