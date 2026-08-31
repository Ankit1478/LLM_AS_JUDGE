import unittest

from pydantic import ValidationError

from llm_judge.contracts import (
    Criterion,
    CriterionScore,
    Decision,
    EvaluationInput,
    EvaluationResult,
)


def score(criterion: Criterion, value: int) -> CriterionScore:
    return CriterionScore(
        criterion=criterion,
        score=value,
        evidence="Evidence from the supplied reference.",
    )


class EvaluationContractTests(unittest.TestCase):
    def test_input_requires_reference_answer(self) -> None:
        with self.assertRaises(ValidationError):
            EvaluationInput(
                case_id="case-1",
                question="What is Python?",
                reference_answer="",
                candidate_answer="Python is a programming language.",
            )

    def test_result_passes_when_thresholds_are_met(self) -> None:
        result = EvaluationResult(
            case_id="case-1",
            scores=[
                score(Criterion.CORRECTNESS, 4),
                score(Criterion.RELEVANCE, 4),
                score(Criterion.COMPLETENESS, 3),
                score(Criterion.CLARITY, 4),
            ],
            summary="The answer is correct and directly addresses the question.",
        )

        self.assertEqual(result.weighted_score, 3.8)
        self.assertEqual(result.decision, Decision.PASS)

    def test_low_correctness_forces_failure(self) -> None:
        result = EvaluationResult(
            case_id="case-2",
            scores=[
                score(Criterion.CORRECTNESS, 2),
                score(Criterion.RELEVANCE, 5),
                score(Criterion.COMPLETENESS, 5),
                score(Criterion.CLARITY, 5),
            ],
            summary="The response is polished but contains a material factual error.",
        )

        self.assertEqual(result.weighted_score, 3.8)
        self.assertEqual(result.decision, Decision.FAIL)

    def test_all_criteria_are_required_exactly_once(self) -> None:
        with self.assertRaises(ValidationError):
            EvaluationResult(
                case_id="case-3",
                scores=[
                    score(Criterion.CORRECTNESS, 4),
                    score(Criterion.RELEVANCE, 4),
                    score(Criterion.COMPLETENESS, 4),
                    score(Criterion.COMPLETENESS, 4),
                ],
                summary="Invalid duplicate criterion.",
            )


if __name__ == "__main__":
    unittest.main()

