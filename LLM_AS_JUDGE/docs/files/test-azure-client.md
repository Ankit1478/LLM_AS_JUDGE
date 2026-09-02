# File Guide: `tests/test_azure_client.py`

Actual file: [`tests/test_azure_client.py`](../../tests/test_azure_client.py)

## Purpose

These tests use a fake Azure-compatible SDK object to verify:

- Deployment and messages are sent correctly.
- Strict JSON Schema is requested.
- Optional temperature is omitted unless configured.
- Raw content, refusals, IDs, and token usage are preserved.
- Empty responses are rejected.
- Provider errors do not expose secrets or candidate text.

The tests never call Azure and never spend tokens.
