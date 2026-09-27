# Smart LLM Router

A practical routing system that uses **Jev** to classify incoming user requests and deterministically route them to an appropriate LLM through **LangChain + OpenRouter**.

## Problem

Using one large model for every request is often unnecessary.

A simple question may only need a fast, inexpensive model, while a difficult coding or reasoning task may justify a stronger model.

This project explores whether a small, fast decision layer can route requests intelligently while reducing latency and model cost without materially reducing answer quality.

## Architecture

```text
User Query
    |
    v
+----------------+
|   Jev Router   |
|                |
| category       |
| complexity     |
+-------+--------+
        |
        v
+-------------------+
| Routing Policy    |
|                   |
| fast              |
| coding            |
| reasoning         |
+---------+---------+
          |
          v
+-------------------+
|    LangChain      |
|                   |
| model abstraction |
| orchestration     |
+---------+---------+
          |
          v
+-------------------+
|    OpenRouter     |
|                   |
| selected LLM      |
+---------+---------+
          |
          v
       Response
```

Jev makes the semantic decision. The application owns the routing policy. LangChain handles model abstraction/orchestration, while OpenRouter provides model access.

## Initial Routes

| Route | Intended workload |
|---|---|
| `fast` | Simple factual questions, summaries, basic transformations |
| `coding` | Programming, debugging, code generation |
| `reasoning` | Complex analysis, multi-step reasoning, difficult technical tasks |

The exact models are configured rather than hard-coded into routing logic so they can be changed without changing the application.

## MVP

The first version will:

1. Accept a user query.
2. Ask Jev to classify the task.
3. Determine task complexity.
4. Convert the decision into a route.
5. Invoke the selected LLM through LangChain/OpenRouter.
6. Return the answer and routing metadata.
7. Log latency, token usage, model selection, and estimated cost.

## Evaluation

The project will compare:

- **Baseline:** every request goes to one strong model.
- **Router:** Jev selects an appropriate model.

Key metrics:

- routing accuracy
- answer quality
- average latency
- estimated cost/request
- strong-model utilization
- fallback rate

The goal is not to claim that routing is universally better. The goal is to measure the trade-offs on a controlled evaluation set.

## Tech Stack

- Python 3.11+
- LangChain
- Jev / TypeSafe Python SDK
- OpenRouter
- FastAPI
- Pydantic
- SQLite
- pytest
- Docker

## Project Status

- [ ] Python project scaffold
- [ ] Jev classification
- [ ] Routing policy
- [ ] OpenRouter provider
- [ ] LangChain model integration
- [ ] API endpoint
- [ ] Request telemetry
- [ ] Evaluation dataset
- [ ] Baseline benchmark
- [ ] Router benchmark
- [ ] Dashboard
- [ ] Docker deployment
- [ ] Resume-ready documentation

## Design Principle

Do not let the LLM decide its own route.

The flow is:

```text
Jev -> typed decision -> deterministic policy -> LangChain -> selected model
```

This keeps the routing policy testable and explainable.
