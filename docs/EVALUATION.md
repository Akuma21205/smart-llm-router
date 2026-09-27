# Evaluation Plan

## Objective

Determine whether the Jev router can reduce model cost and/or latency while preserving acceptable answer quality.

## Baseline

Every query is sent to the same strong model.

```text
Query -> Strong Model -> Answer
```

## Router

```text
Query -> Jev -> Policy -> Selected Model -> Answer
```

## Dataset

Start with 150 queries.

Suggested distribution:

```text
30 general
30 coding
30 reasoning
30 creative
30 ambiguous/mixed
```

Each query should have:

```json
{
  "id": "q001",
  "query": "Explain what a mutex is.",
  "expectedCategory": "general",
  "expectedComplexity": "low"
}
```

Do not use the same wording repeatedly.

## Routing Metrics

### Classification accuracy

```text
correct classifications / total classifications
```

### Complexity accuracy

```text
correct complexity predictions / total predictions
```

### Route accuracy

Compare the selected route with the expected route label.

This is an evaluation metric, not an assertion that one route is objectively correct for every query.

## Generation Metrics

For each query record:

- answer quality
- latency
- input tokens
- output tokens
- estimated cost
- model selected

## Quality Evaluation

Use a separate evaluator or manually scored rubric.

Example rubric:

| Dimension | Score |
|---|---:|
| Correctness | 1-5 |
| Relevance | 1-5 |
| Completeness | 1-5 |
| Instruction following | 1-5 |

Avoid using the router's own Jev decision as the answer-quality evaluator. Otherwise the evaluation becomes circular.

## Final Comparison

Example output:

```text
                    Baseline      Jev Router
------------------------------------------------
Quality score          4.5           4.4
Avg latency            2.8s          1.7s
Avg cost               $X            $Y
Strong model usage     100%          38%
Routing accuracy         -            92%
```

The actual numbers must come from experiments.

## Experiments

### Experiment 1 — Routing Accuracy

Measure how accurately Jev classifies the dataset.

### Experiment 2 — Cost

Compare total and average estimated cost.

### Experiment 3 — Latency

Compare end-to-end latency.

### Experiment 4 — Quality

Compare answer quality.

### Experiment 5 — Confidence Threshold

Run:

```text
0.50
0.60
0.70
0.80
0.90
```

and measure how routing behavior changes.

### Experiment 6 — Model Mix

Test different models for:

```text
fast
coding
reasoning
```

This prevents the final result from being tied to one arbitrary model lineup.

## Success Criteria

The project does not need to prove that Jev is universally superior.

A successful project demonstrates:

1. A working semantic routing layer.
2. Deterministic routing policy.
3. Multiple LLMs behind the router.
4. Measurable telemetry.
5. Reproducible evaluation.
6. Clear trade-offs.
