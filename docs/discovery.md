# Skill discovery

Select smallest relevant skill without loading whole library.

## Routing

```text
task
  → docs/skill-index.md or data/skills.json
  → candidate descriptions + metadata
  → activation boundaries
  → selected SKILL.md
  → conditional references/scripts/assets
  → execution + validation
```

For common skills start `common/README.md`. Codex also `common/CODEX.md`; other runtimes portable entrypoint only. Generated index routing aid, not replacement; read selected `SKILL.md` before instructions/resources.

## Query

Source repo: `docs/skill-index.md` human; `data/skills.json` tooling. Regenerate both after metadata changes.

```bash
python3 scripts/generate_skill_index.py
python3 scripts/generate_skill_index.py --check
python3 scripts/discover_skills.py "build a Node.js API"
python3 scripts/discover_skills.py --category personal "data pipeline"
python3 scripts/discover_skills.py --format json "debug failing test"
python3 scripts/discover_skills.py --invocation user ...
python3 scripts/discover_skills.py --invocation both ...
python3 scripts/discover_skills.py --invocation model ...
```

## Consumer installed catalog

Consumer installation uses `.agents/skills/`, not `.agent/skills`. If `.skill-catalog.json` is provided, use `.agents/skills/.skill-catalog.json` for discovery. It contains installed skills + bundle membership snapshot. Schema version **3**; discovery accepts **1–3**; old records without `requires` default `[]`. Don't assume `scripts/install_skills.py` writes `.skill-catalog.json` unless verified. With `--bundle`, installed catalog needs snapshot; don't fall back to source bundle registry.

```bash
python3 scripts/discover_skills.py --registry /path/to/project/.agents/skills/.skill-catalog.json "debug failing test"
python3 scripts/discover_skills.py --registry /path/to/project/.agents/skills/.skill-catalog.json --bundle feature-delivery "..."
```

## Selection rules

1. Match outcome not only technology keyword.
2. Prefer most specific skill covering task.
3. Reject `when not to use` boundary.
4. Combine only distinct responsibilities.
5. If no skill clearly applies, continue without forcing unrelated skill.

## Discoverable descriptions

Specific what + when; exclusion when misrouting likely. Prefer `Debug Python package installation...; not for general Python...`, avoid `Python development helper.` Category/subject/scope/status/version metadata aids routing but description still specific.

## Routing vs execution

Discovery returns candidates + reasons, not implement request. After selection read entrypoint + follow workflow, not repeat discovery instead of execution. Skill authoring/evaluation/intake/maintenance uses meta workflows.

## Overlap + conflicts

Resolve overlap via narrower scope, explicit exclusions, clear outputs. If two skills conflict procedures, stop + surface conflict; don't silently merge. User-invoked skills not silently trigger other user-invoked workflows.
