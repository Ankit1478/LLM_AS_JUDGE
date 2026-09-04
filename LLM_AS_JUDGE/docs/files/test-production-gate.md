# File Guide: `tests/test_production_gate.py`

Actual file: [`tests/test_production_gate.py`](../../tests/test_production_gate.py)

## Purpose

These offline tests verify that Step 12 makes a transparent, deterministic release
decision without contacting Azure.

## What is tested

- A gate passes when every required measurement satisfies its threshold.
- Low accuracy, high false-pass risk, draft labels, and mismatched case sets fail.
- Missing measurements fail safely instead of being skipped.
- A custom JSON threshold policy is validated by Pydantic.

Run all tests with:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
