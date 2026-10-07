---
name: skill-intake
description: Decide whether to reference, adopt, adapt, rebuild, or reject an external skill or a demonstrated recurring workflow.
category: meta
subject: skill-system
scope: repository
status: stable
version: 2.0.0
invocation: user
---

# Skill intake

## When to use

Use when reviewing an external skill or ecosystem for possible use in this
library, or when a recurring workflow provides evidence that a new skill may be
needed. Produce a disposition before importing or authoring content.

## When not to use

Do not use to author or restructure an already accepted skill; use
`meta/skill-authoring`. Use `meta/skill-discovery` to select an existing skill
for a task and `meta/skill-evaluation` to assess its behavior. Do not use intake
as domain implementation guidance.

## Workflow

1. State the target task, desired outcome, and evidence the capability is needed.
2. Inspect source structure, license, dependencies, scope, runtime assumptions,
   and validation. For a personal workflow, inspect evidence from repeated real
   use rather than proposing a skill from a topic label.
3. Choose one disposition: reference, copy, adapt, rebuild, or reject.
4. Classify the proposed result as `common`, `personal`, or `meta`.
5. Record license/attribution obligations, prerequisites, and a migration path
   before any content is copied or adapted.
6. If accepted, hand off to skill authoring for entrypoint creation and
   representative/boundary evaluation; do not treat intake approval as proof
   that the resulting skill works.

## Disposition rules

- **Reference:** use a pattern without importing source implementation.
- **Copy:** only when the license permits it and the skill already fits this
  library's scope and format.
- **Adapt:** retain useful procedure while rewriting activation, boundaries, and
  repository conventions.
- **Rebuild:** extract the needed behavior when the source is complex, coupled to
  another runtime, overly generic, or incompatible.
- **Reject:** choose when scope is unclear, redundant, unsafe, unmaintained, or
  unsupported by a real task.

For a one-file Markdown skill, inspect the file and its license directly. For a
complex skill with scripts, references, or runtime assumptions, inspect the
whole dependency/resource tree before choosing a disposition.

## Classification rules

- `common`: transferable procedure without Ryan-specific dependencies.
- `personal`: depends on Ryan's tools, projects, conventions, or domain judgment.
- `meta`: changes how skills are authored, routed, evaluated, intaken, or maintained.

If reusable and personal parts differ, keep the reusable core in `common/` and
the preference-specific extension in `personal/`.

## Failure modes

- License unclear: do not copy; request review or rebuild only from independently
  established behavior.
- Documentation dump: extract decisions and workflow, not the source text.
- Scope overlap: extend the existing skill or record a clear boundary.
- No real task evidence: reject or defer the proposed new skill.

## Expected output and validation

Record the disposition, classification, evidence, license/attribution duties,
dependencies, migration path, and next authoring/evaluation step. Intake itself
does not claim behavioral validation of an unauthored skill.

## Agent handoff

- Selected when: An external capability or demonstrated recurring workflow needs an adopt/adapt/rebuild/reject decision.
- Do not activate when: The task only selects a skill, authors an already accepted skill, evaluates its behavior, or implements domain work.
- Expected output: A disposition and evidence record with license, classification, dependencies, and migration obligations.
- User-facing report: Explain the evidence, chosen disposition, attribution/migration duties, and follow-up validation.
- Confirmation boundary: Ask before copying under uncertain license, destructive changes, external writes, publication, or irreversible acceptance.
