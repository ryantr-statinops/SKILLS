# Versioning and releases

Two layers: skill `version` + repository release tag. Generated index regenerate after metadata. `local.md` not source.

## Skill versions

SemVer `MAJOR.MINOR.PATCH`.

- `PATCH`: typo/link/clarification/validation/wording no activation/expected behavior change.
- `MINOR`: new backward-compatible capability/example/resource.
- `MAJOR`: changed activation boundary/output contract/path/safety rule/behavior invalidating consumer.
- Bump each affected skill independently. Regenerate indexes. `status` separate lifecycle; `promotion` separate. Breaking recorded. Adding bundle additive; removing/changing member distribution change; removing docs no skill version unless skill content. No push/tag/release without explicit.

## Repository releases

Tags `vMAJOR.MINOR.PATCH`. Reviewed release-ready batch, not every commit. Tag identifies coherent snapshot; frontmatter skill lifecycle. Before tag:

1. structural validation + eval + generated-index + local link checks;
2. review diff + generated registry;
3. review skill SemVer + breaking behavior;
4. update `CHANGELOG.md` Added/Changed/Fixed/Deprecated/Removed;
5. record compatibility/subtree/breaking notes;
6. confirm subtree consumers pull + source tag;
7. create + push tag only after approval. CI doesn't tag/publish/push. Publish report.

## Release report

Tag, source commit, total skill count (don't hard-code; from `data/skills.json`), validator, evaluation, metadata changes, link check, breaking notes, known limitations. Release automation explicit; ordinary CI never creates/pushes tags. See [CI and release](ci-release.md).
