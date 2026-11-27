# Consumer smoke test

Verify small Codex-compatible project can discover + install selected portable skills without copying whole repo.

## Fixture contract

- `AGENTS.md` project instructions.
- `.agents/skills/` portable installed skill root; not `.agent/skills`.
- `CONTEXT.md` project boundaries + artifact paths.
- minimal source + test seam.
- `docs/agent/` workflow artifacts.

Fixture creates temp copy, inspects runtime layout, runs bundle check mode, selected safe sync, verifies relative resources. Must prove existing target reported before overwrite; safe sync stops. Check mode no write.

## Manual Codex smoke

After automated fixture passes, run representative + nearby boundary task in real Codex-compatible consumer when model use authorized:

1. install `portable-agent-baseline` or smallest workflow bundle;
2. ask representative feature/bug/research/data task;
3. confirm workflow + artifact path;
4. ask nearby out-of-scope task;
5. confirm unrelated workflow not activated.

Record source commit, bundle ID, runtime layout, checks, unresolved risks in consumer integration notes. Don't copy project-only instructions back. Local discovery not model quality. No model-backed run unless authorized.
