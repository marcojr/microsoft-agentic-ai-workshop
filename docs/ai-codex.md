# OpenAI Codex — Integration Guide

How to use the OpenAI Codex CLI and the OpenAI API in this project.

---

## Two Separate Tools

| Tool | What it is | When to use |
|---|---|---|
| **Codex CLI** (`@openai/codex`) | Terminal-based AI coding assistant | Generate boilerplate, scaffold tools, write tests |
| **OpenAI API** (via `openai` Python SDK) | Programmatic LLM calls | Agent pipelines, embeddings for RAG, alternative to Claude |

These are independent. You can use the Codex CLI without calling the OpenAI API from Python, and vice versa.

---

## Codex CLI

### Installation

```bash
npm install -g @openai/codex
```

### Configuration

```bash
export OPENAI_API_KEY=sk-...
codex --version
```

Or add to `.env` and source it:

```env
OPENAI_API_KEY=sk-...
```

### Usage Modes

```bash
# Interactive (ask and approve each step)
codex

# One-shot (run and exit)
codex "Generate a FastMCP tool called get_account_details"

# Auto-apply (no approval prompt — use carefully)
codex --auto "Add pytest tests for get_shipment_status"
```

### Typical Tasks in This Project

#### Scaffold a new MCP tool

```bash
codex "Create a FastMCP tool called get_account_risk_profile that takes account_id as input,
loads accounts.json from MockDataService, finds the matching account and returns
accountId, name, riskLevel, creditLimit, outstandingBalance"
```

#### Write tests

```bash
codex "Write pytest tests for get_latest_order in mcp-server/src/enterprise_agentops_mcp/tools/orders.py.
Test: found case, not found case, multiple orders returns latest by date.
Use DATA_MODE=mock, no mocking of files."
```

#### Generate a Pulumi resource

```bash
codex "Write a Pulumi TypeScript resource for Azure AI Search in infrastructure/pulumi/resources/aiSearch.ts.
Use azure-native provider, free SKU, uksouth location, import resourceGroup from ./resourceGroup,
export searchService and searchEndpoint."
```

#### Seed data

```bash
codex "Write a Python script at data/seed-scripts/seed_dataverse.py that reads contacts.json,
accounts.json, orders.json from mcp-server/src/enterprise_agentops_mcp/data/ and
posts each record to Dataverse using dataverse_service.dv_post."
```

---

## OpenAI API (Python SDK)

### Installation

```bash
uv add openai
```

### Environment Variable

```env
OPENAI_API_KEY=sk-...
```

### Models Used in This Project

| Model | ID | Usage | Input / Output (per 1M tokens) |
|---|---|---|---|
| GPT-4.1 Mini | `gpt-4.1-mini` | Draft Agent, Intake, Critic (provider=openai) | $0.40 / $1.60 |
| GPT-4.1 | `gpt-4.1` | Higher quality drafting (optional) | $2.00 / $8.00 |
| text-embedding-3-small | `text-embedding-3-small` | Embeddings for Azure AI Search RAG | $0.02 / — |

---

## Token Tracking

Always capture token usage to feed into `log_agent_run`:

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    max_tokens=512,
    messages=[
        {"role": "system", "content": DRAFT_PROMPT},
        {"role": "user", "content": context}
    ]
)

text = response.choices[0].message.content
input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens
```

---

## Draft Agent (OpenAI)

```python
import os
from openai import OpenAI
from agents.prompts import DRAFT_PROMPT

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_draft_agent_openai(context: str) -> tuple[str, int, int]:
    """Returns (text, input_tokens, output_tokens)."""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        max_tokens=512,
        messages=[
            {"role": "system", "content": DRAFT_PROMPT},
            {"role": "user", "content": context}
        ]
    )
    return (
        response.choices[0].message.content,
        response.usage.prompt_tokens,
        response.usage.completion_tokens
    )
```

---

## Embeddings for Azure AI Search

The ingestion pipeline uses OpenAI embeddings to vectorise policy documents:

```python
from openai import OpenAI

client = OpenAI()

def embed(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text[:8000]
    )
    return response.data[0].embedding
```

See [docs/08-secure-rag.md](08-secure-rag.md) for the full ingestion script.

---

## Semantic Kernel Integration

The same SK pipeline runs with OpenAI by changing the provider parameter:

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

kernel = Kernel()
kernel.add_service(OpenAIChatCompletion(
    ai_model_id="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY")
))
```

Switch from Anthropic to OpenAI:

```python
pipeline = WebshopOrderSupportPipeline(provider="openai")
```

No other code changes required.

---

## When to Use Each Provider

| Scenario | Recommended Provider |
|---|---|
| Primary development and drafting | Anthropic (`claude-sonnet-4-6`) |
| Fast cheap classification and evaluation | Anthropic (`claude-haiku-4-5-20251001`) |
| OpenAI embeddings for vector search | OpenAI (`text-embedding-3-small`) |
| Client requires Azure OpenAI only | Azure OpenAI (`gpt-4o-mini`) |
| Testing provider parity | Run both and compare via Critic Agent |
| Generating code and tests | Codex CLI (interactive) |
| Scaffolding Pulumi resources | Codex CLI (one-shot) |

---

## Pricing Reference

See [docs/01-project-setup.md](01-project-setup.md) for the full `pricing.json`. The `calculate_agent_run_cost` MCP tool supports both Anthropic and OpenAI vendors.

---

## Codex CLI Workflow Tips

- Run `codex` interactively when you are unsure of the output — review before applying
- Use `codex --auto` only for low-risk tasks (adding tests, generating seed data)
- Prefix the prompt with the exact file path so Codex targets the right location
- After Codex writes a file, run the test suite to verify: `uv run pytest tests/ -v`
