import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from src.models.schemas import Category, Complexity, Route
from src.policy.router import ROUTING_MATRIX


class EvalQuery(BaseModel):
    """Schema for a single evaluation benchmark query."""
    id: str
    query: str
    expected_category: str = Field(..., alias="expectedCategory")
    expected_complexity: Complexity = Field(..., alias="expectedComplexity")
    expected_route: Optional[Route] = Field(None, alias="expectedRoute")

    model_config = {
        "populate_by_name": True,  # Allows both snake_case and camelCase
    }

    def get_expected_route(self) -> Route:
        """Derives expected route from deterministic matrix if not explicitly set."""
        if self.expected_route:
            return self.expected_route
        if self.expected_category in Category._value2member_map_:
            cat = Category(self.expected_category)
            return ROUTING_MATRIX.get((cat, self.expected_complexity), Route.REASONING)
        # Ambiguous or unknown categories default to REASONING
        return Route.REASONING


def load_dataset(path: str | Path = "data/queries.json") -> List[EvalQuery]:
    """Loads and validates the query benchmark dataset."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found at {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("queries.json must contain a JSON array of query objects.")

    return [EvalQuery(**item) for item in data]


def get_dataset_stats(queries: List[EvalQuery]) -> Dict[str, Any]:
    """Returns distribution of categories and complexities in the dataset."""
    category_counts = {}
    complexity_counts = {}
    route_counts = {}

    for q in queries:
        cat_key = q.expected_category if isinstance(q.expected_category, str) else q.expected_category.value
        comp_key = q.expected_complexity.value if hasattr(q.expected_complexity, "value") else str(q.expected_complexity)
        category_counts[cat_key] = category_counts.get(cat_key, 0) + 1
        complexity_counts[comp_key] = complexity_counts.get(comp_key, 0) + 1
        expected_r = q.get_expected_route().value
        route_counts[expected_r] = route_counts.get(expected_r, 0) + 1

    return {
        "total_queries": len(queries),
        "categories": category_counts,
        "complexities": complexity_counts,
        "expected_routes": route_counts,
    }

