# CLAUDE.md — Enterprise AgentOps Control Tower

## Project Identity

Enterprise reference architecture demonstrating end-to-end Microsoft Agentic AI.
Positioning: **Microsoft Agentic AI Architect**

Primary scenario: **Webshop Order Support Agent**
Secondary scenario: **Customer Support Case Intelligence Agent**

---

## AI Providers Used in This Project

| Provider | Role | Docs |
|---|---|---|
| Azure OpenAI | Primary enterprise LLM path for the Microsoft case | [docs/ai-azure-openai.md](docs/ai-azure-openai.md) |
| OpenAI / Codex | Direct API lab path, code generation, orchestration scripting | [docs/ai-codex.md](docs/ai-codex.md) |
| Gemini | Secondary comparison/lab LLM path | [docs/ai-gemini.md](docs/ai-gemini.md) |

Default runtime model: `gpt-5-mini` via Azure OpenAI.
Secondary model: `gemini-3.5-flash` via Gemini.

---

## Repository Structure

```
/
├── CLAUDE.md                        ← you are here
├── context.md                       ← authoritative project spec
├── docs/
│   ├── 00-setup.md                  ← install everything (start here)
│   ├── 01-project-setup.md          ← day 1: structure + contracts
│   ├── 02-mcp-server.md             ← day 2: MCP Server MVP + first tools
│   ├── 03-mcp-tools-extended.md     ← day 3: remaining MCP tools
│   ├── 04-orchestrator-api.md       ← day 4: Azure Function Orchestrator API
│   ├── 05-pulumi-infrastructure.md  ← day 5: Pulumi + Azure resources
│   ├── 06-dataverse-setup.md        ← day 6: Dataverse tables + sample data
│   ├── 07-dataverse-integration.md  ← day 7: replace mocks with Dataverse
│   ├── 08-secure-rag.md             ← day 8: Azure AI Search + RAG
│   ├── 09-agent-framework.md        ← day 9: Microsoft Agent Framework + one Semantic Kernel comparison agent
│   ├── 10-observability-polish.md   ← day 10: cost, dashboard, demo
│   ├── agents.md                    ← all agents: roles, prompts, wiring
│   ├── ai-azure-openai.md           ← Azure OpenAI integration guide
│   ├── ai-codex.md                  ← OpenAI Codex integration guide
│   └── ai-gemini.md                 ← Gemini integration guide
├── mcp-server/                      ← Python MCP Server (start here)
├── apps/
│   ├── orchestrator-api/            ← Azure Functions backend
│   ├── frontend-demo/               ← optional demo UI
│   └── m365-agent/                  ← post-MVP: Microsoft 365 Agents SDK
├── agents/                          ← agent definitions and prompts
├── copilot-studio/                  ← Copilot Studio exports + screenshots
├── foundry/                         ← Microsoft Foundry (formerly Azure AI Foundry) config
├── power-platform/                  ← Power Automate flows + Dataverse schema
├── infrastructure/pulumi/           ← Pulumi IaC (C#)
├── data/                            ← sample documents + seed scripts
└── dashboards/                      ← Power BI reports + screenshots
```

---

## Core Commands

```bash
# MCP Server
cd mcp-server
uv sync
uv run fastmcp dev src/enterprise_agentops_mcp/server.py

# Azure Functions
cd apps/orchestrator-api
func start

# Pulumi
cd infrastructure/pulumi
pulumi up --stack dev

# Tests
cd mcp-server
uv run pytest tests/ -v

# Power Platform CLI
pac auth create --url https://yourorg.crm.dynamics.com
```

---

## Key Technologies

