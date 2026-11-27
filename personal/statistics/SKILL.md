---
name: statistics
description: Apply foundational statistical reasoning across descriptive analysis, probability, inference, regression, time-series, and stochastic processes with explicit assumptions and uncertainty.
category: personal
subject: statistics
scope: personal
status: experimental
version: 1.0.0
invocation: both
---

# Statistics foundations

Use this skill as a compact statistical foundation for Data Engineering, AI Engineering, Quant Research, and general analytical work. It is one scalable skill for now; split a module into a child skill only when repeated workflows need independent routing.

## When to use

Use when a task requires statistical description, applied probability, inference, regression, temporal reasoning, stochastic-process concepts, or method selection under uncertainty. Do not use it as a substitute for data-pipeline, model-serving, backend, or code-optimization guidance.

## Descriptive statistics

Choose summaries that match the data-generating context and explain what they do not establish. Consider:

- Mean, median, variance, quantiles, and robust summaries.
- Distribution shape, skew, tails, dependence, and association.
- Grouped summaries and appropriate visualizations.
- Missingness, duplicates, outliers, and measurement limitations.
- Summary versus interpretation, prediction, or causal claim.

## Applied probability

Make the model explicit before manipulating formulas:

- Sample space, events, random variables, and distributions.
- Conditional probability and independence.
- Expectation, variance, covariance, and common distributions.
- Simulation as a check of a stated model, not a replacement for assumptions.
- Distinction between probability statements and observed frequencies.

## Inference

Define the estimand and uncertainty before choosing a test or interval:

- Sampling distributions and estimators.
- Confidence intervals and hypothesis tests.
- Effect size versus statistical significance.
- Practical importance, power, and multiple comparisons.
- Bootstrap and permutation methods at the applied level.
- Uncertainty communication and limitations of the sample.

## Regression

Use regression according to the question rather than treating it as an automatic explanation tool:

- Define feature, target, estimand, and prediction goal.
- Linear and logistic regression foundations.
- Residuals, diagnostics, confounding, and dependence.
- Regularization and model complexity.
- Prediction versus explanation and the limits of causal interpretation.
- Validation, calibration, and uncertainty.

## Time-series

Respect temporal structure:

- Timestamp semantics, gaps, lags, autocorrelation, trend, and seasonality.
- Stationarity and regime changes.
- Forecast horizon and chronological train/validation/test splits.
- Simple baselines before more complex models.
- Forecast uncertainty, residual diagnostics, and future-feature leakage.

## Stochastic processes

Connect formal definitions to dynamics and verification:

- Index and state spaces.
- Transition and dependence structure.
- Markov property, stationarity, and ergodicity when relevant.
- Theoretical properties versus finite-sample simulation evidence.
- Simulation of special cases and consistency checks.

## Method-selection workflow

```text
Define question
→ Define data-generating context
→ Define estimand or target
→ Inspect data
→ State assumptions
→ Select method
→ Compute or model
→ Validate
→ Interpret uncertainty and limitations
```

## Decision rules

- Do not use independence, stationarity, normality, or causal assumptions implicitly.
- Do not treat a p-value as effect size, practical importance, or causality.
- Do not use random splits for temporal prediction.
- Do not present simulation evidence as proof of a theoretical property.
- Do not choose a complex method before defining a simple baseline.
- Do not let a statistically precise result hide biased measurement, sampling, or missingness.

## Boundaries

- Use `personal/engineering/core` for algorithm, performance, and systems reasoning.
- Use `personal/engineering/data` for contracts, pipelines, storage, lineage, and data operations.
- Use `personal/engineering/ai` for model/system design, evaluation infrastructure, and inference operations.
- Use `personal/quant/research` for signal hypotheses, backtesting, costs, and research evidence.

## Expected output

Provide the question, data-generating context, estimand or target, assumptions, selected method, calculation/model, uncertainty, diagnostics, interpretation, and limitations.

## Validation

The method matches the data structure, assumptions are stated and checked where possible, baselines or special cases are used, uncertainty is reported, and conclusions do not exceed the evidence.
