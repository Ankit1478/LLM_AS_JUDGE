# File Guide: `src/llm_judge/response_parser.py`

Actual file: [`src/llm_judge/response_parser.py`](../../src/llm_judge/response_parser.py)

## Purpose

This module performs Step 6. It converts a judge model's raw JSON text into the correct
Pydantic result:

```text
RawJudgeResponse
        ↓
parse_judge_response()
        ↓
BinaryEvaluationResult, PairwiseEvaluationResult, or EvaluationResult
```

## What it checks

- The response mode matches the submitted case.
- The judge model did not refuse the evaluation.
- The content is valid JSON.
- All required fields, enum values, and data types are valid.
- Unexpected fields are rejected.
- The returned `case_id` matches the submitted case.

The parser raises a clear validation error instead of allowing malformed model
output to enter metrics, storage, or production decisions.