| Layer | Technology |
|---|---|
| Business Agent | Copilot Studio (Test Chat for MVP) |
| Managed Agent | Microsoft Foundry (formerly Azure AI Foundry) / Foundry Agent Service |
| Pro-code Orchestration | Microsoft Agent Framework (successor to Semantic Kernel + AutoGen) |
| Legacy/Comparison Agent | Semantic Kernel Draft Agent, kept intentionally for learning and comparison |
| Custom-Engine Agent (Post-MVP) | Microsoft 365 Agents SDK / Agents Playground |
| Governed Tool Layer | MCP Server (Python, FastMCP) |
| Public MCP Server | OpenStreetMap / Geocoding MCP Server |
| Backend API | Azure Functions (Python) |
| Business Data | Dataverse |
| Knowledge Search | Azure AI Search (Secure RAG) |
| Workflow Automation | Power Automate + Logic Apps + Service Bus |
| Observability | Application Insights + Azure Monitor |
| Cost Dashboard | Power BI |
| Infrastructure | Pulumi (C#) |

---

## Working Rules for Claude

- The authoritative spec is `context.md`. When in doubt, follow it.
- Record every meaningful setup step, implementation step, decision, verification result and blocker in `progress.md` at the repository root.
- Keep `progress.md` short, chronological and factual.
- Always start with mock data (`MCP_DATA_MODE=mock`). Replace with real services only after the mock pattern works.
- Never hardcode secrets. Use `.env` locally and Key Vault in Azure.
- Prefer the correct production-shaped path over shortcuts. Do not hardcode business tool names, model names, schemas, or resource names when the project already has a source of truth.
- Agent prompts must not invent available tools. If an agent returns `toolsRequired`, derive the allowed values from the MCP client/tool registry and inject that list into the prompt or validate against it.
- Use typed contracts for agent inputs/outputs where practical. In Python, prefer Pydantic models plus explicit validation over loose dictionaries for LLM response contracts.
- Keep MCP as the governed tool boundary. Agents and orchestrators should call tools through the MCP client wrapper or a registered MCP integration, not import random business services directly.
- If a best-practice implementation needs a small shared abstraction, add it deliberately instead of duplicating local lists or prompt fragments.
- Every MCP tool must log its execution. No silent tool calls.
- All agent runs must call `log_agent_run` and `calculate_agent_run_cost`.
- Approval gates (`create_approval_request`) cannot be bypassed by agents.
- Mock data lives in `mcp-server/src/enterprise_agentops_mcp/data/`.
- Keep mock fallback mode even after Dataverse integration is complete.
- Pulumi manages all Azure resources — do not create resources manually in the portal.
- Dataverse runtime authentication standard is Service Principal. Use interactive `pac auth` only for maker/admin tasks.
- Stage 9 uses Microsoft Agent Framework as the modern pro-code direction. Keep exactly one Semantic Kernel agent, the Draft Agent, for comparison, didactics and legacy understanding.
- Agent/orchestration code must include short step-by-step English comments that explain the execution flow. Keep comments practical: explain why each major step exists, not obvious syntax.

---

## Environment Variables

```env
# AI Providers
OPENAI_API_KEY=
GEMINI_API_KEY=

AI_PRIMARY_PROVIDER=azure_openai
AI_PRIMARY_VENDOR=Azure OpenAI
AI_PRIMARY_MODEL=gpt-5-mini

AI_SECONDARY_PROVIDER=gemini
AI_SECONDARY_VENDOR=Gemini
AI_SECONDARY_MODEL=gemini-3.5-flash

# Azure OpenAI (via Foundry)
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5-mini

# Azure AI Search
AZURE_AI_SEARCH_ENDPOINT=
AZURE_AI_SEARCH_KEY=
AZURE_AI_SEARCH_INDEX=enterprise-knowledge

# Dataverse
DATAVERSE_URL=
DATAVERSE_SP_CLIENT_ID=
DATAVERSE_SP_CLIENT_SECRET=
DATAVERSE_SP_TENANT_ID=

# Power Automate
POWER_AUTOMATE_APPROVAL_URL=

# Azure
APPLICATION_INSIGHTS_CONNECTION_STRING=
AZURE_SERVICE_BUS_CONNECTION_STRING=
AZURE_KEY_VAULT_URL=
AZURE_FUNCTION_KEY=

# MCP
MCP_DATA_MODE=mock
```

---

## MVP Build Order

1. [docs/00-setup.md](docs/00-setup.md) — install everything
2. [docs/01-project-setup.md](docs/01-project-setup.md) — structure + contracts
3. [docs/02-mcp-server.md](docs/02-mcp-server.md) — MCP Server with first tools
4. [docs/03-mcp-tools-extended.md](docs/03-mcp-tools-extended.md) — remaining tools
5. [docs/04-orchestrator-api.md](docs/04-orchestrator-api.md) — Azure Function API
6. [docs/05-pulumi-infrastructure.md](docs/05-pulumi-infrastructure.md) — Pulumi + Azure
7. [docs/06-dataverse-setup.md](docs/06-dataverse-setup.md) — Dataverse tables + data
8. [docs/07-dataverse-integration.md](docs/07-dataverse-integration.md) — replace mocks
9. [docs/08-secure-rag.md](docs/08-secure-rag.md) — Azure AI Search
10. [docs/09-agent-framework.md](docs/09-agent-framework.md) — Microsoft Agent Framework + Copilot Studio, with one Semantic Kernel comparison agent
11. [docs/10-observability-polish.md](docs/10-observability-polish.md) — cost + demo

**Post-MVP:** Microsoft 365 Agents SDK — custom-engine agent surface via Agents Playground, reusing the same Orchestrator API and MCP tool layer.
