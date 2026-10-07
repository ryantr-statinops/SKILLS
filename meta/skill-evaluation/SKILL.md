---
name: skill-evaluation
description: Assess a new or changed SKILLS entry for routing, procedure, safety boundaries, observable outcomes, and regression evidence.
category: meta
subject: skill-system
scope: repository
status: stable
version: 2.0.0
invocation: both
---

# Skill evaluation

## When to use

Use to assess a new or changed skill, diagnose weak behavior, or decide whether
evidence supports promoting a skill. Evaluate the skill's stated representative
and boundary tasks rather than relying on its prose alone.

## When not to use

Do not use this workflow to author or restructure the skill; use
`meta/skill-authoring`. For duplicated, stale, or lifecycle issues use
`meta/skill-maintenance`. For routing a domain task to an installed skill use
`meta/skill-discovery`. This workflow does not implement domain tasks or publish
a release.

## Workflow

1. Read the skill entrypoint, its evaluation cases, and only the linked context
   needed to judge them.
2. Confirm each case has a representative or boundary task, observable expected
   output, failure condition, and validation signal.
3. Run the task with the skill available; inspect the artifact, decisions,
   failure handling, resource use, and safety boundary.
4. Separate static contract checks from observed runtime behavior. Record the
   runtime/version and limits of the evidence; do not infer reasoning quality
   from structural validation.
5. Record a narrow change request for each concrete failure.
6. After changes, rerun the representative and boundary tasks and compare the
   observable outcomes.

## Quality checklist

- The description activates for the intended outcome and excludes nearby work.
- The procedure is actionable, bounded, and does not duplicate generic facts.
- References are loaded only when they affect the evaluated task.
- Scripts, if present, are deterministic and their failures are observable.
- Expected artifacts, failure behavior, and validation are externally checkable.
- Safety boundaries lead to safe behavior in both representative and boundary
  cases.

## Evaluation levels

- **Static:** structure, metadata, resources, and validator results.
- **Behavioral:** observed output from representative and boundary tasks in a
  named runtime.
- **Regression:** repeat prior cases after a skill change and compare artifacts.

Agent-based evaluation is optional. Use it only when independent behavior
evidence materially improves confidence and the runtime/API action is authorized.

## Expected output and validation

Report each case, observed artifact, pass/fail reason, checks run, runtime/version
when applicable, and remaining uncertainty. Static results must not be described
as behavioral proof.

## Agent handoff

- Selected when: A new or changed SKILLS entry needs evidence-based review or a promotion-readiness decision.
- Do not activate when: The task is authoring, routine skill selection, domain implementation, or release publication.
- Expected output: Representative/boundary findings with observed artifacts, failures, validation, and evidence limits.
- User-facing report: State what was exercised, what passed or failed, concrete follow-up, and unresolved uncertainty.
- Confirmation boundary: Ask before external model/API evaluation, publishing, or irreversible lifecycle changes.
