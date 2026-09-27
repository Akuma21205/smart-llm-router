import time
import logging
from typing import Tuple, Optional
from typesafe_sdk import TypeSafeClient

from src.config import Config
from src.models.schemas import Category, Complexity, RoutingDecision
from src.classifier.prompts import CLASSIFIER_QUESTIONS

logger = logging.getLogger(__name__)


class JevClassifier:
    """Classifies user queries semantically using Jev."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.JEV_API_KEY
        if not self.api_key:
            raise ValueError("JEV_API_KEY is not configured in .env or environment.")
        self.client = TypeSafeClient(api_key=self.api_key)

    def classify(self, query: str) -> Tuple[RoutingDecision, float]:
        """
        Classifies the query.
        Returns:
            Tuple[RoutingDecision, routing_latency_ms]
        """
        start_time = time.perf_counter()

        try:
            response = self.client.system_one(
                state={"query": query},
                questions=CLASSIFIER_QUESTIONS,
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            answers = response.answers
            cat_ans = answers.get("category")
            comp_ans = answers.get("complexity")

            cat_choice = cat_ans.choice if cat_ans else "general"
            comp_choice = comp_ans.choice if comp_ans else "high"

            cat_val = Category(cat_choice) if cat_choice in Category._value2member_map_ else Category.GENERAL
            comp_val = Complexity(comp_choice) if comp_choice in Complexity._value2member_map_ else Complexity.HIGH

            cat_conf = float(cat_ans.confidence) if cat_ans and cat_ans.confidence is not None else 0.5
            comp_conf = float(comp_ans.confidence) if comp_ans and comp_ans.confidence is not None else 0.5

            # Conservative confidence: weakest link
            overall_confidence = min(cat_conf, comp_conf)

            decision = RoutingDecision(
                category=cat_val,
                complexity=comp_val,
                confidence=overall_confidence,
                raw_model=response.model if hasattr(response, "model") else None,
                category_probabilities=cat_ans.probabilities if cat_ans else None,
                complexity_probabilities=comp_ans.probabilities if comp_ans else None,
            )
            return decision, elapsed_ms

        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            logger.error(f"Jev classification failed: {e}. Using conservative fallback.")
            fallback_decision = RoutingDecision(
                category=Category.GENERAL,
                complexity=Complexity.HIGH,
                confidence=0.0,
                raw_model="fallback_error",
            )
            return fallback_decision, elapsed_ms
