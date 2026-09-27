# Architecture

## 1. High-Level System

```text
                         +-------------+
                         |    Client   |
                         +------+------+
                                |
                                | POST /chat
                                v
                     +----------------------+
                     |    Router API        |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |      Jev Layer       |
                     |                      |
                     | category             |
                     | complexity           |
                     | confidence           |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |  Routing Policy      |
                     |                      |
                     | category +           |
                     | complexity -> route  |
                     +----------+-----------+
                                |
                +---------------+---------------+
                |               |               |
                v               v               v
             FAST            CODING          REASONING
                |               |               |
                +---------------+---------------+
                                |
                                v
                         +-------------+
                         | OpenRouter  |
                         +------+------+
                                |
                                v
                           Selected LLM
```

## 2. Responsibility Boundaries

### Jev

Jev answers semantic questions about the request.

Example:

```text
Category:
coding

Complexity:
high

Needs strong reasoning:
true
```

Jev should not contain application-specific provider IDs.

### Routing Policy

The routing policy maps Jev's decision to a route.

Example:

```text
coding + low  -> coding
coding + high -> reasoning
general + low -> fast
general + high -> reasoning
```

This layer is deterministic and unit-testable.

### OpenRouter

OpenRouter provides access to the actual model selected by the routing policy.

The router should not depend on OpenRouter's automatic routing for model selection. OpenRouter is the inference transport/model access layer.

## 3. Why Separate Jev From Routing Policy?

A probabilistic classifier should not directly have authority to execute arbitrary infrastructure decisions.

Instead:

```text
Probabilistic decision
        |
        v
Validated typed result
        |
        v
Deterministic policy
        |
        v
Model selection
```

This lets us change policy without changing the Jev prompt and lets us test policy independently.

## 4. Confidence and Fallback

If Jev is uncertain:

```text
confidence < threshold
        |
        v
fallback route
```

The first MVP should use a conservative fallback rather than making an aggressive model selection.

Example:

```text
uncertain -> reasoning
```

Later, this can be evaluated against:

```text
uncertain -> ask another classifier
uncertain -> strongest model
uncertain -> default model
```

## 5. Observability

Each request should record:

```json
{
  "requestId": "...",
  "category": "coding",
  "complexity": "high",
  "route": "reasoning",
  "model": "...",
  "routingLatencyMs": 120,
  "generationLatencyMs": 1800,
  "inputTokens": 80,
  "outputTokens": 500,
  "estimatedCostUsd": 0.002
}
```

This telemetry is required for the final benchmark.

## 6. Failure Modes

### Jev failure

Use a deterministic fallback route.

### Selected model failure

Use provider/model fallback infrastructure where appropriate.

### Invalid decision

Reject the decision and use the safe default route.

### Missing usage data

Do not fabricate cost. Mark cost as unavailable.

## 7. Future Architecture

Later versions can add:

```text
                 +----------------+
                 | Evaluation DB  |
                 +-------+--------+
                         |
                         v
User -> Jev -> Policy -> Model
              |
              +-> telemetry
              |
              +-> feedback
              |
              +-> policy tuning
```

This creates a closed evaluation loop without allowing the production router to silently change itself.
