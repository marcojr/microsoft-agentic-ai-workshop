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
codex "Write a Pulumi C# resource for Azure AI Search in infrastructure/pulumi/Program.cs and supporting files.
Use Pulumi.AzureNative, free SKU, uksouth location, read names from azure-context.json,
and export searchService and searchEndpoint."
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
| GPT-5 Mini | `gpt-5-mini` | Direct OpenAI lab path only | Check current provider pricing |
| text-embedding-3-small | `text-embedding-3-small` | Embeddings for Azure AI Search RAG | $0.02 / — |

---

## Token Tracking

Always capture token usage to feed into `log_agent_run`:

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5-mini",
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
        model="gpt-5-mini",
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

## Direct OpenAI Lab Path

The active enterprise path uses Azure OpenAI. Direct OpenAI is kept for lab comparison and Codex/API experiments.

```python
pipeline = WebshopOrderSupportPipeline(provider="azure_openai")
secondary_pipeline = WebshopOrderSupportPipeline(provider="gemini")
```

Do not use direct OpenAI as the default runtime for this Microsoft case.

---

## When to Use Each Provider

| Scenario | Recommended Provider |
|---|---|
| Primary enterprise runtime | Azure OpenAI (`gpt-5-mini` deployment) |
| Direct API lab path | OpenAI (`gpt-5-mini`) |
| Secondary model path | Gemini (`gemini-3.5-flash`) |
| OpenAI embeddings for vector search | OpenAI (`text-embedding-3-small`) |
| Client requires Azure OpenAI only | Azure OpenAI (`gpt-5-mini`) |
| Testing provider parity | Run both and compare via Critic Agent |
| Generating code and tests | Codex CLI (interactive) |
| Scaffolding Pulumi resources | Codex CLI (one-shot) |

---

## Pricing Reference

See [docs/01-project-setup.md](01-project-setup.md) for the full `pricing.json`. The `calculate_agent_run_cost` MCP tool supports OpenAI and Gemini vendors in the active runtime path.

---

## Codex CLI Workflow Tips

- Run `codex` interactively when you are unsure of the output — review before applying
- Use `codex --auto` only for low-risk tasks (adding tests, generating seed data)
- Prefix the prompt with the exact file path so Codex targets the right location
- After Codex writes a file, run the test suite to verify: `uv run pytest tests/ -v`

