from typing import Optional, Dict, Any
from src.models.schemas import ChatResponse
from src.telemetry.db import get_db_connection, init_db


class TelemetryCollector:
    """Logs pipeline requests and queries usage metrics."""

    def __init__(self):
        init_db()

    def record(self, response: ChatResponse):
        """Saves a ChatResponse and its routing metadata to SQLite."""
        routing = response.routing
        conn = get_db_connection()
        with conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO request_telemetry (
                    request_id, query, category, complexity, route, model,
                    confidence, fallback_triggered, fallback_reason,
                    routing_latency_ms, generation_latency_ms,
                    input_tokens, output_tokens, estimated_cost_usd
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    response.request_id,
                    response.query,
                    routing.category.value,
                    routing.complexity.value,
                    routing.route.value,
                    routing.model,
                    routing.confidence,
                    1 if routing.fallback_triggered else 0,
                    routing.fallback_reason,
                    routing.routing_latency_ms,
                    routing.generation_latency_ms,
                    routing.input_tokens,
                    routing.output_tokens,
                    routing.estimated_cost_usd,
                ),
            )
        conn.close()

    def get_summary_stats(self) -> Dict[str, Any]:
        """Returns aggregate metrics across all processed queries."""
        conn = get_db_connection()
        cursor = conn.cursor()

        total = cursor.execute("SELECT COUNT(*) FROM request_telemetry").fetchone()[0]
        if total == 0:
            conn.close()
            return {"total_requests": 0}

        avg_latencies = cursor.execute("""
            SELECT 
                AVG(routing_latency_ms) as avg_routing_ms,
                AVG(generation_latency_ms) as avg_generation_ms,
                SUM(input_tokens) as total_in_tokens,
                SUM(output_tokens) as total_out_tokens,
                SUM(fallback_triggered) as total_fallbacks
            FROM request_telemetry
        """).fetchone()

        route_counts = dict(
            cursor.execute("SELECT route, COUNT(*) FROM request_telemetry GROUP BY route").fetchall()
        )
        model_counts = dict(
            cursor.execute("SELECT model, COUNT(*) FROM request_telemetry GROUP BY model").fetchall()
        )
        category_counts = dict(
            cursor.execute("SELECT category, COUNT(*) FROM request_telemetry GROUP BY category").fetchall()
        )
        conn.close()

        return {
            "total_requests": total,
            "avg_routing_latency_ms": round(avg_latencies["avg_routing_ms"] or 0, 1),
            "avg_generation_latency_ms": round(avg_latencies["avg_generation_ms"] or 0, 1),
            "total_input_tokens": avg_latencies["total_in_tokens"] or 0,
            "total_output_tokens": avg_latencies["total_out_tokens"] or 0,
            "fallback_count": avg_latencies["total_fallbacks"] or 0,
            "route_distribution": route_counts,
            "model_distribution": model_counts,
            "category_distribution": category_counts,
        }

    def get_recent_requests(self, limit: int = 50) -> list[Dict[str, Any]]:
        """Returns the most recent logged requests from SQLite."""
        conn = get_db_connection()
        cursor = conn.cursor()
        rows = cursor.execute(
            """
            SELECT request_id, timestamp, query, category, complexity, route,
                   model, confidence, fallback_triggered, fallback_reason,
                   routing_latency_ms, generation_latency_ms, input_tokens, output_tokens
            FROM request_telemetry
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

