# Skill bundles

Named reviewed selection of skill IDs. Distribution manifest, not second copy.

## Registry contract

Source truth `data/bundles.json`:

```json
{
  "schema_version": 1,
  "bundles": [
    {
      "id": "feature-delivery",
      "description": "Build a feature through planning, implementation, testing, and review.",
      "scope": "universal",
      "runtime_target": "portable",
      "allow_deprecated": false,
      "skills": ["common/workflow/feature-delivery"]
    }
  ]
}
```

Kebab-case id; useful description; scope; `portable` runtime target; explicit deprecated policy; canonical skill IDs. Universal bundles only reusable skills. Personal bundles may add `personal`; separate universal distribution. Current `feature-delivery` has **5** skills. Current bundles listed by `python3 scripts/install_skills.py --list-bundles`.

## Distribution

Resolve canonical ID. Copy referenced skill + supporting resources. Don't copy unrelated repo files. Installed adapter name hyphenated canonical ID under `.agents/skills`; supporting resources stay next to `SKILL.md`. Not claim preserve `common/...` path inside `.agents/skills`. Use [integration](integration.md).

Check mode resolves + validates no write. Normal safe sync **stops when target exists**; existing target not overwritten. Confirm remove/replace. Deprecated rejected unless `allow_deprecated: true`. `scripts/install_skills.py`, not `scripts/sync_skills.py`.

## Compatibility

Adding bundle additive. Removing/changing member distribution change; record changelog/release notes. Consumers needing reproducibility record source commit/release tag + bundle ID. Promotion separate `data/promoted.json`. Promoted skill in supported bundle; not every member promoted. `status` lifecycle separate from promotion. See [promotion](promotion.md).
