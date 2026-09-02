# File Guide: `src/llm_judge/azure_client.py`

Actual file: [`src/llm_judge/azure_client.py`](../../src/llm_judge/azure_client.py)

## Purpose

This module is the network boundary between the project and Azure OpenAI.

```text
JudgePrompt
    ↓
AzureJudgeClient.evaluate()
    ↓
Azure OpenAI
    ↓
RawJudgeResponse
```

## `AzureJudgeClient`

When no client is injected, it creates the official SDK's `AzureOpenAI` client
using the validated endpoint, API key, version, timeout, and retry settings.

`build_request()` can be used without network access. It creates:

- Azure deployment name
- System and user messages
- Strict JSON-schema response format
- Maximum completion tokens
- Optional temperature only when configured

`evaluate()` performs the call and preserves raw response metadata. Provider
errors are wrapped without copying candidate text or secrets into the public error.

## `RawJudgeResponse`

Stores:

- Response and request IDs
- Deployment and resolved model
- Evaluation mode and rubric version
- Raw JSON content or refusal
- Finish reason
- Prompt, completion, and total token counts

This is not the final evaluation result. Step 6 in `response_parser.py` validates
`content` against the correct Pydantic result model.

## Why the client is injectable

Tests pass a fake object with the same `chat.completions.create()` shape. This lets
the suite verify exact requests without credentials, network access, or token cost.

## Structured outputs

The request uses JSON Schema with `strict: true`, following the
[official OpenAI Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).
Support still depends on the selected Azure deployment and API version.
