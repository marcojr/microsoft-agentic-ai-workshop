# Gemini API Integration Guide

Gemini is the secondary LLM provider for this project.

Primary project path:

```text
Azure OpenAI -> primary enterprise provider
Gemini -> secondary comparison provider
Direct OpenAI -> not active in this case
Anthropic -> not active
```

## Environment

Use:

```env
GEMINI_API_KEY=
AI_SECONDARY_PROVIDER=gemini
AI_SECONDARY_VENDOR=Gemini
AI_SECONDARY_MODEL=gemini-3.5-flash
```

Google's Gemini SDK can also read `GOOGLE_API_KEY`, but this repo standardizes on `GEMINI_API_KEY`.

Official source:

- https://ai.google.dev/gemini-api/docs/api-key
- https://ai.google.dev/gemini-api/docs/quickstart

## Python SDK

The project dependency is:

```toml
google-genai>=1.0.0
```

Minimal call:

```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Summarise this support case."
)

print(response.text)
```

## Current Decision

We are not using Anthropic in the active runtime because API credits are not available.

The current runtime should read model/provider settings from `.env`, not hardcode model names in the orchestrator.
