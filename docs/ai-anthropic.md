# Anthropic — Integration Guide

How to use the Anthropic API (Claude models) in this project.

---

## Models Used

| Model | ID | Usage | Input / Output (per 1M tokens) |
|---|---|---|---|
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | Draft Agent, Orchestrator summary | $3.00 / $15.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Intake, Critic, Governance agents | $0.80 / $4.00 |
| Claude Opus 4.8 | `claude-opus-4-8` | Complex reasoning (optional) | $15.00 / $75.00 |

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

## Semantic Kernel Integration

Semantic Kernel wraps the Anthropic client transparently via the `AnthropicChatCompletion` connector:

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.anthropic import AnthropicChatCompletion

kernel = Kernel()
kernel.add_service(AnthropicChatCompletion(
    ai_model_id="claude-sonnet-4-6",
    api_key=os.getenv("ANTHROPIC_API_KEY")
))
```

The same kernel, plugins and pipelines run unchanged regardless of whether the provider is Anthropic or OpenAI. See [docs/09-agent-framework.md](09-agent-framework.md).

---

## Best Practices

- Use `claude-haiku-4-5-20251001` for classification and evaluation — it is significantly cheaper and fast enough for structured JSON output
- Use `claude-sonnet-4-6` for the Draft Agent where prose quality matters
- Always log `input_tokens` and `output_tokens` from `message.usage` — never estimate
- Set `max_tokens` to a realistic ceiling; overshooting wastes budget on latency buffers
- Keep system prompts focused — one agent, one task; split roles across agents rather than mega-prompts

---

## Pricing Reference

See [docs/01-project-setup.md](01-project-setup.md) for the full `pricing.json` and `calculate_agent_run_cost` MCP tool.
