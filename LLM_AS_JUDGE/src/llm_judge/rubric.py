"""Step 2: an explicit, versioned rubric for consistent scoring."""

from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .contracts import CRITERIA, Criterion


class RubricCriterion(BaseModel):
    """Scoring guidance for one evaluation criterion.

    ``score_anchors`` explains what every score from 1 through 5 means. Critical
    failure rules prevent serious errors from receiving an inflated score.
    """

    model_config = ConfigDict(frozen=True)

    criterion: Criterion
    definition: str = Field(min_length=1)
    score_anchors: Dict[int, str]
    critical_failure_rules: List[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_all_score_anchors(self) -> "RubricCriterion":
        """Fail at startup if an author forgets or mistypes a score level."""

        expected = {1, 2, 3, 4, 5}
        actual = set(self.score_anchors)
        if actual != expected:
            missing = sorted(expected - actual)
            unexpected = sorted(actual - expected)
            raise ValueError(
                "Score anchors must contain exactly 1 through 5; "
                f"missing={missing}, unexpected={unexpected}"
            )
        if any(not text.strip() for text in self.score_anchors.values()):
            raise ValueError("Every score anchor must contain guidance")
        return self


class EvaluationRubric(BaseModel):
    """The complete rubric supplied to humans and, later, the LLM judge.

    Humans and the model must use the same rubric; otherwise agreement metrics do
    not measure whether they interpreted the same evaluation task.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(min_length=1)
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    criteria: List[RubricCriterion]
    judge_instructions: List[str]

    @model_validator(mode="after")
    def require_every_criterion_once(self) -> "EvaluationRubric":
        """Ensure the rubric matches the dimensions required by result validation."""

        actual = [item.criterion for item in self.criteria]
        expected = set(Criterion)
        if len(set(actual)) != len(actual):
            raise ValueError("Each rubric criterion must appear exactly once")
        if set(actual) != expected:
            missing = sorted(item.value for item in expected - set(actual))
            raise ValueError(f"Rubric is missing criteria: {missing}")
        return self

    def for_criterion(self, criterion: Criterion) -> RubricCriterion:
        """Return the rubric entry for a criterion."""

        return next(item for item in self.criteria if item.criterion == criterion)


# Rubric versions are immutable evaluation artifacts. If scoring guidance changes,
# create a new version instead of silently changing historical interpretation.
RUBRIC_V1 = EvaluationRubric(
    name="reference_based_answer_quality",
    version="1.0.0",
    judge_instructions=[
        "Use only the supplied question, reference answer, and optional context.",
        "Give each criterion an independent score before calculating an overall result.",
        "Support every score with short evidence from the candidate answer or reference.",
        "Do not reward length, confidence, formatting, or model identity by themselves.",
        "Treat missing optional details as acceptable unless the question requires them.",
    ],
    criteria=[
        RubricCriterion(
            criterion=Criterion.CORRECTNESS,
            definition=CRITERIA[Criterion.CORRECTNESS].description,
            score_anchors={
                1: "Mostly incorrect, fabricated, or contradicts the reference.",
                2: "Contains one or more major factual errors that undermine the answer.",
                3: "Generally correct, but contains a minor error or unsupported claim.",
                4: "Correct and consistent with the reference, with no important errors.",
                5: "Completely accurate, precise, and fully supported by the reference.",
            },
            critical_failure_rules=[
                "A fabricated central claim limits correctness to 2 or below.",
                "Contradicting the reference on the main answer limits correctness to 2 or below.",
            ],
        ),
        RubricCriterion(
            criterion=Criterion.RELEVANCE,
            definition=CRITERIA[Criterion.RELEVANCE].description,
            score_anchors={
                1: "Does not address the user's question.",
                2: "Addresses the question only indirectly or is mostly unrelated.",
                3: "Answers the main question but includes notable irrelevant material.",
                4: "Directly answers the question with little or no distraction.",
                5: "Entirely focused; every included detail helps answer the question.",
            },
            critical_failure_rules=[
                "Refusing or changing the subject without need limits relevance to 2 or below.",
            ],
        ),
        RubricCriterion(
            criterion=Criterion.COMPLETENESS,
            definition=CRITERIA[Criterion.COMPLETENESS].description,
            score_anchors={
                1: "Misses nearly all information required to answer the question.",
                2: "Includes part of the answer but omits several important points.",
                3: "Covers the central answer but misses at least one useful required detail.",
                4: "Covers all important points needed for a satisfactory answer.",
                5: "Fully covers every required point without unnecessary expansion.",
            },
            critical_failure_rules=[
                "Omitting the central requested result limits completeness to 2 or below.",
            ],
        ),
        RubricCriterion(
            criterion=Criterion.CLARITY,
            definition=CRITERIA[Criterion.CLARITY].description,
            score_anchors={
                1: "Very difficult to understand because it is incoherent or contradictory.",
                2: "Frequently confusing, ambiguous, or poorly organized.",
                3: "Understandable overall, but some wording or organization is unclear.",
                4: "Clear, concise, and logically organized.",
                5: "Exceptionally clear and precise for the intended reader.",
            },
            critical_failure_rules=[
                "Style preferences alone must not be treated as clarity failures.",
            ],
        ),
    ],
)
