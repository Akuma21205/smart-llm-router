from enum import Enum
from typing import Optional, Dict
from pydantic import BaseModel, Field


class Category(str, Enum):
    GENERAL = "general"
    CODING = "coding"
    REASONING = "reasoning"
    CREATIVE = "creative"


class Complexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Route(str, Enum):
    FAST = "fast"
    CODING = "coding"
    REASONING = "reasoning"


class RoutingDecision(BaseModel):
    """The raw semantic classification produced by Jev."""
    category: Category
    complexity: Complexity
    confidence: float = Field(..., ge=0.0, le=1.0)
    raw_model: Optional[str] = None
    category_probabilities: Optional[Dict[str, float]] = None
    complexity_probabilities: Optional[Dict[str, float]] = None


class RoutingMetadata(BaseModel):
    """Execution and routing metadata returned with the answer and logged to telemetry."""
    category: Category
    complexity: Complexity
    route: Route
    model: str
    confidence: float
    fallback_triggered: bool = False
    fallback_reason: Optional[str] = None
    routing_latency_ms: float = 0.0
    generation_latency_ms: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    estimated_cost_usd: Optional[float] = None


class ChatRequest(BaseModel):
    """Incoming user chat query."""
    query: str = Field(..., min_length=1, description="The user query to route and process.")


class ChatResponse(BaseModel):
    """Final response returned to the user."""
    request_id: str
    query: str
    answer: str
    routing: RoutingMetadata
