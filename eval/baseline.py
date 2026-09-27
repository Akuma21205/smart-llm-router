import time
from typing import List, Dict, Any
from eval.dataset import EvalQuery
from src.llm.client import LLMClient
from src.config import Config


class BaselineRunner:
    """Executes all queries against a single strong model (the benchmark baseline)."""

    def __init__(self, llm_client: LLMClient | None = None):
        self.client = llm_client or LLMClient()
        self.model = Config.NVIDIA_HEAVY_MODEL

    def run_query(self, query_item: EvalQuery) -> Dict[str, Any]:
        start = time.perf_counter()
        result = self.client.generate(prompt=query_item.query, task="heavy")
        latency_ms = (time.perf_counter() - start) * 1000

        return {
            "id": query_item.id,
            "query": query_item.query,
            "answer": result.get("content", ""),
            "model": result.get("model", self.model),
            "provider": result.get("provider", "unknown"),
            "latency_ms": latency_ms,
            "input_tokens": result.get("input_tokens") or 0,
            "output_tokens": result.get("output_tokens") or 0,
            "total_tokens": (result.get("input_tokens") or 0) + (result.get("output_tokens") or 0),
        }

    def run_all(self, queries: List[EvalQuery]) -> List[Dict[str, Any]]:
        results = []
        for i, q in enumerate(queries, start=1):
            print(f"  [Baseline] ({i}/{len(queries)}) Query: {q.id} - {q.query[:50]}...")
            res = self.run_query(q)
            results.append(res)
        return results
