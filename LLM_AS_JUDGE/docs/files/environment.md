# File Guide: `.env.example`

Actual file: [`.env.example`](../../.env.example)

## Purpose

This file documents the environment-variable names needed by the Azure judge. It
contains placeholders only and must never contain a real API key.

## Required values

- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI resource URL.
- `AZURE_OPENAI_API_KEY`: Secret credential.
- `AZURE_OPENAI_DEPLOYMENT`: Judge deployment name, not merely a generic model name.
- `AZURE_OPENAI_API_VERSION`: API version supported by that Azure resource.

## Optional controls

- Request timeout
- SDK retry count
- Maximum completion tokens
- Temperature, only for deployments that support it

The application does not automatically read a `.env` file. Production systems
should inject these values through a secret manager or deployment environment.

