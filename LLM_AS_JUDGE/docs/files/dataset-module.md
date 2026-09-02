# File Guide: `src/llm_judge/dataset.py`

Actual file: [`src/llm_judge/dataset.py`](../../src/llm_judge/dataset.py)

## Purpose

This module loads evaluation cases and checks whether their structure, expected
labels, category coverage, and human-review status are valid.

Simple analogy:

```text
Rubric              = Teacher's marking guide
Evaluation dataset  = Exam with an answer key
dataset.py          = Person checking that the exam is complete and approved
```

## `ReviewStatus`

- `DRAFT`: Suggested label; no human has approved it.
- `HUMAN_REVIEWED`: At least one human confirmed the label.
- `ADJUDICATED`: At least two reviewers participated and disagreement was resolved.

Draft data is useful for development but cannot be treated as production truth.

## `EvaluationCase`

Extends `EvaluationInput` with an expected result and review metadata. Its
validator ensures the expected label matches the mode:

- Score mode needs four expected dimension scores.
- Binary mode needs `PASS` or `FAIL`.
- Pairwise mode needs `A_WINS`, `B_WINS`, or `TIE`.

It also prevents a case from claiming human review without recording reviewers.

## `EvaluationDataset`

Holds a list of cases and provides three important checks:

- Case IDs must be unique.
- Minimum good, bad, borderline, and tie coverage must be present.
- Every case must be human-reviewed before production use.

## `load_jsonl`

Loads one JSON object per line:

```python
from llm_judge import load_jsonl

dataset = load_jsonl("datasets/evaluation_cases.example.jsonl")
print(dataset.kind_counts)
```

Invalid data reports the source file and line number, making large datasets easier
to repair.

## Production gate

```python
dataset.ensure_ready_for_production()
```

The included example dataset fails this check intentionally because its labels are
still drafts. Real humans must review them first.

