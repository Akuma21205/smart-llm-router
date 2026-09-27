from fastapi import APIRouter, HTTPException, Depends
from src.config import Config
from src.models.schemas import ChatRequest, ChatResponse
from src.pipeline import RouterPipeline
from src.telemetry.collector import TelemetryCollector

router = APIRouter()

# Global pipeline and collector instances
_pipeline: RouterPipeline | None = None
_telemetry: TelemetryCollector | None = None


def get_pipeline() -> RouterPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = RouterPipeline()
    return _pipeline


def get_telemetry() -> TelemetryCollector:
    global _telemetry
    if _telemetry is None:
        _telemetry = TelemetryCollector()
    return _telemetry


@router.post("/chat", response_model=ChatResponse, summary="Route and process a user query")
async def chat(request: ChatRequest, pipeline: RouterPipeline = Depends(get_pipeline)):
    """
    Classifies the user query semantically with Jev, selects an optimal route,
    invokes the appropriate model, logs telemetry, and returns the answer.
    """
    try:
        response = pipeline.process(query=request.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Routing or generation failed: {str(e)}")


@router.get("/health", summary="Health check and configuration status")
async def health():
    """Returns system status, active providers, and model mappings."""
    return {
        "status": "healthy",
        "primary_provider": "nvidia" if Config.NVIDIA_API_KEY else "disabled",
        "fallback_provider": "openrouter" if Config.OPENROUTER_API_KEY else "disabled",
        "jev_configured": bool(Config.JEV_API_KEY),
        "confidence_threshold": Config.CONFIDENCE_THRESHOLD,
        "models": {
            "fast": Config.NVIDIA_FAST_MODEL,
            "coding": Config.NVIDIA_CODING_MODEL,
            "reasoning": Config.NVIDIA_REASONING_MODEL,
            "openrouter_fallback": Config.OPENROUTER_FALLBACK_MODEL,
        },
    }


@router.get("/stats", summary="Get aggregated telemetry metrics")
async def stats(telemetry: TelemetryCollector = Depends(get_telemetry)):
    """Returns total request counts, average latencies, token usage, and route distribution."""
    return telemetry.get_summary_stats()


@router.get("/telemetry/recent", summary="Get recent logged requests")
async def recent_requests(limit: int = 50, telemetry: TelemetryCollector = Depends(get_telemetry)):
    """Returns recent requests with routing metadata for dashboard tables and inspectors."""
    return telemetry.get_recent_requests(limit=limit)

