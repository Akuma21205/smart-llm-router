import uuid
from typing import Optional
from src.config import Config
from src.models.schemas import ChatResponse, RoutingMetadata
from src.classifier.jev_client import JevClassifier
from src.policy.router import RoutingPolicy
from src.llm.client import LLMClient
from src.telemetry.collector import TelemetryCollector


class RouterPipeline:
    """
    End-to-End Smart LLM Router Pipeline:
    Query -> Jev Semantic Classification -> Deterministic Policy -> LLM Generation -> Telemetry Response
    """

    def __init__(
        self,
        classifier: Optional[JevClassifier] = None,
        policy: Optional[RoutingPolicy] = None,
        llm_client: Optional[LLMClient] = None,
        telemetry: Optional[TelemetryCollector] = None,
    ):
        self.classifier = classifier or JevClassifier()
        self.policy = policy or RoutingPolicy(confidence_threshold=Config.CONFIDENCE_THRESHOLD)
        self.llm_client = llm_client or LLMClient()
        self.telemetry = telemetry if telemetry is not None else TelemetryCollector()


    def process(self, query: str, request_id: Optional[str] = None) -> ChatResponse:
        req_id = request_id or f"req_{uuid.uuid4().hex[:12]}"

        # Step 1: Jev Classification
        decision, routing_latency_ms = self.classifier.classify(query)

        # Step 2: Deterministic Policy Evaluation
        policy_result = self.policy.evaluate(decision)

        # Step 3: LLM Generation (Primary NVIDIA with OpenRouter Fallback)
        task_name = policy_result.route.value
        llm_result = self.llm_client.generate(prompt=query, task=task_name)

        # Combine fallback details
        fallback_triggered = policy_result.fallback_triggered or llm_result.get("fallback_triggered", False)
        reasons = []
        if policy_result.fallback_triggered and policy_result.fallback_reason:
            reasons.append(f"Policy: {policy_result.fallback_reason}")
        if llm_result.get("fallback_triggered") and llm_result.get("fallback_reason"):
            reasons.append(f"LLM: {llm_result.get('fallback_reason')}")
        fallback_reason = " | ".join(reasons) if reasons else None

        # Build RoutingMetadata
        routing = RoutingMetadata(
            category=decision.category,
            complexity=decision.complexity,
            route=policy_result.route,
            model=llm_result.get("model", "unknown"),
            confidence=decision.confidence,
            fallback_triggered=fallback_triggered,
            fallback_reason=fallback_reason,
            routing_latency_ms=routing_latency_ms,
            generation_latency_ms=llm_result.get("generation_latency_ms"),
            input_tokens=llm_result.get("input_tokens"),
            output_tokens=llm_result.get("output_tokens"),
            estimated_cost_usd=None,
        )

        response = ChatResponse(
            request_id=req_id,
            query=query,
            answer=llm_result.get("content", ""),
            routing=routing,
        )

        # Step 4: Log to Telemetry
        if self.telemetry:
            self.telemetry.record(response)

        return response

