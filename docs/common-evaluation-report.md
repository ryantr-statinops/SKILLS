# Common skills evaluation report

## Scope

This review covers the 16 common skills currently in the repository. It
validates routing artifacts, portable entrypoints, evaluation scenarios, and
Codex-specific guidance without executing external project mutations.

## Results

- 16 common `SKILL.md` files discovered.
- 16 representative/boundary evaluation files discovered.
- Every common skill has `When to use`, `When not to use`, workflow or decision guidance, failure handling, expected output, and validation.
- `common/README.md` provides quick routing links for common skills.
- `common/CODEX.md` keeps Codex-only guidance outside portable skills.
- `docs/skill-index.md` and `data/skills.json` are synchronized.
- Duplicate names and canonical IDs are rejected by the validator.

## Commands

```bash
python3 scripts/validate_skills.py
python3 scripts/generate_skill_index.py --check
```

Both commands pass for the current repository.

## Routing review

| Request shape | Expected route |
| --- | --- |
| Understand an unfamiliar repository | `common/foundation/repository-onboarding` |
| Clarify an ambiguous request | `common/foundation/requirements-analysis` |
| Plan multi-step implementation | `common/foundation/task-planning` |
| Inspect Git before editing | `common/engineering/git-workflow` |
| Investigate a reproducible failure | `common/engineering/debugging` |
| Design tests for changed behavior | `common/engineering/testing` |
| Research a technical question | `common/research/research` |
| Compare technical options | `common/workflow/research-decision` |
| Review a security boundary | `common/security/security-review` |
| Prepare a release | No common release skill; use `docs/ci-release.md` |

Unrelated requests should not activate a common skill solely because they
contain a matching technology keyword.

## Follow-up

The repository-level phase is complete. A separate integration exercise may
still run these scenarios inside a real consumer project to verify runtime
discovery and project-specific behavior.
