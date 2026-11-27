# SKILLS architecture

Portable Agent Skill Library separating capability content from discovery, integration, quality lifecycle.

```text
SKILLS/
├── Skill library
│   ├── common/       portable workflows shared across projects
│   ├── personal/     Ryan's workflow and domain judgment
│   └── meta/         authoring, discovery, evaluation, intake, maintenance
│
├── Discovery & integration
│   ├── index          docs/skill-index.md and data/skills.json
│   ├── metadata       frontmatter and docs/metadata.md
│   ├── router         category/subject SKILL.md entrypoints
│   └── installer      scripts/install_skills.py
│
└── Quality & lifecycle
    ├── validation     scripts/validate_skills.py
    ├── evaluation     scripts/run_evaluations.py + evaluation docs
    ├── regression     tests/ and evaluation fixtures
    ├── CI             .github/workflows/validate.yml
    ├── versioning     docs/versioning.md
    └── release        CHANGELOG.md + docs/ci-release.md
```

## Skill library

Every skill directory has required `SKILL.md`. Optional `references/`, `scripts/`, `examples/`, `assets/` only when real supporting content. Keep capability, boundaries, workflow, decisions, failure modes, output, validation close together.

- `common/`: reusable engineering, data, security, delivery, agent workflows.
- `personal/`: Ryan-specific preferences and domain foundations.
- `meta/`: skill-system procedures.

## Discovery

Smallest relevant skill before full instructions:

```text
user intent
  → AGENTS.md + runtime guidance
  → optional local.md
  → generated index + candidate descriptions
  → router SKILL.md
  → selected leaf SKILL.md
  → conditional resources
  → execution, validation, report
```

Canonical ID path-based, e.g. `common/engineering/testing`. Installed adapter name hyphenated canonical ID, e.g. `common-engineering-testing`. Runtime discovery root `.agents/skills/`, not `.agent/skills`. `docs/discovery.md` defines selection. `docs/integration.md` defines safe install. `docs/bundles.md` defines bundle manifests.

## Quality

1. Structural metadata, paths, links, generated files checked by validator.
2. Representative + boundary cases checked by evaluation harness.
3. Regression tests protect harness/tooling.
4. CI runs checks on PRs and pushes to `main`.
5. Skill SemVer + repository tags distribution.

Runtime-specific behavior belongs in adapters/runtime notes, not portable meaning.

## Related

- [Agent operating model](agent-operating-model.md)
- [Integration](integration.md)
- [Discovery](discovery.md)
- [Metadata](metadata.md)
- [Evaluation](evaluation.md)
- [Compatibility](compatibility.md)
- [Versioning](versioning.md)
- [CI and release](ci-release.md)
