# File Guide: `tests/test_dataset.py`

Actual file: [`tests/test_dataset.py`](../../tests/test_dataset.py)

## Purpose

These tests verify that Step 3 safely loads cases and prevents unreviewed or
incorrectly labelled data from becoming a production benchmark.

## Behaviors covered

- All 12 example cases load successfully.
- Every required category has enough examples.
- Draft cases are blocked from production.
- Duplicate case IDs are rejected.
- Pairwise category and winner labels must agree.
- Human-reviewed status requires at least one reviewer.

## Run this file's tests

```bash
PYTHONPATH=src python3 -m unittest tests.test_dataset -v
```
