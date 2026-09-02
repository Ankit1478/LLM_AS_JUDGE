# File Guide: `tests/test_prompt_builder.py`

Actual file: [`tests/test_prompt_builder.py`](../../tests/test_prompt_builder.py)

## Purpose

These tests prove that Step 4 produces deterministic prompts with the correct
instructions, case data, examples, and output schemas.

## Behaviors covered

- Score prompts include anchors, failure rules, case data, and score schema.
- Pairwise prompts contain neutral candidates and all three outcomes.
- Reference-free prompts omit reference answers.
- Examples match both mode and reference policy.
- Candidate prompt-injection text remains marked as untrusted data.
- Binary mode receives the binary response schema.
- API messages contain only role and content.

## Run this file's tests

```bash
PYTHONPATH=src python3 -m unittest tests.test_prompt_builder -v
```
