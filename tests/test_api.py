import pytest
from starlette.testclient import TestClient
from src.api.app import app
from src.api.routes import get_pipeline
from src.models.schemas import (
    ChatResponse,
    RoutingMetadata,
    Category,
    Complexity,
    Route,
)


class MockPipeline:
    def process(self, query: str, request_id: str | None = None) -> ChatResponse:
        return ChatResponse(
            request_id="test_req_123",
            query=query,
            answer="Mock answer for query",
            routing=RoutingMetadata(
                category=Category.GENERAL,
                complexity=Complexity.LOW,
                route=Route.FAST,
                model="mock-model",
                confidence=0.95,
                fallback_triggered=False,
                routing_latency_ms=15.0,
                generation_latency_ms=250.0,
                input_tokens=10,
                output_tokens=20,
            ),
        )


@pytest.fixture
def client():
    # Override pipeline dependency with mock
    app.dependency_overrides[get_pipeline] = lambda: MockPipeline()
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "models" in data


def test_stats_endpoint(client):
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data


def test_chat_endpoint_success(client):
    response = client.post("/chat", json={"query": "Hello world!"})
    assert response.status_code == 200
    data = response.json()
    assert data["request_id"] == "test_req_123"
    assert data["query"] == "Hello world!"
    assert data["answer"] == "Mock answer for query"
    assert data["routing"]["route"] == "fast"
    assert data["routing"]["confidence"] == 0.95


def test_chat_endpoint_validation_error(client):
    # Empty query should fail pydantic min_length=1
    response = client.post("/chat", json={"query": ""})
    assert response.status_code == 422


def test_v1_models(client):
    response = client.get("/v1/models")
    assert response.status_code == 200
    data = response.json()
    model_ids = [m["id"] for m in data["data"]]
    assert "smart-llm-router" in model_ids


def test_v1_chat_completions_json(client):
    payload = {
        "model": "smart-llm-router",
        "messages": [
            {"role": "user", "content": "How do I reverse a string?"}
        ],
        "stream": False,
    }
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "chat.completion"
    assert len(data["choices"]) == 1
    assert "Mock answer for query" in data["choices"][0]["message"]["content"]
    assert "Routed to" in data["choices"][0]["message"]["content"]
    assert "routing" in data


def test_v1_chat_completions_streaming(client):
    payload = {
        "model": "smart-llm-router",
        "messages": [
            {"role": "user", "content": "Tell me a joke"}
        ],
        "stream": True,
    }
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    assert "data: " in response.text
    assert "[DONE]" in response.text


def test_dashboard_endpoint(client):
    response = client.get("/dashboard/")
    assert response.status_code == 200
    assert "Smart LLM Router" in response.text


