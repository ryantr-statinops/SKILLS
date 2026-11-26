# API design & service architecture reference

## API design
- Prefer boring explicit contracts and predictable errors over clever interfaces.
- Define consumers and operations, model inputs/outputs/errors, set compatibility rules, document examples, and test boundary cases.
- Design for the actual consumer and lifecycle; do not expose internal storage models accidentally.
- Validate input, minimize sensitive output, and document breaking changes before freezing the contract.

## Service architecture
- Prefer a modular simple service before splitting into independently operated services.
- Map domain boundaries and data flow, identify failure/ownership boundaries, compare deployment options, and define migration triggers.
- Do not create a distributed boundary without independent scaling, ownership, or failure justification.
- Account for observability, local development, deployment, and debugging cost; ensure a runnable local path.
