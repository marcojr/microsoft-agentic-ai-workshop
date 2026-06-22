# Anthropic — Integration Guide

Status: optional legacy reference. The active runtime path for this repo is Azure OpenAI + Gemini.

Anthropic is intentionally not part of the active Microsoft case because the project demonstrates Azure OpenAI through Microsoft Foundry (formerly Azure AI Foundry). Keep this document only as a comparison/reference note.

How to use the Anthropic API (Claude models) in this project.

---

## Models Used

| Model | ID | Usage | Input / Output (per 1M tokens) |
|---|---|---|---|
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | Legacy drafting example only | $3.00 / $15.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Legacy classification example only | $0.80 / $4.00 |
| Claude Opus 4.8 | `claude-opus-4-8` | Legacy complex reasoning example only | $15.00 / $75.00 |

---

## Installation

```bash
uv add anthropic
```

---

## Environment Variable

```env
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Basic Usage

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Summarise the order situation for customer john.smith@contoso.com"}
    ]
)
print(message.content[0].text)
```

---

## With System Prompt

```python
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    system="You are an enterprise AI intake agent. Classify the request and output ONLY valid JSON.",
    messages=[
        {"role": "user", "content": "Check the order for john.smith@contoso.com — shipment delayed 2 weeks"}
    ]
)
```

---

## Token Tracking for Cost Engineering

Always capture token usage and pass it to `log_agent_run`:

```python
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=512,
    system=DRAFT_PROMPT,
    messages=[{"role": "user", "content": context}]
)

text = message.content[0].text
input_tokens = message.usage.input_tokens
output_tokens = message.usage.output_tokens

from enterprise_agentops_mcp.tools.observability import log_agent_run

log_agent_run(
    workflow_name="WebshopOrderSupport",
    intent="SummariseLatestOrderIssue",
    model_used="claude-sonnet-4-6",
    vendor="Anthropic",
    input_tokens=input_tokens,
    output_tokens=output_tokens,
    latency_ms=latency_ms,
    tools_called=tools_called,
    requires_approval=requires_approval,
    risk_score=risk_score,
    quality_score=quality_score,
    groundedness_score=groundedness_score
)
```

---

## Streaming

Use streaming for Copilot Studio or long summaries where latency matters:

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=512,
    system=DRAFT_PROMPT,
    messages=[{"role": "user", "content": context}]
) as stream:
    for text_chunk in stream.text_stream:
        print(text_chunk, end="", flush=True)

final_message = stream.get_final_message()
input_tokens = final_message.usage.input_tokens
output_tokens = final_message.usage.output_tokens
```

---

## Draft Agent Implementation

**File:** `agents/draft_agent.py`

```python
import os
import anthropic
from agents.prompts import DRAFT_PROMPT

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def run_draft_agent(context: str) -> tuple[str, int, int]:
    """Returns (text, input_tokens, output_tokens)."""
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=DRAFT_PROMPT,
        messages=[{"role": "user", "content": context}]
    )
    return (
        message.content[0].text,
        message.usage.input_tokens,
        message.usage.output_tokens
    )
```

---

## Critic Agent Implementation

**File:** `agents/critic_agent.py`

```python
import json, os
import anthropic
from agents.prompts import CRITIC_PROMPT

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def run_critic_agent(draft: str, source_data: str) -> dict:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=CRITIC_PROMPT,
        messages=[{"role": "user", "content": f"Draft:\n{draft}\n\nSource data:\n{source_data}"}]
    )
    return json.loads(message.content[0].text)
```

---

## Intake Agent Implementation

**File:** `agents/intake_agent.py`

```python
import json, os
import anthropic
from agents.prompts import INTAKE_PROMPT

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def run_intake_agent(user_message: str) -> dict:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=INTAKE_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )
    return json.loads(message.content[0].text)
```

---

## Legacy Anthropic Integration

Anthropic is not part of the active runtime path.

This is not used by the active project runtime. See [docs/09-agent-framework.md](09-agent-framework.md) for the current Microsoft Agent Framework direction.

---

## Legacy Notes

- Do not use Claude models in the active Microsoft case.
- If Anthropic is revisited later, keep it as an explicit comparison provider, not as the default runtime.
- Always log `input_tokens` and `output_tokens` from `message.usage` — never estimate
- Set `max_tokens` to a realistic ceiling; overshooting wastes budget on latency buffers
- Keep system prompts focused — one agent, one task; split roles across agents rather than mega-prompts

---

## Pricing Reference

See [docs/01-project-setup.md](01-project-setup.md) for the full `pricing.json` and `calculate_agent_run_cost` MCP tool.
