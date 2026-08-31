# File Guide: `tests/test_contracts.py`

Actual file: [`tests/test_contracts.py`](../../tests/test_contracts.py)

## Purpose

These tests prove that the evaluation contract accepts valid data, rejects invalid
data, and calculates deterministic decisions correctly.

## Behaviors covered

- Required references cannot be empty.
- Reference-free cases work without a reference.
- Pairwise cases require two candidates.
- Pairwise candidates remain neutrally named A and B.
- Pairwise mode and order-swap controls are configured.
- Pointwise weighted scores are calculated correctly.
- Low correctness forces a failure even if other scores are high.
- Every scoring criterion must appear exactly once.
- Binary and pairwise result objects accept valid decisions.

## Why these tests matter

They prevent malformed evaluation cases from reaching a paid model API. They also
protect the business decision rule from accidental changes.

## Run this file's tests

```bash
PYTHONPATH=src python3 -m unittest tests.test_contracts -v
```

