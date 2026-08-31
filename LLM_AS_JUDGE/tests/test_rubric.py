import unittest

from pydantic import ValidationError

from llm_judge.contracts import Criterion
from llm_judge.rubric import EvaluationRubric, RUBRIC_V1, RubricCriterion


class RubricTests(unittest.TestCase):
    def test_v1_contains_every_criterion_and_score_anchor(self) -> None:
        self.assertEqual(
            {item.criterion for item in RUBRIC_V1.criteria},
            set(Criterion),
        )
        for item in RUBRIC_V1.criteria:
            self.assertEqual(set(item.score_anchors), {1, 2, 3, 4, 5})

    def test_criterion_lookup(self) -> None:
        correctness = RUBRIC_V1.for_criterion(Criterion.CORRECTNESS)

        self.assertIn("reference", correctness.definition)
        self.assertIn("fabricated", correctness.score_anchors[1])

    def test_incomplete_score_anchors_are_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            RubricCriterion(
                criterion=Criterion.CLARITY,
                definition="Is the answer clear?",
                score_anchors={1: "Unclear", 5: "Clear"},
            )

    def test_incomplete_rubric_is_rejected(self) -> None:
        one_criterion = RubricCriterion(
            criterion=Criterion.CLARITY,
            definition="Is the answer clear?",
            score_anchors={
                1: "Very unclear",
                2: "Unclear",
                3: "Adequate",
                4: "Clear",
                5: "Very clear",
            },
        )

        with self.assertRaises(ValidationError):
            EvaluationRubric(
                name="incomplete",
                version="1.0.0",
                criteria=[one_criterion],
                judge_instructions=["Use the supplied evidence."],
            )


if __name__ == "__main__":
    unittest.main()

