from dataclasses import dataclass
from typing import Optional, Tuple, Dict
from src.models.schemas import Category, Complexity, Route, RoutingDecision


@dataclass(frozen=True)
class PolicyResult:
    """The result of applying routing policy to a semantic decision."""
    route: Route
    fallback_triggered: bool = False
    fallback_reason: Optional[str] = None


# Deterministic matrix mapping (Category, Complexity) -> Route
ROUTING_MATRIX: Dict[Tuple[Category, Complexity], Route] = {
    # General
    (Category.GENERAL, Complexity.LOW): Route.FAST,
    (Category.GENERAL, Complexity.MEDIUM): Route.FAST,
    (Category.GENERAL, Complexity.HIGH): Route.REASONING,

    # Coding
    (Category.CODING, Complexity.LOW): Route.CODING,
    (Category.CODING, Complexity.MEDIUM): Route.CODING,
    (Category.CODING, Complexity.HIGH): Route.REASONING,

    # Reasoning
    (Category.REASONING, Complexity.LOW): Route.REASONING,
    (Category.REASONING, Complexity.MEDIUM): Route.REASONING,
    (Category.REASONING, Complexity.HIGH): Route.REASONING,

    # Creative
    (Category.CREATIVE, Complexity.LOW): Route.FAST,
    (Category.CREATIVE, Complexity.MEDIUM): Route.FAST,
    (Category.CREATIVE, Complexity.HIGH): Route.REASONING,
}


class RoutingPolicy:
    """
    Deterministic rule engine that maps Jev's semantic classification
    to an infrastructure route (fast, coding, reasoning).
    """

    def __init__(
        self,
        confidence_threshold: float = 0.70,
        fallback_route: Route = Route.REASONING,
    ):
        self.confidence_threshold = confidence_threshold
        self.fallback_route = fallback_route

    def evaluate(self, decision: RoutingDecision) -> PolicyResult:
        # Rule 1: Check confidence threshold
        if decision.confidence < self.confidence_threshold:
            return PolicyResult(
                route=self.fallback_route,
                fallback_triggered=True,
                fallback_reason=(
                    f"Confidence {decision.confidence:.2f} is below "
                    f"threshold {self.confidence_threshold:.2f}"
                ),
            )

        # Rule 2: Lookup in deterministic matrix
        key = (decision.category, decision.complexity)
        route = ROUTING_MATRIX.get(key)

        if route is None:
            # Fallback if unknown combination
            return PolicyResult(
                route=self.fallback_route,
                fallback_triggered=True,
                fallback_reason=f"Unknown combination category={decision.category}, complexity={decision.complexity}",
            )

        return PolicyResult(route=route, fallback_triggered=False, fallback_reason=None)
