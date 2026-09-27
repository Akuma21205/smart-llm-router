"""
Benchmark Evaluation Runner
Compares Baseline (single strong model) vs. Jev Smart LLM Router.
"""
import sys
import json
import argparse
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from eval.dataset import load_dataset, get_dataset_stats
from eval.baseline import BaselineRunner
from eval.benchmark import RouterBenchmarkRunner
from eval.metrics import compute_metrics, print_comparison_table


def main():
    parser = argparse.ArgumentParser(description="Evaluate Smart LLM Router against Baseline")
    parser.add_argument(
        "--dataset",
        type=str,
        default="data/queries.json",
        help="Path to evaluation dataset JSON",
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        help="Number of queries to sample (default: all queries in dataset)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="eval_results.json",
        help="Path to save detailed evaluation results",
    )
    parser.add_argument(
        "--skip-baseline",
        action="store_true",
        help="Skip baseline run (router benchmark only)",
    )

    args = parser.parse_args()

    print("=" * 62)
    print("SMART LLM ROUTER — EVALUATION HARNESS")
    print("=" * 62)

    # 1. Load dataset
    queries = load_dataset(args.dataset)
    stats = get_dataset_stats(queries)
    print(f"Loaded {len(queries)} queries from {args.dataset}")
    print(f"Distribution: Categories={stats['categories']}, Complexities={stats['complexities']}")

    if args.sample and args.sample < len(queries):
        per_cat = max(1, args.sample // 5)
        by_cat = {}
        for q in queries:
            by_cat.setdefault(q.expected_category, []).append(q)
        sampled = []
        for cat, q_list in by_cat.items():
            sampled.extend(q_list[:per_cat])
        queries = sampled[:args.sample]
        print(f"Sampled {len(queries)} balanced queries across all 5 categories.\n", flush=True)

    # 2. Run Baseline
    baseline_results = []
    if not args.skip_baseline:
        print("\n--- PHASE 1: Running Baseline (Single Strong Model) ---")
        baseline_runner = BaselineRunner()
        baseline_results = baseline_runner.run_all(queries)
    else:
        print("\n--- Skipping Baseline as requested ---")

    # 3. Run Router Benchmark
    print("\n--- PHASE 2: Running Jev Smart Router Pipeline ---")
    router_runner = RouterBenchmarkRunner()
    router_results = router_runner.run_all(queries)

    # 4. Compute & Print Metrics
    print("\n--- PHASE 3: Benchmark Results ---")
    metrics = compute_metrics(baseline_results, router_results)
    print_comparison_table(metrics)

    # 5. Save detailed report
    output_data = {
        "dataset_stats": stats,
        "sample_size": len(queries),
        "metrics": metrics,
        "baseline_results": baseline_results,
        "router_results": router_results,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"\nDetailed evaluation report saved to: {args.output}")


if __name__ == "__main__":
    main()
