---
name: requirements-analysis
description: Turn an ambiguous request into explicit outcomes, constraints, assumptions, and acceptance criteria.
category: common
subject: foundation
scope: universal
status: stable
version: 1.0.0
invocation: both
---

# Requirements analysis

## When to use
Use when a request has unclear scope, missing inputs, competing interpretations, or meaningful risk.

## When not to use
Do not over-analyze a small, unambiguous change.

## Workflow
1. Restate the desired outcome.
2. Identify inputs, outputs, constraints, actors, and affected files.
3. Separate facts from assumptions and open decisions.
4. Define acceptance criteria and boundary cases.
5. Ask only questions that materially change the implementation.

## Decision rules
- Prefer observable outcomes over implementation preferences.
- Resolve high-impact ambiguity before making irreversible choices.

## Failure modes
If requirements conflict, present the conflict and viable interpretations instead of guessing silently.

## Expected output
Produce a short requirements summary with scope, exclusions, assumptions, and acceptance criteria.

## Validation
Check that another engineer could implement the request without inventing product decisions.
