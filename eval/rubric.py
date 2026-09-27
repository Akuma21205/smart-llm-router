from typing import Optional
from pydantic import BaseModel, Field


class QualityScore(BaseModel):
    """Rubric score for an LLM response."""
    correctness: float = Field(..., ge=1.0, le=5.0)
    relevance: float = Field(..., ge=1.0, le=5.0)
    completeness: float = Field(..., ge=1.0, le=5.0)
    instruction_following: float = Field(..., ge=1.0, le=5.0)
    overall: float = 0.0
    reasoning: Optional[str] = None

    def model_post_init(self, __context):
        if self.overall == 0.0:
            self.overall = round(
                (self.correctness + self.relevance + self.completeness + self.instruction_following) / 4.0,
                2
            )
