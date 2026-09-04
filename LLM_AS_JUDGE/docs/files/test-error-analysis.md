# File Guide: `tests/test_error_analysis.py`

Actual file: [`tests/test_error_analysis.py`](../../tests/test_error_analysis.py)

## Purpose

These offline tests prove that Step 11 performs the statistical calculations
correctly without contacting Terra, Luna, or Azure.

## What is tested

- Known true-positive, true-negative, false-positive, and false-negative counts
- Accuracy, precision, recall, F1, false-pass rate, and false-fail rate
- Aggregate abstentions when Terra and Luna disagree
- Pairwise confusion matrices and per-label metrics
- Reproducible bootstrap intervals with a fixed seed
- Undefined zero-denominator metrics
- Draft-label, small-sample, and incomplete-class warnings
- Invalid bootstrap and confidence-level settings

Run all tests with:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
