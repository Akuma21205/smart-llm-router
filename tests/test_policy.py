import pytest
from src.models.schemas import Category, Complexity, Route, RoutingDecision
from src.policy.router import RoutingPolicy, ROUTING_MATRIX


def test_confidence_fallback():
    policy = RoutingPolicy(confidence_threshold=0.70)
    decision = RoutingDecision(
        category=Category.GENERAL,
        complexity=Complexity.LOW,
        confidence=0.55,  # Below 0.70
    )
    result = policy.evaluate(decision)

    assert result.route == Route.REASONING
    assert result.fallback_triggered is True
    assert "below threshold" in result.fallback_reason


@pytest.mark.parametrize(
    "category,complexity,expected_route",
    [
        (cat, comp, route)
        for (cat, comp), route in ROUTING_MATRIX.items()
    ],
)
def test_matrix_rules(category, complexity, expected_route):
    policy = RoutingPolicy(confidence_threshold=0.70)
    decision = RoutingDecision(
        category=category,
        complexity=complexity,
        confidence=0.90,  # High confidence
    )
    result = policy.evaluate(decision)

    assert result.route == expected_route
    assert result.fallback_triggered is False
