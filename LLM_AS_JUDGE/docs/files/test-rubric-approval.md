# File Guide: `tests/test_rubric_approval.py`

Actual file: [`tests/test_rubric_approval.py`](../../tests/test_rubric_approval.py)

## What is tested

- A complete approval passes against the exact active rubric.
- One rubric edit invalidates the old SHA-256 fingerprint.
- Expired approvals fail.
- Missing reviewer roles fail.
- One person cannot satisfy both required roles.
- A review dated after the final approval decision fails.
- Approval JSON round-trips through strict Pydantic validation.

The production-gate tests separately prove that excellent metrics cannot pass
when rubric approval is missing.
