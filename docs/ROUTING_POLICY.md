# Routing Policy

## Goal

Map Jev's semantic classification to one of three model routes.

The policy is intentionally simple in V1.

## Input

```ts
type RoutingDecision = {
  category: "general" | "coding" | "reasoning" | "creative";
  complexity: "low" | "medium" | "high";
  confidence: number;
};
```

## Routes

```ts
type Route = "fast" | "coding" | "reasoning";
```

## Initial Rules

| Category | Complexity | Route |
|---|---|---|
| general | low | fast |
| general | medium | fast |
| general | high | reasoning |
| coding | low | coding |
| coding | medium | coding |
| coding | high | reasoning |
| reasoning | low | reasoning |
| reasoning | medium | reasoning |
| reasoning | high | reasoning |
| creative | low | fast |
| creative | medium | fast |
| creative | high | reasoning |

## Confidence Rule

If confidence is below the initial threshold:

```text
confidence < 0.70
```

route to:

```text
reasoning
```

This is deliberately conservative for the first benchmark.

The threshold is a configurable experiment parameter, not a universal recommendation.

## Important

The route should be selected by deterministic code.

Do not ask Jev:

```text
Which exact model should I call?
```

Ask Jev:

```text
What kind of task is this?
How complex is it?
```

Then let our policy decide.

This separation gives us a clean experiment:

```text
Jev classification quality
+
routing policy
+
model quality
=
system behavior
```

## Future Policy Experiments

We can later test:

### Cost-aware

```text
Use stronger models only when necessary.
```

### Latency-aware

```text
Prefer fast models for low-complexity requests.
```

### Quality-aware

```text
Use stronger models when complexity or uncertainty is high.
```

### Budget-aware

```text
Daily budget remaining -> route differently.
```

These should be evaluated experimentally rather than assumed to improve the system.
