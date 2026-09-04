# File Guide: `tests/test_adversarial.py`

Actual file: [`tests/test_adversarial.py`](../../tests/test_adversarial.py)

## What is tested

- Injection category and field detection without retaining matched text
- No findings for an ordinary answer
- Resisted, compromised, disagreement, and error outcomes
- Safe provider error messages
- Draft-label and paid-call gates before model execution
- Loading all eight example categories
- Result files do not copy adversarial candidate payloads

All tests use a fake judge and make no Azure calls.
