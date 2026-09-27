import sys
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.classifier.jev_client import JevClassifier
from src.policy.router import RoutingPolicy

TEST_QUERIES = [
    "What is the capital of France?",
    "Write a Python function to check if a string is a palindrome.",
    "If all bloops are razzies and all razzies are lazzies, are all bloops definitely lazzies? Prove it step by step.",
    "Write a short, moody poem about the rain in Tokyo at 2 AM.",
]


def main():
    print("=" * 60)
    print("SMOKE TEST: JEV CLASSIFICATION & ROUTING POLICY")
    print("=" * 60)

    classifier = JevClassifier()
    policy = RoutingPolicy()

    for idx, query in enumerate(TEST_QUERIES, start=1):
        print(f"\n[{idx}] Query: {query}")
        decision, latency_ms = classifier.classify(query)
        policy_result = policy.evaluate(decision)

        print(f"    Category:   {decision.category.value}")
        print(f"    Complexity: {decision.complexity.value}")
        print(f"    Confidence: {decision.confidence:.2f}")
        print(f"    Latency:    {latency_ms:.1f} ms")
        print(f"    --> Route:  {policy_result.route.value.upper()}")
        if policy_result.fallback_triggered:
            print(f"    (Fallback triggered: {policy_result.fallback_reason})")

    print("\n" + "=" * 60)
    print("JEV SMOKE TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()
