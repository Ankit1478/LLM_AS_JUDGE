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
- V2 is active while V1 remains available for reproducibility.
- Every evaluation mode and reference policy has instructions.
- `A_WINS`, `B_WINS`, and `TIE` are all defined.
- All six human-labelled example types are present.
- Bias controls cover order, identity, length, confidence, and formatting.
- Invalid pairwise and reference-free examples are rejected.

## Why these tests matter

An incomplete rubric creates unpredictable human and model judgments. These tests
detect that problem before any evaluation is run.

## Run this file's tests

```bash
PYTHONPATH=src python3 -m unittest tests.test_rubric -v
```
