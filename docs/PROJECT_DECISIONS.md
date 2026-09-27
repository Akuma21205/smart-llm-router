# Project Decisions

## Decision 1 — Python

We will use Python because it is the primary development language for this project and provides a strong ecosystem for LLM orchestration, APIs, evaluation, and data analysis.

The current Jev ecosystem also provides a Python SDK, allowing us to use Jev without forcing the project into a TypeScript-only stack.

## Decision 2 — LangChain

LangChain will be the AI application framework.

It will provide:

- model abstraction
- provider integration
- orchestration
- prompt/model composition
- a consistent interface for swapping models

LangChain does **not** replace Jev.

The responsibilities remain:

```text
Jev -> semantic classification
LangChain -> model orchestration
OpenRouter -> model access
Our policy -> model selection
```

## Decision 3 — Jev Does Classification, Not Model Selection

We do not want Jev tightly coupled to provider/model IDs.

Instead:

```text
Jev
 ↓
semantic decision
 ↓
routing policy
 ↓
route
 ↓
LangChain
 ↓
model ID/provider
```

This lets us benchmark different policies and model mixes.

## Decision 4 — OpenRouter

OpenRouter will be the model access layer.

Reason:

- one API
- multiple model providers
- easy model replacement
- consistent OpenAI-compatible interface
- useful usage metadata

## Decision 5 — No Local Models

The project intentionally uses hosted models.

This keeps the experiment focused on routing rather than local inference infrastructure.

## Decision 6 — No Database in the First Prototype

The first working pipeline should not depend on a database.

Database telemetry comes after the routing loop works.

## Decision 7 — No Frontend in V1

The first interface is an HTTP API/CLI.

A dashboard comes after evaluation data exists.

This prevents us from spending time making an attractive UI around an unvalidated system.

## Decision 8 — Benchmark Against a Baseline

A router without a baseline cannot demonstrate whether it helped.

The baseline is:

```text
Every query -> same strong model
```

The experimental system is:

```text
Every query -> Jev -> routing policy -> LangChain -> selected model
```

## Decision 9 — Cost Is Measured, Not Assumed

Model prices and availability change.

The project should read current model metadata/pricing where possible and record the pricing snapshot used for an evaluation run.

Do not hard-code claims such as "X% cheaper" until the experiment has produced those numbers.
