---
name: git-workflow
description: Inspect and safely modify Git repositories, including status, branches, diffs, commits, and synchronization.
category: common
subject: engineering
scope: universal
status: experimental
version: 1.0.0
invocation: both
---

# Git workflow

## When to use
Use for repository changes involving branches, diffs, commits, merges, or pushes.

## Workflow
1. Inspect status, branch, remotes, and recent commits.
2. Understand unrelated or pre-existing changes.
3. Make focused edits and review the diff.
4. Run relevant checks and `git diff --check`.
5. Commit with a descriptive message and synchronize only when authorized.

## Decision rules
- Preserve user changes and prefer small commits.
- Never overwrite or discard work to make a clean diff.

## Safety constraints
Do not use destructive reset, checkout, clean, or force-push operations without explicit authorization.

## Failure modes
Stop on conflicts, unexpected remote changes, or unclear ownership and report the exact state.

## Expected output
Report changed files, checks, commit, and synchronization status.

## Validation
Review staged diff, run relevant tests, and verify branch/remote state after synchronization.
