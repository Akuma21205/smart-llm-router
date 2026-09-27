# Roadmap

## Phase 0 — Foundation

- [x] Define problem
- [x] Define architecture
- [x] Define initial routing policy
- [x] Define evaluation methodology

## Phase 1 — Jev Prototype

- [ ] Initialize TypeScript project
- [ ] Install AI SDK
- [ ] Configure Jev
- [ ] Send first classification request
- [ ] Validate typed result
- [ ] Add Jev smoke tests

## Phase 2 — OpenRouter

- [ ] Configure OpenRouter
- [ ] Choose one fast model
- [ ] Choose one coding model
- [ ] Choose one reasoning model
- [ ] Test each model independently
- [ ] Capture usage metadata

## Phase 3 — Router

- [ ] Implement routing types
- [ ] Implement deterministic policy
- [ ] Add confidence threshold
- [ ] Add fallback route
- [ ] Connect Jev to policy
- [ ] Connect policy to OpenRouter

## Phase 4 — API

- [ ] Build `POST /chat`
- [ ] Validate request body
- [ ] Return routing metadata
- [ ] Add request IDs
- [ ] Add error handling

## Phase 5 — Observability

- [ ] SQLite telemetry
- [ ] Routing latency
- [ ] Generation latency
- [ ] Token usage
- [ ] Estimated cost
- [ ] Selected model
- [ ] Failure/fallback tracking

## Phase 6 — Evaluation

- [ ] Create 150-query dataset
- [ ] Run baseline
- [ ] Run router
- [ ] Compare quality
- [ ] Compare latency
- [ ] Compare cost
- [ ] Compare strong-model usage
- [ ] Test confidence thresholds

## Phase 7 — Dashboard

- [ ] Request count
- [ ] Route distribution
- [ ] Model distribution
- [ ] Average latency
- [ ] Estimated cost
- [ ] Routing confidence
- [ ] Error rate

## Phase 8 — Production Polish

- [ ] Dockerfile
- [ ] Docker Compose
- [ ] Health endpoint
- [ ] Configuration validation
- [ ] README examples
- [ ] Architecture diagram
- [ ] Benchmark report
- [ ] Resume bullets

## Final Deliverable

The final repository should allow someone to:

```bash
git clone ...
npm install
cp .env.example .env
npm run dev
```

Then send:

```http
POST /chat
Content-Type: application/json

{
  "query": "Debug this Python recursion error..."
}
```

and receive:

```json
{
  "answer": "...",
  "routing": {
    "category": "coding",
    "complexity": "medium",
    "route": "coding",
    "model": "..."
  }
}
```
