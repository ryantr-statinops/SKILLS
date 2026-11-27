---
name: networking
description: Diagnose and design personal service connectivity, ports, DNS, routing, and access boundaries.
category: personal
subject: engineering
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# Networking workflow

## When to use
Use when services cannot connect or a system needs a deliberate network boundary.

## Personal principles
Trace the path from process to port to route to endpoint before changing configuration.

## Workflow
Inspect processes, listeners, DNS, routes, firewall, and container/network boundaries; test each layer; change the narrowest layer.

## Decision rules
Do not expose a service publicly to bypass an unresolved local connectivity problem.

## Constraints
Minimize exposed ports and preserve authentication boundaries.

## Failure modes
Report whether failure is local process, bind address, DNS, route, firewall, or remote service.

## Expected output
Provide path diagnosis, targeted change, security impact, and verification.

## Validation
Connectivity works through the intended boundary without unnecessary exposure.
