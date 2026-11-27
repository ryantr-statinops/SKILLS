# Evaluation case contract

Small reviewable behavior contract: when activates, when not, useful result, how checked. Path `<skill>/examples/evaluation.md`.

## Required structure

For both `## Representative task` + `## Boundary task`:

- `Task:`
- `Expected:`
- `Failure condition:`
- `Validation:`

Nonempty values; label alone/whitespace invalid. Values continue immediately following lines until blank/next field. Representative activates intended outcome; boundary close but outside scope/safety. `Task:` user request/test setup. `Expected:` observable behavior not internal thought. `Failure condition:` fails/unsafe. `Validation:` review/command/artifact/assertion.

Router `Expected:` selected child + unrelated not loaded. Leaf expected workflow output. Draft explicitly defer/decline. Concrete activation/exclusion not generic template.

## Routing fixture

`tests/fixtures/agent-routing.json` at least one case. `task` nonempty. `expected_skill` exists; optional `boundary_skill` exists + differs. `expected_explanation` + `expected_validation` true; `confirmation` allowed. Structural routing claims only; not actual agent choice.

## Harness boundary

Harness validates contract + registry references. Doesn't simulate agent selection/evaluate reasoning/execute arbitrary Markdown. Future executable checks explicit allowlist + reviewed runtime adapter. Runtime reports only actual tasks/runtime/version/outputs; not broader claims. `check_observable_evaluations.py` checks literal terms, not semantic correctness/safety. Future runtime execution, human scoring, stable rubric, regression baselines, flaky handling, runtime matrix, timeout/network/filesystem/mutation bounds explicit; no self-grading shortcut. Validation commands allowlisted; `--run-commands` explicit.
