"""Step 1: define exactly what the LLM judge evaluates.

This module contains no model or Azure integration. It is the stable contract that
future prompts, API calls, datasets, and metrics will use.
"""

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator


class Criterion(str, Enum):
    """The only quality dimensions evaluated by the first judge."""

    CORRECTNESS = "correctness"
    RELEVANCE = "relevance"
    COMPLETENESS = "completeness"
    CLARITY = "clarity"


class Decision(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"


class CriterionDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    description: str
    weight: float = Field(gt=0, le=1)


CRITERIA: Dict[Criterion, CriterionDefinition] = {
    Criterion.CORRECTNESS: CriterionDefinition(
        description=(
            "The answer is factually consistent with the supplied reference "
            "and contains no material errors."
        ),
        weight=0.40,
    ),
    Criterion.RELEVANCE: CriterionDefinition(
        description="The answer directly addresses the user's question.",
        weight=0.25,
    ),
    Criterion.COMPLETENESS: CriterionDefinition(
        description="The answer covers the important information needed by the user.",
        weight=0.20,
    ),
    Criterion.CLARITY: CriterionDefinition(
        description="The answer is understandable, precise, and well organized.",
        weight=0.15,
    ),
}


class TaskDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    objective: str
    score_min: int
    score_max: int
    pass_threshold: float
    minimum_critical_score: int
    target_human_agreement: float
    excluded_dimensions: List[str]


TASK_DEFINITION = TaskDefinition(
    name="reference_based_answer_quality",
    objective=(
        "Evaluate an AI-generated answer against a user question and supplied "
        "reference information."
    ),
    score_min=1,
    score_max=5,
    pass_threshold=3.5,
    minimum_critical_score=3,
    target_human_agreement=0.80,
    excluded_dimensions=[
        "personal writing-style preference",
        "answer length by itself",
        "model identity",
        "generation cost",
        "response latency",
    ],
)


class EvaluationInput(BaseModel):
    """All evidence that the judge is permitted to use."""

    case_id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    reference_answer: str = Field(min_length=1)
    candidate_answer: str = Field(min_length=1)
    context: Optional[str] = None


class CriterionScore(BaseModel):
    """A score plus short, observable evidence for that score."""

    criterion: Criterion
    score: int = Field(ge=1, le=5)
    evidence: str = Field(min_length=1, max_length=500)


class EvaluationResult(BaseModel):
    """Validated judge output with an application-owned final decision."""

    case_id: str = Field(min_length=1)
    scores: List[CriterionScore] = Field(min_length=4, max_length=4)
    summary: str = Field(min_length=1, max_length=500)

    @model_validator(mode="after")
    def require_every_criterion_once(self) -> "EvaluationResult":
        actual = [item.criterion for item in self.scores]
        expected = set(Criterion)
        if len(set(actual)) != len(actual):
            raise ValueError("Each criterion must appear exactly once; duplicate found")
        if set(actual) != expected:
            missing = sorted(item.value for item in expected - set(actual))
            raise ValueError(f"Scores are missing criteria: {missing}")
        return self

    @computed_field
    @property
    def weighted_score(self) -> float:
        score_by_criterion = {item.criterion: item.score for item in self.scores}
        total = sum(
            score_by_criterion[criterion] * definition.weight
            for criterion, definition in CRITERIA.items()
        )
        return round(total, 2)

    @computed_field
    @property
    def decision(self) -> Decision:
        score_by_criterion = {item.criterion: item.score for item in self.scores}
        critical_scores_pass = all(
            score_by_criterion[criterion] >= TASK_DEFINITION.minimum_critical_score
            for criterion in (Criterion.CORRECTNESS, Criterion.RELEVANCE)
        )
        if critical_scores_pass and self.weighted_score >= TASK_DEFINITION.pass_threshold:
            return Decision.PASS
        return Decision.FAIL

