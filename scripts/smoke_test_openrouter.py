"""
Smoke test for LLM generation (NVIDIA primary + OpenRouter fallback).
"""
import sys
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.llm.client import LLMClient


def test_routes():
    print("=" * 60)
    print("SMOKE TEST: LLM INFERENCE (PRIMARY NVIDIA)")
    print("=" * 60)

    client = LLMClient()

    tasks = ["fast", "coding", "reasoning"]
    for task in tasks:
        print(f"\n--> Testing Route: {task.upper()}")
        res = client.generate(
            prompt="Reply in exactly 5 words confirming you are working.",
            task=task,
            max_tokens=30,
        )
        print(f"    Provider: {res['provider']}")
        print(f"    Model:    {res['model']}")
        print(f"    Latency:  {res['generation_latency_ms']:.1f} ms")
        print(f"    Tokens:   in={res['input_tokens']}, out={res['output_tokens']}")
        print(f"    Content:  {res['content'].strip()}")

    print("\n" + "=" * 60)
    print("SMOKE TEST: OPENROUTER FALLBACK RESILIENCE")
    print("=" * 60)

    # Simulate NVIDIA disabled
    client.nvidia = None
    res = client.generate(
        prompt="Reply in exactly 5 words confirming OpenRouter fallback works.",
        task="fast",
        max_tokens=30,
    )
    print(f"    Provider: {res['provider']}")
    print(f"    Model:    {res['model']}")
    print(f"    Latency:  {res['generation_latency_ms']:.1f} ms")
    print(f"    Tokens:   in={res['input_tokens']}, out={res['output_tokens']}")
    print(f"    Fallback: {res['fallback_triggered']} ({res['fallback_reason']})")
    print(f"    Content:  {res['content'].strip()}")

    print("\n" + "=" * 60)
    print("LLM SMOKE TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    test_routes()
