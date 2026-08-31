# File Guide: `src/llm_judge/contracts.py`

Actual file: [`src/llm_judge/contracts.py`](../../src/llm_judge/contracts.py)

## Purpose

This file defines the structure and policy of the evaluation system.

Simple analogy:

```text
contracts.py = question-paper and answer-sheet format
rubric.py    = teacher's marking guide
```

It does not call an LLM. It makes sure data is complete and internally valid before
another component sends it to a judge model.

## Main objects

### `EvaluationMode`

Defines the supported evaluation formats:

- `SCORE`: Score one answer on several dimensions.
- `BINARY`: Produce `PASS` or `FAIL`.
- `PAIRWISE`: Compare Answer A and Answer B.

### `ReferencePolicy`

Defines how a trusted reference answer is used:

- `REQUIRED`: A reference must be provided.
- `OPTIONAL`: A reference may be provided.
- `REFERENCE_FREE`: A reference must not be provided.

### `TASK_DEFINITION`

This is the central project policy. It records:

- What the judge evaluates
- Supported and preferred modes
- Score range and pass rules
- Expected human-review procedure
- Reliability metrics to calculate later
- Information that must not affect a judgment

It describes the overall evaluation task, not one individual case.

### `INPUT_ORDER_POLICY`

This policy reduces pairwise position bias by hiding candidate identities,
randomizing which answer appears first, and evaluating a second time with A/B
swapped.

It is configuration for a future runner. The policy object itself is not sent to
the LLM.

### `RELIABLE_EXAMPLE_POLICY`

This defines the minimum kinds of human-labelled cases needed to test the judge:

- Clearly good
- Clearly bad
- Borderline
- Pairwise tie

It is a quality gate for the test dataset. It does not evaluate answers.

### `EvaluationInput`

This represents one case to evaluate:

```python
from llm_judge import EvaluationInput, EvaluationMode

case = EvaluationInput(
    case_id="python-001",
    mode=EvaluationMode.PAIRWISE,
    question="What is Python?",
    reference_answer="Python is a programming language.",
    candidate_answer="Python is a programming language.",
    candidate_b="Python is only a snake.",
)
```

Pydantic validates the structure. It does not decide whether either answer is
factually correct.

### `CriterionScore`

Stores one 1–5 score and a short evidence-based explanation. Evidence is for audit
and debugging; it is not a request for private model chain-of-thought.

### Result objects

- `EvaluationResult`: Four pointwise dimension scores plus a computed result.
- `BinaryEvaluationResult`: Direct `PASS` or `FAIL` with evidence.
- `PairwiseEvaluationResult`: `A_WINS`, `B_WINS`, or `TIE` with evidence.

For pointwise scoring, the model supplies dimension scores, while Python calculates
the weighted score and final decision. This prevents contradictory output.

## Pointwise decision rule

```text
Weighted score =
  correctness  × 0.40
  relevance    × 0.25
  completeness × 0.20
  clarity      × 0.15
```

An answer passes only when:

- Weighted score is at least `3.5`.
- Correctness is at least `3`.
- Relevance is at least `3`.

## What this file does not do

- Build prompts
- Call Azure OpenAI
- Load a dataset
- Calculate reliability reports

Those responsibilities belong to later project steps.

