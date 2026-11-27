# Consumer smoke test

The consumer smoke test verifies that a small Codex-compatible project can
discover and install selected portable skills without copying the whole
repository.

## Fixture contract

A fixture project contains:

- `AGENTS.md` for project instructions;
- `.agents/skills/` as the portable skill root;
- `CONTEXT.md` with project boundaries and artifact paths;
- a minimal source and test seam;
- `docs/agent/` for workflow artifacts.

The test creates a temporary copy, inspects the runtime layout, runs bundle
check mode, performs selected sync, and verifies relative resources. It must
also prove that an existing target path is reported before overwrite.

## Manual Codex smoke run

After the automated fixture passes, run one representative task and one nearby
boundary task in a real Codex-compatible consumer project:

1. install `portable-agent-baseline` or the smallest relevant workflow bundle;
2. ask for a representative feature, bug, research, or data task;
3. confirm the expected workflow and artifact path;
4. ask a nearby out-of-scope task;
5. confirm that the unrelated workflow is not activated.

Record the source commit, bundle ID, runtime layout, checks, and unresolved
risks in the consumer project's integration notes. Do not copy project-only
instructions back into this repository.
