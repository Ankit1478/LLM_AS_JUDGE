# File Guide: `tests/test_calibration.py`

Actual file: [`tests/test_calibration.py`](../../tests/test_calibration.py)

## What is tested

- Deterministic, disjoint splitting with full case coverage
- Binary, score, and pairwise representation in both example partitions
- Draft-data protection
- Split file and manifest round trips
- Accidental overwrite prevention
- Accepted improvements and rejected regressions
- Developer-review requirements
- Fixed and newly introduced false-pass/false-fail IDs
- Rejection of modified human labels
- Rejection of unexpected or missing partition IDs
- Exact held-out verification

All tests are offline and make no Azure calls.
