# Evaluation case contract

Every skill evaluation is a small, reviewable behavior contract. It should
show when the skill activates, when it does not, what a useful result looks
like, and how the result can be checked.

## Required structure

Each skill with an evaluation case keeps it at:

```text
<skill>/examples/evaluation.md
```

The file must contain these sections for both cases:

- `## Representative task`
- `## Boundary task`
- `Task:`
- `Expected:`
- `Failure condition:`
- `Validation:`
Each field must have a nonempty value; a label alone or whitespace-only text
does not satisfy the contract. Values may continue on immediately following
lines and end at a blank line or the next field label.
The representative task should activate the skill and exercise its intended
outcome. The boundary task should be close enough to test routing, but outside
the skill's scope or safety boundary.

## Case semantics

- `Task:` describes the user request or test setup.
- `Expected:` describes observable behavior, not an ideal internal thought
  process.
- `Failure condition:` describes behavior that makes the case fail or unsafe.
- `Validation:` names the review, command, artifact, or assertion used to
  verify the result.

Router skills should make `Expected:` identify the selected child skill and
explain why unrelated children were not loaded. Leaf skills should make it
identify the expected workflow output. Draft scaffolds should explicitly state
when they must decline activation or defer to another skill.

## Harness boundary

The repository harness validates the contract and registry references. It does
not pretend to evaluate an agent's reasoning and does not execute arbitrary
commands from Markdown. Any future executable check must use an explicit
allowlist and a reviewed runtime adapter.

Future extensions may add runtime execution, human scoring, regression
baselines, and flaky-case handling without changing this basic contract.
