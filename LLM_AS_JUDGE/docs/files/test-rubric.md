# File Guide: `tests/test_rubric.py`

Actual file: [`tests/test_rubric.py`](../../tests/test_rubric.py)

## Purpose

These tests prove that the rubric is complete and internally consistent.

## Behaviors covered

- `RUBRIC_V1` contains every required criterion.
- Every criterion defines scores 1 through 5.
- A criterion can be looked up by name.
- Missing score anchors are rejected.
- A rubric missing required criteria is rejected.

## Why these tests matter

An incomplete rubric creates unpredictable human and model judgments. These tests
detect that problem before any evaluation is run.

## Run this file's tests

```bash
PYTHONPATH=src python3 -m unittest tests.test_rubric -v
```

