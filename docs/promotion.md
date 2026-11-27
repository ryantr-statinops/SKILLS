# Promotion and distribution lifecycle

`status`: `draft`, `experimental`, `stable`, `deprecated`. Promotion separate `data/promoted.json`, not duplicated frontmatter. `docs/skill-index` generated from metadata; promoted not separate status. Stable doesn't mean promoted. `local.md` not source.

## Promoted contract

Promoted skill:

- stable frontmatter;
- documented public guides;
- required evaluation contract;
- at least one supported bundle;
- valid metadata/links/invocation;
- reviewed activation boundary, evals, supporting links, bundle membership, consumer behavior.

Promotion doesn't move/copy content. Explicit supported consumer entry. Promoted set small reviewed, not automatic entire library. `deprecated` excluded new bundles/workflows unless reviewed `allow_deprecated: true`. Universal bundles reject deprecated unless explicit; promoted stable in supported bundle.

## Lifecycle

- `draft`: incomplete not ready.
- `experimental`: usable seeking evidence/feedback.
- `stable`: contract mature; versioning policy.
- `deprecated`: excluded new workflows/bundles unless reviewed exception.
- Stable repository-only or not promoted allowed.
- Workflows `invocation: user`; don't silently trigger user workflows.

## Review

Before adding `data/promoted.json`, review boundaries, evals, links, bundle membership, consumer. Removing/changing promoted distribution record. See [versioning](versioning.md).
