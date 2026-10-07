# Evaluation harness

The repository evaluation harness is intentionally lightweight. It checks that
every common and personal skill has a valid representative case, boundary case,
required observable fields, and a skill ID present in the generated registry.
It does not claim to score an agent's reasoning. The observable workflow cases
in `tests/fixtures/observable-agent-evaluations.json` additionally verify the
required terms in all four workflow representative and boundary artifacts.
The observable checker requires one representative and one boundary case for
each of the four workflow skills. It rejects duplicate or invalid workflow/case
pairs and empty required-term lists; its term checks do not grade reasoning.
Codex Action reports are evidence from a configured run, not a substitute for
these deterministic checks.

## Current commands

```bash
python3 scripts/run_evaluations.py
python3 scripts/run_evaluations.py --format json
python3 scripts/run_evaluations.py --output /tmp/skill-evaluation.md
python3 scripts/check_observable_evaluations.py --format json
```

The default output is Markdown. JSON is intended for CI and later tooling.
Validation commands declared by a case are rejected unless they exactly match
the allowlist in the script. Allowlisted commands are skipped by default and
can be explicitly enabled with `--run-commands`.

## Extension checklist

Future harness work should be added in this order:

- [ ] Runtime adapter that runs a representative task in a disposable fixture.
- [ ] Human review form for routing, procedure, safety, and output quality.
- [ ] Stable scoring rubric separate from structural validation.
- [ ] Regression baseline for approved results and intentional changes.
- [ ] Failure capture that preserves logs without secrets or private data.
- [ ] Flaky-case classification, retry policy, and quarantine workflow.
- [ ] Runtime/version matrix for Codex and later adapters.
- [ ] Explicit timeout, network, filesystem, and mutation boundaries.

Do not add LLM self-grading or arbitrary command execution as a shortcut for
these controls. A future execution adapter must be allowlisted, isolated, and
reviewable.
