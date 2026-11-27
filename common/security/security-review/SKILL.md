---
name: security-review
description: Review a change or system for concrete threats involving authentication, authorization, data, injection, dependencies, and access.
category: common
subject: security
scope: universal
status: experimental
version: 1.0.0
invocation: both
---

# Security review

## When to use
Use when designing or changing code that handles input, secrets, identity, files, network calls, or sensitive data, or when reviewing a change or system for security risk.

## Workflow
1. Map assets, actors, trust boundaries, and sensitive values.
2. Validate inputs, constrain outputs, minimize permissions, and keep secrets out of source, logs, and artifacts.
3. Inspect authentication, authorization, injection, dependencies, abuse cases, and failure behavior.
4. Rank findings by impact and likelihood, with evidence, security-focused tests, and remediation.

## Decision rules
- Fail closed when validation or authorization is uncertain; never disable a security control as a shortcut.
- Prioritize exploitable, concrete findings over generic best-practice lists.
- Do not claim a system is secure; state review scope, protections, and residual risk.

## Failure modes
If source, deployment, or threat context is missing, limit conclusions explicitly.

## Expected output
Return prioritized findings, evidence, impact, remediation, and limitations.

## Validation
Findings are reproducible or supported by a clear threat argument.
