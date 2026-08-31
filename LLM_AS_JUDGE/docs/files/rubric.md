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

The expanded structure can hold:

- Instructions for score, binary, and pairwise evaluation
- Instructions for each reference policy
- Definitions of pairwise outcomes
- Bias-prevention rules
- Human-labelled examples

The validator requires each project criterion exactly once. Missing or duplicate
criteria are rejected.

## `RubricExample`

A rubric example demonstrates how a human applied the rules to a real case. Each
example declares its mode, reference policy, candidates, expected label, and a
short explanation.

The validator prevents mismatched examples. For instance, a pairwise example must
contain Candidate B and an expected pairwise decision.

## `PairwiseOutcomeGuide`

Defines the three valid relative-comparison outcomes:

- `A_WINS`: A is meaningfully better.
- `B_WINS`: B is meaningfully better.
- `TIE`: Neither answer has a meaningful quality advantage.

## Rubric versions

`RUBRIC_V1` is the original pointwise, reference-based guide:

```python
RUBRIC_V1.version
# "1.0.0"
```

`RUBRIC_V2` adds all evaluation modes, reference policies, pairwise outcomes,
bias controls, and human-labelled examples:

```python
RUBRIC_V2.version
# "2.0.0"

ACTIVE_RUBRIC is RUBRIC_V2
# True
```

Versioning matters because changing a scoring rule can change evaluation results.
Stored results should eventually record the exact rubric version used.

V2 contains six example categories:

- Clearly good
- Clearly bad
- Borderline
- Candidate A wins
- Candidate B wins
- Pairwise tie

It also tells the future judge to ignore candidate order, model identity, answer
length by itself, confidence, formatting, style preference, and unsupported
concreteness.

## Future use

```text
ACTIVE_RUBRIC
    ↓
Prompt builder converts it to clear model instructions
    ↓
LLM judge returns structured scores and evidence
    ↓
EvaluationResult validates and calculates the decision
```

This file does not call the model by itself.
