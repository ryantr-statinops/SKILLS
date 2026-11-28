# Repository Guidance

## Purpose

`SKILLS` is a portable library of agent skills: concise operational knowledge,
procedures, and judgment for engineering, data, AI, quantitative, and personal
workflows.

## Agent bootstrap protocol

Before acting on a repository task:

1. Inspect `git status`, the current branch, and relevant repository files.
2. Read `local.md` when it exists to understand current project state; it is
   local-only context, not a portable instruction or public source.
3. Use `docs/skill-index.md` or `data/skills.json` to discover candidates.
4. Read the selected router or leaf `SKILL.md` before following its procedure.
5. Load references, scripts, examples, and assets only when the task needs
   them.
6. Explain selected skills, assumptions, and confirmation boundaries when the
   task is multi-step or has material side effects.
7. Preserve unrelated work, validate the result, and report changed files,
   checks, risks, and next actions in user-facing language. When opening or
   completing a Pull Request, provide the direct clickable PR link
   (e.g. `https://github.com/ryantr-statinops/SKILLS/pull/<number>`) so the
   maintainer can review and merge with one click.

Follow the detailed lifecycle in
[`docs/agent-operating-model.md`](docs/agent-operating-model.md).

## Working rules

- Inspect the repository state before changing files.
- Keep each skill narrowly scoped and explicit about activation boundaries.
- Put essential routing and procedure in `SKILL.md`; defer deep context to linked references.
- Use scripts only when deterministic execution materially improves reliability.
- Do not create empty resource directories or copy generic documentation.
- Validate skills and links before committing.
- Avoid destructive Git commands and preserve unrelated user changes.
- Do not infer permission for destructive, external, push, tag, or release
  actions merely because a skill or tool is available.

## Repository taxonomy

- `common/`: broadly reusable skills.
- `personal/`: Ryan's workflow, preferences, and domain-specific practices.
- `meta/`: skills about authoring, discovering, evaluating, and maintaining skills.

## Change discipline

Follow [`CONTRIBUTING.md`](CONTRIBUTING.md) for branch, PR, and commit workflows:
branch off `main`, use short-lived branches (`feat/`, `fix/`, `docs/`, `chore/`),
and open PRs instead of pushing directly to `main`. Use focused commits with
imperative Conventional Commit messages. Run the relevant validation and
`git diff --check` before committing. When completing a PR, always supply the
clickable PR link in the final response.
