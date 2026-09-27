import time
import json
import asyncio
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from src.pipeline import RouterPipeline
from src.api.routes import get_pipeline

openai_router = APIRouter(tags=["OpenAI Compatible"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "smart-llm-router"
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False


AVAILABLE_MODELS = [
    {
        "id": "smart-llm-router",
        "object": "model",
        "created": 1700000000,
        "owned_by": "smart-llm-router",
        "description": "Dynamic semantic routing using Jev + deterministic policies",
    },
    {
        "id": "smart-router-fast",
        "object": "model",
        "created": 1700000000,
        "owned_by": "smart-llm-router",
        "description": "Forces the fast route",
    },
    {
        "id": "smart-router-coding",
        "object": "model",
        "created": 1700000000,
        "owned_by": "smart-llm-router",
        "description": "Forces the coding route",
    },
    {
        "id": "smart-router-reasoning",
        "object": "model",
        "created": 1700000000,
        "owned_by": "smart-llm-router",
        "description": "Forces the reasoning route",
    },
]


@openai_router.get("/v1/models", summary="List OpenAI-compatible models")
@openai_router.get("/models", include_in_schema=False)
async def list_models():
    """Lists available router models for Open WebUI and OpenAI-compatible clients."""
    return {
        "object": "list",
        "data": AVAILABLE_MODELS,
    }


def _format_routing_badge(routing) -> str:
    """Creates a discrete markdown footer highlighting Jev's routing decision."""
    route_name = routing.route.value.upper()
    cat = routing.category.value
    comp = routing.complexity.value
    conf = f"{routing.confidence:.0%}"
    tot_ms = routing.routing_latency_ms + (routing.generation_latency_ms or 0)
    fb_str = " *(Fallback)*" if routing.fallback_triggered else ""

    return (
        f"\n\n---\n"
        f"*⚡ Routed to **`{route_name}`** (`{routing.model}`){fb_str} | "
        f"Intent: `{cat}` (`{comp}`, Conf: {conf}) | Total: `{tot_ms:.0f}ms`*"
    )


@openai_router.post("/v1/chat/completions", summary="OpenAI-compatible chat completion")
@openai_router.post("/chat/completions", include_in_schema=False)
async def chat_completions(
    request: ChatCompletionRequest,
    pipeline: RouterPipeline = Depends(get_pipeline),
):
    """
    OpenAI-compatible endpoint supporting both standard JSON and SSE streaming.
    Extracts the latest user query, routes it via Jev, and returns responses formatted for Open WebUI.
    """
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty.")

    # Extract the last user message as the query to route
    user_query = None
    for msg in reversed(request.messages):
        if msg.role.lower() == "user":
            user_query = msg.content
            break

    if not user_query:
        user_query = request.messages[-1].content

    # Execute through smart router pipeline
    response = pipeline.process(query=user_query)
    badge = _format_routing_badge(response.routing)
    full_content = response.answer + badge
    created_time = int(time.time())
    completion_id = f"chatcmpl-{response.request_id}"

    # Handle streaming response for Open WebUI
    if request.stream:
        async def event_generator():
            words = full_content.split(" ")
            for i, word in enumerate(words):
                chunk_text = word + (" " if i < len(words) - 1 else "")
                chunk = {
                    "id": completion_id,
                    "object": "chat.completion.chunk",
                    "created": created_time,
                    "model": response.routing.model,
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"content": chunk_text},
                            "finish_reason": None,
                        }
                    ],
                }
                yield f"data: {json.dumps(chunk)}\n\n"
                await asyncio.sleep(0.015)  # Smooth typewriter effect

            # Final closing chunk
            final_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created_time,
                "model": response.routing.model,
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            }
            yield f"data: {json.dumps(final_chunk)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    # Non-streaming standard response
    return {
        "id": completion_id,
        "object": "chat.completion",
        "created": created_time,
        "model": response.routing.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": full_content,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": response.routing.input_tokens or 0,
            "completion_tokens": response.routing.output_tokens or 0,
            "total_tokens": (response.routing.input_tokens or 0) + (response.routing.output_tokens or 0),
        },
        "routing": response.routing.model_dump(),
    }
