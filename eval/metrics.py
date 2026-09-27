from typing import List, Dict, Any


def compute_metrics(
    baseline_results: List[Dict[str, Any]],
    router_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    n = len(router_results)
    if n == 0:
        return {}

    # Routing Accuracies
    cat_accuracy = sum(1 for r in router_results if r["category_correct"]) / n * 100.0
    comp_accuracy = sum(1 for r in router_results if r["complexity_correct"]) / n * 100.0
    route_accuracy = sum(1 for r in router_results if r["route_correct"]) / n * 100.0

    # Latencies
    b_avg_latency = sum(r["latency_ms"] for r in baseline_results) / len(baseline_results) if baseline_results else 0.0
    r_avg_latency = sum(r["total_latency_ms"] for r in router_results) / n
    r_avg_routing_latency = sum(r["routing_latency_ms"] for r in router_results) / n
    r_avg_gen_latency = sum(r["generation_latency_ms"] for r in router_results) / n
    latency_reduction = ((b_avg_latency - r_avg_latency) / b_avg_latency * 100.0) if b_avg_latency > 0 else 0.0

    # Tokens
    b_total_tokens = sum(r["total_tokens"] for r in baseline_results) if baseline_results else 0
    r_total_tokens = sum(r["total_tokens"] for r in router_results)

    # Route and Model Distributions
    routes_count = {}
    for r in router_results:
        routes_count[r["selected_route"]] = routes_count.get(r["selected_route"], 0) + 1

    # Strong model utilization (reasoning route %)
    reasoning_count = routes_count.get("reasoning", 0)
    strong_model_utilization = (reasoning_count / n) * 100.0

    # Fallback Rate
    fallback_count = sum(1 for r in router_results if r["fallback_triggered"])
    fallback_rate = (fallback_count / n) * 100.0

    return {
        "total_queries": n,
        "routing_accuracy": {
            "category_accuracy_pct": round(cat_accuracy, 1),
            "complexity_accuracy_pct": round(comp_accuracy, 1),
            "route_accuracy_pct": round(route_accuracy, 1),
        },
        "latency": {
            "baseline_avg_ms": round(b_avg_latency, 1),
            "router_avg_total_ms": round(r_avg_latency, 1),
            "router_avg_classification_ms": round(r_avg_routing_latency, 1),
            "router_avg_generation_ms": round(r_avg_gen_latency, 1),
            "latency_reduction_pct": round(latency_reduction, 1),
        },
        "tokens": {
            "baseline_total": b_total_tokens,
            "router_total": r_total_tokens,
        },
        "strong_model_usage_pct": round(strong_model_utilization, 1),
        "fallback_rate_pct": round(fallback_rate, 1),
        "route_distribution": routes_count,
    }


def print_comparison_table(metrics: Dict[str, Any]):
    """Prints benchmark summary matching docs/EVALUATION.md format."""
    print("\n" + "=" * 62)
    print(f"{'METRIC':<30} | {'BASELINE':<12} | {'JEV ROUTER':<12}")
    print("-" * 62)
    lat = metrics.get("latency", {})
    acc = metrics.get("routing_accuracy", {})

    print(f"{'Avg Latency':<30} | {lat.get('baseline_avg_ms', 0):>9.1f} ms | {lat.get('router_avg_total_ms', 0):>9.1f} ms")
    print(f"{'Strong Model Usage':<30} | {'100.0 %':>12} | {metrics.get('strong_model_usage_pct', 0):>10.1f} %")
    print(f"{'Route Accuracy':<30} | {'-':>12} | {acc.get('route_accuracy_pct', 0):>10.1f} %")
    print(f"{'Category Accuracy':<30} | {'-':>12} | {acc.get('category_accuracy_pct', 0):>10.1f} %")
    print(f"{'Complexity Accuracy':<30} | {'-':>12} | {acc.get('complexity_accuracy_pct', 0):>10.1f} %")
    print(f"{'Fallback Rate':<30} | {'-':>12} | {metrics.get('fallback_rate_pct', 0):>10.1f} %")
    print("=" * 62)
