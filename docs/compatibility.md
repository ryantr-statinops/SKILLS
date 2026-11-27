# Compatibility

Plain Markdown + optional local resources; portable. Runtimes differ discovery, directory conventions, symlinks, script execution.

## Baseline

- Skill directory with `SKILL.md`.
- Runtime can read Markdown + relative links.
- Optional resources next to entrypoint.
- Project instructions selected agent directory `AGENTS.md`.
- Scripts not trusted automatically; review before execution.
- Skills don't require runtime-specific metadata beyond optional documented fields.
- Keep executable helpers self-contained + prerequisites.
- Separate portable procedure from personal/runtime integration.

## Integration check

Verify:

1. runtime scans which directory;
2. recognizes `SKILL.md` + YAML;
3. nested `references/`, `scripts/`, `examples/`, `assets/` accessible;
4. script interpreter/dependencies;
5. project/skill instruction priority.

Canonical modern layout `.agents/skills/<hyphenated-id>/SKILL.md`; user-level `~/.agents/skills`. Not `.agent/skills`. Installed adapter name hyphenated canonical ID; supporting resources remain. Runtime support requires tested version, layout, representative task, validation result; directory name not proof. Don't claim runtime support until tested. `scripts/install_skills.py`.

## Change compatibility contract

Preserve existing consumer integrations unless breaking change documented.

- Registry schema version **3**. Discovery reads **1–3**; old records without `requires` default `[]`; present dependency lists retained + validated. Sync writes current. Breaking schema changes update version + compatibility reader when safe.
- Additive metadata needs migration/default.
- Adapter must not change portable meaning.
- **Safe sync:** `--check` no write; normal sync stops when target exists; no overwrite; confirm removal; preserve selected target layout + conflicts. `scripts/install_skills.py`.
- Runtime support claims require fixture, tested layout, runtime version, representative task, validation result.
- `.skill-catalog.json` only if provided; schema 1–3; don't claim installer generates.

## Verified runtime matrix

| Runtime | Layout | Verification | Scope |
|---|---|---|---|
| Codex CLI 0.160.0 ([guide](runtime-codex.md)) | `.agents/skills/<hyphenated-id>/SKILL.md` | `codex debug prompt-input` fixture: all 5 `feature-delivery` skills visible under project root `r5` | local prompt construction only; no model selection/behavior |
| OpenCode 1.18.35 ([guide](runtime-opencode.md)) | `.agents/skills/<hyphenated-id>/SKILL.md` | `opencode debug skill --pure` fixture: all 5 `feature-delivery` skills with project `location` | discovery + frontmatter loading; no model quality |
| oh-my-pi `omp` 18.6.3 ([guide](runtime-omp.md)) | `.agents/skills/<hyphenated-id>/SKILL.md` | `omp skill list` fixture: all 5 `feature-delivery` skills with project `filePath` | local discovery only; repeated display names namespace; no behavior |

CI Codex action version separate. Runtime behavior changes; re-verify. Ecosystem research not support claim.
