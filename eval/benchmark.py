from typing import List, Dict, Any
from eval.dataset import EvalQuery
from src.pipeline import RouterPipeline


class RouterBenchmarkRunner:
    """Executes all queries through the Jev Smart Router Pipeline."""

    def __init__(self, pipeline: RouterPipeline | None = None):
        self.pipeline = pipeline or RouterPipeline()

    def run_query(self, query_item: EvalQuery) -> Dict[str, Any]:
        response = self.pipeline.process(query=query_item.query, request_id=query_item.id)
        routing = response.routing

        expected_cat = query_item.expected_category if isinstance(query_item.expected_category, str) else query_item.expected_category.value
        expected_comp = query_item.expected_complexity.value if hasattr(query_item.expected_complexity, "value") else str(query_item.expected_complexity)
        expected_route = query_item.get_expected_route().value

        if expected_cat == "ambiguous":
            cat_correct = (routing.route.value == "reasoning" or routing.fallback_triggered or routing.confidence < 0.70)
        else:
            cat_correct = (routing.category.value == expected_cat)

        comp_correct = (routing.complexity.value == expected_comp)
        route_correct = (routing.route.value == expected_route)

        total_latency_ms = routing.routing_latency_ms + (routing.generation_latency_ms or 0.0)
        total_tokens = (routing.input_tokens or 0) + (routing.output_tokens or 0)

        return {
            "id": query_item.id,
            "query": query_item.query,
            "answer": response.answer,
            "selected_route": routing.route.value,
            "expected_route": expected_route,
            "selected_category": routing.category.value,
            "expected_category": expected_cat,
            "selected_complexity": routing.complexity.value,
            "expected_complexity": expected_comp,
            "confidence": routing.confidence,
            "model": routing.model,
            "fallback_triggered": routing.fallback_triggered,
            "fallback_reason": routing.fallback_reason,
            "category_correct": cat_correct,
            "complexity_correct": comp_correct,
            "route_correct": route_correct,
            "routing_latency_ms": routing.routing_latency_ms,
            "generation_latency_ms": routing.generation_latency_ms or 0.0,
            "total_latency_ms": total_latency_ms,
            "input_tokens": routing.input_tokens or 0,
            "output_tokens": routing.output_tokens or 0,
            "total_tokens": total_tokens,
        }

    def run_all(self, queries: List[EvalQuery]) -> List[Dict[str, Any]]:
        results = []
        for i, q in enumerate(queries, start=1):
            print(f"  [Router] ({i}/{len(queries)}) Query: {q.id} - {q.query[:50]}...")
            res = self.run_query(q)
            results.append(res)
        return results
