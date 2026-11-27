---
name: latex
description: Create maintainable LaTeX documents for mathematical, technical, and educational writing.
category: personal
subject: education
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# LaTeX foundations

## When to use
Use for structured mathematical or technical documents.

## Personal principles
Prefer semantic structure, readable source, reusable macros, and reproducible builds.

## Workflow
Define document structure, choose minimal packages, write content semantically, build early, and inspect warnings/output.

## Decision rules
Do not fix layout symptoms with arbitrary spacing before understanding structure.

## Constraints
Keep source portable and document required tools.

## Failure modes
If compilation fails, isolate the smallest failing document.

## Expected output
Provide source, build command, and rendered verification.

## Validation
The document builds cleanly enough for its purpose and has no unresolved references.
