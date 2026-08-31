"""Core types for the LLM-as-a-Judge learning project."""

from .contracts import (
    CRITERIA,
    TASK_DEFINITION,
    Criterion,
    CriterionScore,
    Decision,
    EvaluationInput,
    EvaluationResult,
)

__all__ = [
    "CRITERIA",
    "TASK_DEFINITION",
    "Criterion",
    "CriterionScore",
    "Decision",
    "EvaluationInput",
    "EvaluationResult",
]

