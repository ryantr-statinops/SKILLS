---
name: docker
description: Design and troubleshoot personal Docker images and compose environments with reproducibility and minimal operational complexity.
category: personal
subject: engineering
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# Docker workflow

## When to use
Use for containerization, image builds, local services, and compose environments.

## Personal principles
Prefer small deterministic images, explicit configuration, and easy local inspection.

## Workflow
Inspect app/runtime needs, define image boundary, build with pinned inputs, run health checks, and verify logs/network/volumes.

## Decision rules
Do not containerize complexity that the project does not need.

## Constraints
Keep secrets out of images and make persistence explicit.

## Failure modes
Distinguish image build, startup, network, volume, and application failures.

## Expected output
Provide Dockerfile/compose changes, commands, configuration, and checks.

## Validation
Build and startup are reproducible and health checks pass.
