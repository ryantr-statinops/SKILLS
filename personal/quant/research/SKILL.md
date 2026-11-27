---
name: research
description: Investigate quantitative hypotheses and historical strategies with explicit data, leakage, cost, robustness, and reproducibility controls.
category: personal
subject: quant
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# Quant research

Use this skill for quantitative signal or model research before any production decision. Treat every backtest as an experiment with explicit failure modes, not as proof of future returns.

## Workflow

1. State the research question, economic or technical hypothesis, and falsifiable failure criteria.
2. Define the data contract, universe, timestamps, availability, transformations, and ownership.
3. Define features, labels, signal timing, execution delay, warm-up periods, and missing-data behavior.
4. Establish a simple baseline and choose chronological train/validation/test boundaries.
5. Control look-ahead, survivorship, selection, target, and preprocessing leakage.
6. Include transaction costs, slippage, liquidity, rejected actions, and other relevant constraints.
7. Evaluate metrics, sensitivity, robustness, out-of-sample behavior, and uncertainty.
8. Record artifacts, parameters, environment, assumptions, limitations, and the next experiment.

## Decision rules

- Prefer falsifiable hypotheses, simple baselines, and honest out-of-sample evidence.
- Do not use random splits when time or availability ordering matters.
- Do not hide transaction costs, execution delay, warm-up periods, rejected actions, or parameter selection.
- Stop on leakage, impossible fills, survivorship bias, unstable results, or unverified timestamps.
- Separate research evidence from production readiness and execution decisions.

## Expected output

Provide the hypothesis, data contract, timing rules, baseline, evaluation design, metrics, cost assumptions, robustness results, limitations, and next experiment.

## Validation

Results are reproducible, include a baseline and correctly separated out-of-sample evaluation, expose cost and leakage assumptions, and do not authorize live execution.
