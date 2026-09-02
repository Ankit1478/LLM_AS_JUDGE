# File Guide: `src/llm_judge/prompt_builder.py`

Actual file: [`src/llm_judge/prompt_builder.py`](../../src/llm_judge/prompt_builder.py)

## Purpose

This module converts validated evaluation data and rubric rules into messages for
an LLM judge. It builds prompts but does not call Azure or any model.

```text
EvaluationInput + ACTIVE_RUBRIC
              ↓
       build_judge_prompt()
              ↓
      System + user messages
```

## `ChatMessage`

A provider-neutral message containing a `role` (`system` or `user`) and text
`content`. A future Azure client can consume the same simple shape.

## `JudgePrompt`

Stores the two messages plus reproducibility metadata:

- Evaluation mode
- Rubric name and version
- IDs of included examples
- Expected JSON response schema

`as_api_messages()` returns only the role/content fields needed by a chat API.

## `response_schema_for_mode()`

Selects the correct Pydantic output schema:

- Score → `EvaluationResult`
- Binary → `BinaryEvaluationResult`
- Pairwise → `PairwiseEvaluationResult`

The model is instructed to return only JSON matching this schema.

## `select_examples()`

Selects only examples matching both the current evaluation mode and reference
policy. A reference-free prompt never receives a reference-required example.

## `build_judge_prompt()`

Assembles:

- General judging instructions
- Mode-specific instructions
- Reference-policy instructions
- Bias controls
- Pairwise outcome meanings when needed
- Score anchors and critical-failure rules
- Relevant human-labelled examples
- The evaluation case
- The expected response schema

Candidate content is serialized as JSON and explicitly marked as untrusted data.
The system message tells the judge to evaluate candidate instructions rather than
obey them. This reduces prompt-injection risk, although later production layers
must still validate every model response.

## Example

```python
from llm_judge import EvaluationInput, build_judge_prompt

evaluation_input = EvaluationInput(
    case_id="case-001",
    question="What is 2 + 2?",
    reference_answer="4",
    candidate_answer="The answer is 4.",
)

prompt = build_judge_prompt(evaluation_input)
messages = prompt.as_api_messages()
```

