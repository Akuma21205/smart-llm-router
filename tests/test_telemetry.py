import tempfile
from pathlib import Path
import pytest

from src.models.schemas import (
    ChatResponse,
    RoutingMetadata,
    Category,
    Complexity,
    Route,
)
from src.telemetry.collector import TelemetryCollector
from src.config import Config


@pytest.fixture
def temp_telemetry(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_db = Path(tmpdir) / "test_telemetry.db"
        monkeypatch.setattr(Config, "DB_PATH", str(temp_db))
        collector = TelemetryCollector()
        yield collector


def test_telemetry_record_and_summary(temp_telemetry):
    # Initially empty
    stats = temp_telemetry.get_summary_stats()
    assert stats["total_requests"] == 0

    # Record first response
    resp1 = ChatResponse(
        request_id="req_1",
        query="What is python?",
        answer="A programming language",
        routing=RoutingMetadata(
            category=Category.CODING,
            complexity=Complexity.LOW,
            route=Route.CODING,
            model="test-coder",
            confidence=0.88,
            fallback_triggered=False,
            routing_latency_ms=100.0,
            generation_latency_ms=500.0,
            input_tokens=15,
            output_tokens=30,
        ),
    )
    temp_telemetry.record(resp1)

    # Record second response (with fallback)
    resp2 = ChatResponse(
        request_id="req_2",
        query="Complex problem",
        answer="Detailed steps",
        routing=RoutingMetadata(
            category=Category.REASONING,
            complexity=Complexity.HIGH,
            route=Route.REASONING,
            model="test-reasoner",
            confidence=0.60,
            fallback_triggered=True,
            fallback_reason="Low confidence",
            routing_latency_ms=120.0,
            generation_latency_ms=1000.0,
            input_tokens=25,
            output_tokens=70,
        ),
    )
    temp_telemetry.record(resp2)

    stats = temp_telemetry.get_summary_stats()
    assert stats["total_requests"] == 2
    assert stats["avg_routing_latency_ms"] == 110.0
    assert stats["avg_generation_latency_ms"] == 750.0
    assert stats["total_input_tokens"] == 40
    assert stats["total_output_tokens"] == 100
    assert stats["fallback_count"] == 1
    assert stats["route_distribution"] == {"coding": 1, "reasoning": 1}
