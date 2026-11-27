# Skill evaluation

Evaluation checks skill improves agent behavior on realistic tasks, not only Markdown completeness. Static checks not evidence agent followed skill/produced correct work. Behavioral evidence only tasks actually run, runtime/version, outputs.

## Minimum evaluation set

Every new/changed skill:

1. representative task activates skill;
2. nearby boundary task doesn't;
3. expected observable output;
4. failure conditions + safe handling;
5. validation command/review criteria.

Format [evaluation contract](evaluation-contract.md). Common, personal, meta keep `examples/evaluation.md` beside skill when required. Harness includes every `SKILL.md` common/personal/meta regardless promotion. `docs/metadata` generated registry references checked.

## Levels

### Structural

```bash
python3 scripts/validate_skills.py
```

Checks names, frontmatter, placeholders, resource directories, local links. `scripts/check_markdown_links.py` separate; doesn't check anchors.

### Behavioral

Run representative with skill available. Confirm intended procedure, relevant resources only, failure handling, expected result.

### Boundary

Run nearby out-of-scope task. Confirm description/exclusions prevent misrouting. Router selects child + not unrelated; leaf output; draft defer. Unrelated keyword doesn't activate.

## Regression

Keep useful cases. Activation/scope/procedure/output change rerun representative + boundary. Fix narrowest demonstrated problem; no broad rules from single speculative failure. No LLM self-grading or arbitrary command execution. Allowlisted validation commands rejected unless match; skipped default; `--run-commands` explicit. No arbitrary Markdown commands. See [harness](evaluation-harness.md).

## CLI

```bash
python3 scripts/run_evaluations.py
python3 scripts/run_evaluations.py --format json
python3 scripts/run_evaluations.py --output /tmp/skill-evaluation.md
python3 scripts/check_observable_evaluations.py --format json
```

## Codex common

Each `examples/evaluation.md`. `common/README.md` routes; `common/CODEX.md` runtime guidance not portable; selected `SKILL.md` before resources; portable outside Codex. Codex behavioral evidence only tasks actually run.
