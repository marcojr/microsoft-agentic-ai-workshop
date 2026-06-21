# Stage 1: Project Setup (Day 1)

Create the repository structure, define MCP tool contracts, Dataverse schema and API contracts before writing any implementation code.

---

## Day 1 Deliverables

- [ ] Folder structure created
- [ ] `context.md` present and reviewed
- [ ] `CLAUDE.md` present
- [ ] `README.md` created
- [ ] MCP tool contracts defined
- [ ] Dataverse schema drafted
- [ ] API contracts defined
- [ ] MCP Server `pyproject.toml` created
- [ ] `.env.example` created
- [ ] Mock data JSON stubs created (empty files)

---

## Folder Structure

```bash
mkdir -p mcp-server/src/enterprise_agentops_mcp/{tools,services,models,data}
mkdir -p mcp-server/tests
mkdir -p apps/orchestrator-api/{src,tests}
mkdir -p apps/frontend-demo/src
mkdir -p agents/{intake,knowledge,data,governance,draft,critic,cost,workflow}-agent
mkdir -p agents/plugins
mkdir -p agents/pipelines
mkdir -p copilot-studio/{exported-agent,agent-flows,screenshots}
mkdir -p foundry/{agent-definitions,evaluation-config,tracing-config,screenshots}
mkdir -p power-platform/{solutions,flows,dataverse-schema,screenshots}
mkdir -p infrastructure/pulumi/resources
mkdir -p infrastructure/scripts
mkdir -p data/{sample-documents,sample-dataverse-records,seed-scripts}
mkdir -p dashboards/{powerbi,screenshots}
```

---

## MCP Tool Contracts

Complete list of tools the MCP Server will expose:

### Internal tools (enterprise-agentops-mcp-server)

| Tool | Purpose |
|---|---|
| `get_customer_by_email` | Find a contact/customer by email |
| `get_account_by_name` | Find an account by name |
| `get_latest_order` | Most recent order for a contact |
| `get_order_details` | Order header and metadata |
| `get_order_items` | Line items for an order |
| `get_shipment_status` | Shipment status and tracking |
| `get_returns_for_order` | Return requests linked to an order |
| `get_refunds_for_order` | Refund records linked to an order |
| `get_open_cases` | Open support cases for an account |
| `get_case_details` | Full support case with activities |
| `search_knowledge_articles` | Secure RAG knowledge search |
| `create_approval_request` | Create a human approval request |
| `create_follow_up_task` | Create a follow-up task |
| `calculate_agent_run_cost` | Estimate LLM cost from token usage |
| `log_agent_run` | Log agent execution telemetry |
| `evaluate_response` | Score output before returning to user |

### External tools (OpenStreetMap / Geocoding MCP Server)

| Tool | Purpose |
|---|---|
| `geocode_delivery_postcode` | Validate and geocode a delivery postcode |
| `calculate_delivery_distance_or_route` | Calculate route distance for delivery context |

---

## API Contracts (Orchestrator API)

### Endpoints

```
POST /api/agents/webshop/order-support
POST /api/agents/customer-case/summarise
POST /api/agents/knowledge/search
GET  /api/approvals/pending
POST /api/approvals/decision
GET  /api/agent-runs/{runId}
```

### Request: webshop/order-support

```json
{
  "customerEmail": "john.smith@contoso.com",
  "userId": "user-001",
  "department": "Customer Service"
}
```

### Response: webshop/order-support

```json
{
  "runId": "run-0001",
  "threadId": "thread-0001",
  "threadStatus": "WaitingForApproval",
  "customerName": "John Smith",
  "orderNumber": "WEB-1001",
  "summary": "...",
  "approvalRequired": true,
  "approvalStatus": "Pending",
  "approvalId": "apr-9001",
  "humanInTheLoop": true,
  "qualityScore": 0.88,
  "groundednessScore": 0.91,
  "estimatedCost": 0.012,
  "modelUsed": "gpt-5-mini",
  "latencyMs": 3200
}
```

---

## Dataverse Authentication Standard

Dataverse integration should use `Service Principal` as the default authentication model for backend code.

Use this standard across:

- MCP Server Dataverse access
- Azure Function Orchestrator API
- seed/import scripts
- CI/CD automation

Interactive `pac auth create` remains acceptable for admin and maker tasks, but not as the runtime authentication pattern for application code.

The Service Principal should be provisioned as infrastructure and its credentials stored in Key Vault.

---

## pyproject.toml

**File:** `mcp-server/pyproject.toml`

```toml
[project]
name = "enterprise-agentops-mcp"
version = "0.1.0"
description = "Enterprise AgentOps MCP Server — governed enterprise tool layer"
requires-python = ">=3.12"
dependencies = [
    "mcp[cli]>=1.0.0",
    "fastmcp>=0.1.0",
    "openai>=1.50.0",
    "google-genai>=1.0.0",
    "azure-search-documents>=11.4.0",
    "azure-identity>=1.17.0",
    "azure-monitor-opentelemetry>=1.0.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
    "httpx>=0.27.0",
    "msal>=1.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "ruff>=0.5.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

---

## config.py

**File:** `mcp-server/src/enterprise_agentops_mcp/config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATA_MODE = os.getenv("MCP_DATA_MODE", "mock")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

AI_PRIMARY_PROVIDER = os.getenv("AI_PRIMARY_PROVIDER", "azure_openai")
AI_PRIMARY_VENDOR = os.getenv("AI_PRIMARY_VENDOR", "Azure OpenAI")
AI_PRIMARY_MODEL = os.getenv("AI_PRIMARY_MODEL", "gpt-5-mini")

AI_SECONDARY_PROVIDER = os.getenv("AI_SECONDARY_PROVIDER", "gemini")
AI_SECONDARY_VENDOR = os.getenv("AI_SECONDARY_VENDOR", "Gemini")
AI_SECONDARY_MODEL = os.getenv("AI_SECONDARY_MODEL", "gemini-3.5-flash")

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini")

AZURE_AI_SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT", "")
AZURE_AI_SEARCH_KEY = os.getenv("AZURE_AI_SEARCH_KEY", "")
AZURE_AI_SEARCH_INDEX = os.getenv("AZURE_AI_SEARCH_INDEX", "enterprise-knowledge")

# Dataverse runtime auth uses a Service Principal
DATAVERSE_URL = os.getenv("DATAVERSE_URL", "")
DATAVERSE_SP_CLIENT_ID = os.getenv("DATAVERSE_SP_CLIENT_ID", "")
DATAVERSE_SP_CLIENT_SECRET = os.getenv("DATAVERSE_SP_CLIENT_SECRET", "")
DATAVERSE_SP_TENANT_ID = os.getenv("DATAVERSE_SP_TENANT_ID", "")

POWER_AUTOMATE_APPROVAL_URL = os.getenv("POWER_AUTOMATE_APPROVAL_URL", "")
APPLICATION_INSIGHTS_CONNECTION_STRING = os.getenv("APPLICATION_INSIGHTS_CONNECTION_STRING", "")
```

---

## Mock Data JSON Stubs

Create empty files in `mcp-server/src/enterprise_agentops_mcp/data/`:

```
accounts.json
contacts.json
products.json
orders.json
order_items.json
shipments.json
returns.json
refunds.json
cases.json
activities.json
knowledge_articles.json
approvals.json
agent_runs.json
pricing.json
```

Full content for each file is defined in [docs/02-mcp-server.md](02-mcp-server.md) and [docs/03-mcp-tools-extended.md](03-mcp-tools-extended.md).

---

## Next Step

[docs/02-mcp-server.md](02-mcp-server.md) — Day 2: MCP Server local with first tools.
