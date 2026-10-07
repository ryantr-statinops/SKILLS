# Changelog

All notable repository releases are recorded here. Individual skill versions
remain in each skill's frontmatter.

## Unreleased

### Added

- Personal Orca orchestration skill adapted from the upstream runtime workflow.
- Transitive `requires` metadata, schema v3 registry support, safe sync updates,
  provenance manifests, installed catalogs, and native runtime adapters.
- Deterministic representative and boundary evaluations for all four workflow
  bundles plus optional Codex Action smoke and nightly jobs.

### Changed

- Discovery now works from an installed catalog without the source registry.
- Common and personal activation boundaries state concrete outcomes and nearby
  exclusions.
### Fixed

- OpenCode discovery tests verify behavior without pinning a workstation patch version.
- Ordinary sync now rejects managed destinations; use --update with the
  complete selection.
- Sync copy targets now collapse nested parent/child skills before installation.
- Update now restores managed files deleted from a consumer installation.
- Update preflights ancestor obstructions before copying managed files.
- Update rejects managed and catalog paths with unexpected file types before writing.
- Failed updates now remove newly created managed files.
- Failed updates restore prior content and manifest/catalog state.
- Installed catalogs use the current schema and preserve declared dependencies.
- Discovery rejects non-object registries and invalid skill-list containers.
- Discovery rejects incomplete or wrongly typed skill records before scoring.
- External catalog failures report the requested path and original parse/read cause.
- Registry generation and validation reject missing skill dependencies globally.
- Registry generation and validation reject dependency cycles outside bundles.
- Installed catalogs snapshot bundle membership for source-independent filtering.
- Consumer bundle filtering uses installed snapshots without source-tree access.
- Skill evaluation cases with empty required fields no longer pass structural checks.
- The skill validator rejects empty handoff contract values.
- Observable evaluation checks reject duplicate workflow/case pairs.
- Observable evaluation checks require both cases for all four workflows.
- Observable checks reject empty or invalid required-term lists.
- The evaluation harness rejects empty routing fixture collections.
- Routing evaluation rejects empty or whitespace-only task descriptions.
- Routing fixtures reject identical expected and boundary skills.
- Markdown link checks parse titles, reference destinations, parentheses, and code spans.
- Skill validation now shares the Markdown-aware link parser.
- Sync resource discovery uses the shared Markdown-aware destination parser.
- Skill discovery v2 supports universal consumer routing with explicit workflow boundaries.
- Skill authoring v2 narrows activation to authoring work and explicit skill outputs.
- Skill evaluation v2 separates static contracts from observed behavior and scope.
- Skill intake v2 records evidence, disposition, license duties, and authoring/evaluation handoff.
- Skill maintenance v2 covers caller migration, compatibility, and lifecycle scope.

### Added

- Evaluation contracts, personal evaluation cases, and the deterministic
  evaluation harness.
- Versioning and subtree distribution guidance.
- Personal Engineering Foundations covering shared computational and systems
  reasoning.
- A consolidated Statistics foundation and Quant production workflow.
- Portable bundle registry, bundle discovery, and conflict-safe selected sync.
- Feature delivery, bug fixing, research decision, and data analysis workflows.
- Consumer context and artifact templates for portable agent projects.
- Codex-compatible consumer fixture and workflow boundary coverage.
- Explicit promoted skill registry for the verified workflow baseline.

### Changed

- Common and personal evaluation files now include explicit task, expected,
  failure, and validation fields.
- Personal engineering is organized around shared, Data, AI, and Backend
  foundations; Data Engineering now uses the `engineering/data` namespace.
- Statistics now combines descriptive statistics, applied probability,
  inference, regression, time-series, and stochastic-process foundations.
- Quant now focuses on research and research-to-production engineering;
  trading, MT5, and execution-specific skill branches were retired.
- AI Engineering graduated from a draft scaffold to an experimental core
  skill with evaluation, tool, safety, and production boundaries.
- The verified baseline and workflow entry points are stable; the remaining
  library stays experimental or repository-specific.

### Release validation

- 71 skills passed metadata and bundle validation.
- 67 evaluation cases and 10 routing fixtures passed.
- Consumer sync, conflict, context, workflow, and personal routing tests passed.
- Local Markdown links and generated registries passed consistency checks.
