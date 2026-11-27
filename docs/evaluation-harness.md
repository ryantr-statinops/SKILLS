# Evaluation harness

Static contract checks + deterministic observable checks. Not proof agent followed skill/produced correct work; no arbitrary command execution; no LLM self-grading. Runtime evidence separate.

Checks common/personal/meta representative + boundary fields; registry IDs; routing fixture structure; registry references. Includes every `SKILL.md` common/personal/meta regardless promotion. JSON/Markdown report covered skill + static result. Observable workflow checker inspects artifacts for required literal terms one representative + boundary per workflow; rejects missing/duplicate coverage + invalid term lists. Literal presence not semantic correctness/reasoning/safety. Codex/local runtime reports actual tasks only.

## Commands

```bash
python3 scripts/validate_skills.py
python3 scripts/generate_skill_index.py --check
python3 scripts/run_evaluations.py
python3 scripts/run_evaluations.py --format json
python3 scripts/run_evaluations.py --output /tmp/skill-evaluation.md
python3 scripts/check_observable_evaluations.py --format json
python3 scripts/check_markdown_links.py
```

Markdown default; JSON CI/tooling. Validation commands exactly match script allowlist; rejected otherwise. Skipped default; `--run-commands` explicit. Markdown link checker doesn't verify anchors.

## Future extension checklist

- [ ] Disposable fixture runtime adapter representative task.
- [ ] Human review routing/procedure/safety/output.
- [ ] Stable scoring rubric separate structural.
- [ ] Regression baseline approved changes.
- [ ] Failure capture logs no secrets/private.
- [ ] Flaky classification/retry/quarantine.
- [ ] Runtime/version matrix.
- [ ] Timeout/network/filesystem/mutation bounds.
- [ ] Explicit allowlist + isolation + review.

No arbitrary commands/LLM self-grading shortcut. See [contract](evaluation-contract.md).
