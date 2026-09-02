# File Guide: `src/llm_judge/settings.py`

Actual file: [`src/llm_judge/settings.py`](../../src/llm_judge/settings.py)

## Purpose

This module converts environment variables into one validated
`AzureJudgeSettings` object.

```text
Environment variables
        ↓
AzureJudgeSettings.from_env()
        ↓
Validated, typed settings
```

## Safety behavior

- Missing required variables are reported together.
- Invalid endpoints and numeric limits are rejected.
- The API key uses Pydantic `SecretStr`, which masks it in normal representations.
- Settings are frozen after creation.
- The endpoint's trailing slash is normalized.
- The deployment defaults to `gpt-5.6-terra`.
- `AZURE_OPENAI_DEPLOYMENT` can optionally override the Terra default.

## Example

```python
from llm_judge import AzureJudgeSettings

settings = AzureJudgeSettings.from_env()
```

This reads the process environment. It does not read `.env` automatically and does
not contact Azure.
