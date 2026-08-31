# File Guide: `src/llm_judge/rubric.py`

Actual file: [`src/llm_judge/rubric.py`](../../src/llm_judge/rubric.py)

## Purpose

This file defines the marking guide used by humans and, later, the LLM judge.
It answers: “What does a score of 1, 2, 3, 4, or 5 mean?”

## `RubricCriterion`

Represents the scoring guide for one dimension:

- `criterion`: Correctness, relevance, completeness, or clarity.
- `definition`: What the dimension measures.
- `score_anchors`: Meaning of every score from 1 through 5.
- `critical_failure_rules`: Serious errors that limit the possible score.

Example idea:

```text
Correctness 1 = Mostly incorrect or fabricated
Correctness 3 = Mostly correct with a minor issue
Correctness 5 = Completely accurate and supported
```

The validator requires all five score anchors. An incomplete scoring guide fails
when the application starts instead of producing ambiguous judgments later.

## `EvaluationRubric`

Combines every `RubricCriterion` into one complete, versioned marking guide. It
also contains instructions shared by human reviewers and the judge model.

The validator requires each project criterion exactly once. Missing or duplicate
criteria are rejected.

## `RUBRIC_V1`

This is the actual rubric currently configured by the project.

```python
RUBRIC_V1.version
# "1.0.0"
```

Versioning matters because changing a scoring rule can change evaluation results.
Stored results should eventually record the exact rubric version used.

## Future use

```text
RUBRIC_V1
    ↓
Prompt builder converts it to clear model instructions
    ↓
LLM judge returns structured scores and evidence
    ↓
EvaluationResult validates and calculates the decision
```

This file does not call the model by itself.

