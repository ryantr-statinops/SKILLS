---
name: core
description: Design personal AI systems across problem framing, ML/LLM foundations, agents, tools, evaluation, and production constraints.
category: personal
subject: ai-engineering
scope: personal
status: experimental
version: 1.1.0
invocation: both
---

# AI engineering foundations

Use this skill to design an AI-enabled system as an engineered product rather than as a model demo. Keep the user outcome, data, model, context, tools, evaluation, and operational boundary explicit. It is the shared foundation for the personal AI router while specialized routes are not yet justified.

## Problem framing

- Define the user outcome and the decision or workflow being improved.
- Distinguish automation, prediction, classification, retrieval, generation, and decision support.
- Establish a non-AI baseline and identify when deterministic software is sufficient.
- Define error tolerance, human review, latency, privacy, and cost constraints.

## Model and system boundaries

Keep these components separate in the design:

- Data and data preparation.
- Model and model configuration.
- Prompt and context construction.
- Retrieval and embeddings.
- Tool calls and MCP integrations.
- Agent orchestration and memory.
- Application/backend boundary.
- Evaluation and monitoring.

Do not attribute application, retrieval, tool, or data failures to the model without isolating the boundary.

## ML foundations

Reason explicitly about dataset, labels, features, baseline, training/evaluation split, overfitting, generalization, model selection, leakage, distribution shift, offline evaluation, and online behavior. Separate prediction quality from causal claims and document assumptions.

## LLM and agent foundations

For LLM systems, define:

- Prompt and context construction.
- Structured output and validation.
- Embedding and retrieval behavior.
- RAG indexing, retrieval quality, and grounding.
- Tool calling, permissions, timeouts, and failure handling.
- Agent loop, stopping conditions, and human approval boundaries.
- Memory scope, retention, and privacy.

Use the smallest context and permission set that can achieve the user outcome.

## Evaluation

Build representative and boundary cases before relying on a model or agent. Evaluate the complete system where appropriate, including:

- Task success and correctness.
- Grounding and citation/attribution behavior.
- Structured output validity.
- Tool selection and argument safety.
- Refusal and escalation behavior.
- Latency, cost, rate limits, and reliability.
- Regression against previous prompts, models, data, and tools.

Keep offline tests separate from production observations and record uncertainty rather than presenting a small evaluation set as proof of general behavior.

## Production foundations

Plan inference, versioning, configuration, fallbacks, monitoring, privacy, safety, rate-limit handling, and cost controls. Make model, prompt, retrieval, tool, and data versions observable enough to reproduce a failure. Define rollout, rollback, and human approval boundaries before exposing side effects.

## Decision rules

- Do not choose a model before defining the user outcome and baseline.
- Do not add an agent loop when a deterministic call or workflow is sufficient.
- Do not grant tools or context broader permissions than the task requires.
- Do not treat a successful demo as evidence of production reliability.
- Do not hide retrieval, tool, or data-quality failures behind a generic model error.
- Do not create a specialized RAG, agent, MCP, or MLOps route until repeated work justifies a separate skill.

## Failure modes

Stop or narrow the design when:

- The outcome, evaluator, or acceptable failure behavior is unclear.
- Training/evaluation data can leak future or target information.
- Tool permissions, side effects, or human approval boundaries are unspecified.
- Cost, latency, privacy, or rate-limit constraints are ignored.
- A production decision depends on an unvalidated offline metric.

## Expected output

Provide the user outcome, non-AI baseline, system boundary, data/model/context/tool design, evaluation plan, production constraints, safety and approval boundaries, and unresolved risks.

## Validation

The design has a measurable outcome, representative and boundary evaluations, isolated failure boundaries, explicit permissions, and a plan to observe and reproduce production behavior.
