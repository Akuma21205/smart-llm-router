import json
import time
import urllib.request
from typing import Dict, Any

SERVER_URL = "http://localhost:8000/v1/chat/completions"

TEST_PROMPTS = [
    {
        "name": "Test 1: Fast / General Fact",
        "query": "What is the speed of sound in air at sea level in meters per second? Answer in one short sentence.",
        "expected_route": "FAST",
    },
    {
        "name": "Test 2: Coding Implementation",
        "query": "Write a clean Python function `is_anagram(s1, s2)` using Counter or sorting, with docstring.",
        "expected_route": "CODING",
    },
    {
        "name": "Test 3: Multi-step Reasoning Puzzle",
        "query": "If three cats catch three mice in three minutes, how many cats are needed to catch 100 mice in 100 minutes? Walk through the mathematical rate.",
        "expected_route": "REASONING",
    },
    {
        "name": "Test 4: Masked / Ambiguous Safeguard",
        "query": "Investigate how [MASK] protocol resolves split-brain in [REDACTED] cluster without an odd-numbered quorum.",
        "expected_route": "REASONING (Safeguard)",
    },
]


def test_streaming_query(test_case: Dict[str, Any]):
    print(f"\n=======================================================")
    print(f"▶ {test_case['name']}")
    print(f"Query: \"{test_case['query']}\"")
    print(f"Target Route: {test_case['expected_route']}")
    print(f"-------------------------------------------------------")

    payload = {
        "model": "smart-llm-router",
        "messages": [{"role": "user", "content": test_case["query"]}],
        "stream": True,
    }

    req = urllib.request.Request(
        SERVER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    t0 = time.time()
    chunks = []
    with urllib.request.urlopen(req) as resp:
        for line in resp:
            decoded = line.decode("utf-8").strip()
            if decoded.startswith("data: "):
                raw_chunk = decoded[6:]
                if raw_chunk == "[DONE]":
                    break
                try:
                    data = json.loads(raw_chunk)
                    delta = data["choices"][0]["delta"].get("content", "")
                    chunks.append(delta)
                except Exception:
                    pass

    elapsed = time.time() - t0
    full_answer = "".join(chunks)

    # Separate content from routing badge
    parts = full_answer.split("---")
    main_text = parts[0].strip()
    badge_text = ("---" + parts[1]).strip() if len(parts) > 1 else "(No badge appended)"

    print(f"⏱ Total Round-Trip: {elapsed:.2f}s")
    print(f"\nResponse Text Preview:")
    print(main_text[:200] + ("..." if len(main_text) > 200 else ""))
    print(f"\nOpen WebUI Routing Badge:")
    print(badge_text)


if __name__ == "__main__":
    print("Testing Smart LLM Router via OpenAI-Compatible Endpoint...")
    for tc in TEST_PROMPTS:
        try:
            test_streaming_query(tc)
        except Exception as e:
            print(f"❌ Error during {tc['name']}: {e}")
    print("\n✅ All automated Open WebUI compatibility tests completed!")
