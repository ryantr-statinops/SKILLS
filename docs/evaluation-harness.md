# Evaluation harness

The repository evaluation harness checks that each common, personal, and meta
skill has representative and boundary cases with required observable fields,
and that each skill ID appears in the generated registry. It also checks routing
fixture structure and declared expected/boundary skill IDs; it does not execute
the task or simulate agent selection. These are static contract checks, not
evidence that an agent followed a skill or produced correct work.

The observable workflow checker inspects declared artifacts for required literal
terms in one representative and one boundary case per workflow. It rejects
missing/duplicate workflow-case coverage and invalid required-term lists, but
term presence does not prove semantic correctness, reasoning quality, or safety.

The harness includes every `SKILL.md` under `common/`, `personal/`, and `meta/`,
regardless of promotion status. Its JSON report lists each covered skill and
static result.

Codex Action or local runtime reports provide behavioral evidence only for the
tasks actually exercised, runtime/version, and captured outputs. They do not
replace the static checks or establish broader claims than the run supports.

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
