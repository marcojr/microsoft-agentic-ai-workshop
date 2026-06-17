# Stage 10: Observability, Cost Dashboard and Demo Polish (Day 10)

Wire Application Insights telemetry, build the Power BI cost engineering dashboard, run the 7-minute demo end-to-end, and produce the architecture diagram.

---

## Day 10 Deliverables

- [ ] `telemetry.py` sending traces to Application Insights
- [ ] 25 seeded agent runs for dashboard demo
- [ ] Power BI report connected to Dataverse `cr_agentrun` table
- [ ] 3 dashboard pages: Operations, Cost Engineering, Governance
- [ ] 7-minute demo walkthrough completed end-to-end
- [ ] Architecture diagram produced
- [ ] 8 interview talking points documented

---

## OpenTelemetry + Application Insights

**File:** `mcp-server/src/enterprise_agentops_mcp/services/telemetry.py`

```python
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

_provider = None

def init_telemetry():
    global _provider
    conn = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if not conn or _provider:
        return
    exporter = AzureMonitorTraceExporter(connection_string=conn)
    _provider = TracerProvider()
    _provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(_provider)

def get_tracer():
    init_telemetry()
    return trace.get_tracer("enterprise-agentops-mcp")
```

Usage in tools:

```python
from enterprise_agentops_mcp.services.telemetry import get_tracer

tracer = get_tracer()

def log_agent_run(...) -> dict:
    with tracer.start_as_current_span("log_agent_run") as span:
        span.set_attribute("workflow_name", workflow_name)
        span.set_attribute("model_used", model_used)
        span.set_attribute("vendor", vendor)
        span.set_attribute("input_tokens", input_tokens)
        span.set_attribute("output_tokens", output_tokens)
        span.set_attribute("estimated_cost", estimated_cost)
        span.set_attribute("latency_ms", latency_ms)
        span.set_attribute("quality_score", quality_score)
        span.set_attribute("risk_score", risk_score)
        # ... rest of logging logic
```

Install:
```bash
uv add azure-monitor-opentelemetry-exporter opentelemetry-sdk
```

---

## Seed 25 Agent Runs

**File:** `data/seed-scripts/seed_agent_runs.py`

```python
import sys, random

sys.path.insert(0, "mcp-server/src")
from enterprise_agentops_mcp.tools.observability import log_agent_run

workflows = ["WebshopOrderSupport", "CustomerCaseIntelligence"]
intents = ["SummariseLatestOrderIssue", "CheckDeliveryStatus", "EscalateCase", "RequestRefund"]
models = [
    ("claude-sonnet-4-6", "Anthropic"),
    ("claude-haiku-4-5-20251001", "Anthropic"),
    ("gpt-4.1-mini", "OpenAI")
]
tools_pool = ["get_customer_by_email", "get_latest_order", "get_shipment_status",
              "get_returns_for_order", "search_knowledge_articles", "evaluate_response"]

for i in range(25):
    model, vendor = random.choice(models)
    log_agent_run(
        workflow_name=random.choice(workflows),
        intent=random.choice(intents),
        model_used=model, vendor=vendor,
        input_tokens=random.randint(800, 3000),
        output_tokens=random.randint(200, 800),
        latency_ms=random.randint(800, 3500),
        tools_called=random.sample(tools_pool, k=random.randint(3, 6)),
        requires_approval=random.random() > 0.7,
        risk_score=round(random.uniform(0.1, 0.9), 2),
        quality_score=round(random.uniform(0.6, 0.98), 2),
        groundedness_score=round(random.uniform(0.55, 0.98), 2)
    )

print("25 agent runs seeded.")
```

```bash
uv run python data/seed-scripts/seed_agent_runs.py
```

---

## Power BI Dashboard

### Data Source

Connect Power BI Desktop to Dataverse (or import `agent_runs.json` for local demo):

1. **Get Data** → **Dataverse** → connect to your environment → select `cr_agentrun`

Or for local demo:
1. **Get Data** → **JSON** → select `mcp-server/src/enterprise_agentops_mcp/data/agent_runs.json`

### Page 1: Operations Overview

| Visual | Fields |
|---|---|
| Card — Total Runs | COUNT(runId) |
| Card — Avg Latency | AVG(latencyMs) |
| Card — Runs Requiring Approval | COUNT where requiresApproval = true |
| Line Chart — Runs Over Time | startedAt (day), COUNT(runId) |
| Donut — By Workflow | workflowName, COUNT |
| Bar — Avg Quality Score by Workflow | workflowName, AVG(qualityScore) |

### Page 2: Cost Engineering

| Visual | Fields |
|---|---|
| Card — Total Estimated Cost | SUM(estimatedCost) |
| Card — Avg Cost per Run | AVG(estimatedCost) |
| Bar — Cost by Vendor | vendorUsed, SUM(estimatedCost) |
| Bar — Cost by Model | modelUsed, SUM(estimatedCost) |
| Scatter — Latency vs Cost | latencyMs, estimatedCost, workflowName |
| Table — Top 10 Runs by Cost | runId, modelUsed, inputTokens, outputTokens, estimatedCost |

### Page 3: Governance and Quality

| Visual | Fields |
|---|---|
| Gauge — Avg Groundedness Score | AVG(groundednessScore) |
| Gauge — Avg Quality Score | AVG(qualityScore) |
| Bar — Avg Risk Score by Workflow | workflowName, AVG(riskScore) |
| Table — High Risk Runs | filter riskScore > 0.7, all fields |
| Bar — Approvals Required by Workflow | workflowName, COUNT where requiresApproval = true |

---

## 7-Minute Demo Script

### Minute 0:00 — Scene Setting (30 sec)

> "This is the Enterprise AgentOps Control Tower — a Microsoft reference architecture for governed agentic AI. I'll show you a webshop order support scenario with real AI orchestration, human-in-the-loop approval, and live cost tracking."

### Minute 0:30 — Copilot Studio (1:30)

Open Copilot Studio → Enterprise AgentOps Assistant → Test Chat.

Type: **"Find the latest order situation for john.smith@contoso.com"**

Show:
- Agent calls the HTTP action
- Orchestrator API triggers
- JSON response appears in chat
- Summary shown with delivery delay, refund pending, approval required

> "Notice the agent detected a high-risk situation — a delayed shipment with a pending refund — and automatically created an approval request without revealing sensitive compensation details to the customer."

### Minute 2:00 — MCP Server (1:00)

Switch to VS Code → show `mcp-server/src/enterprise_agentops_mcp/tools/`

> "All 18 tools are exposed through a FastMCP server. These are governed enterprise tools — each one typed, documented and observable. The agent never calls Dataverse directly."

### Minute 3:00 — Agent Pipeline (1:30)

Open `agents/pipelines/webshop_pipeline.py`

> "In Stage 9 we replace the single-step orchestrator with a Semantic Kernel multi-agent pipeline. An Intake Agent classifies the request, a Data Agent fetches data via MCP tools, a Draft Agent with Claude Sonnet writes the summary, and a Critic Agent evaluates quality and groundedness before the response is returned."

Switch provider: change `provider="openai"` → re-run → show same output with GPT-4.1 Mini.

> "Provider switching is a single parameter — the architecture supports Anthropic and OpenAI without code changes."

### Minute 4:30 — Governance and Approval (1:00)

Show Power Automate → approval flow → manager receives email → approves.

> "Compensation actions require a human in the loop. The approval request is created in Dataverse and triggers a Power Automate flow that routes to the service manager."

### Minute 5:30 — Observability Dashboard (1:00)

Open Power BI → Operations → Cost Engineering → Governance pages.

> "Every agent run is logged with token counts, estimated cost, latency, quality score, risk score, and groundedness score. This is the cost engineering view — the business can see exactly what AI is spending and where."

### Minute 6:30 — Closing (30 sec)

> "This architecture runs entirely on Microsoft infrastructure — Copilot Studio, Azure Functions, Dataverse, AI Foundry — with Pulumi for reproducible IaC and Anthropic Claude as the reasoning engine. Every component is observable, governed and auditable."

---

## Architecture Diagram

Create in draw.io (diagrams.net) with the following layers (top to bottom):

MVP path:

```
┌─────────────────────────────────────┐
│  Business Users                     │
│  [Copilot Studio] ← Test Chat       │
└────────────┬────────────────────────┘
             │ HTTP Action
┌────────────▼────────────────────────┐
│  Orchestrator Layer                 │
│  [Azure Functions] (Python)         │
│  └── [Semantic Kernel Pipeline]     │
│       ├── Intake Agent              │
│       ├── Data Agent                │
│       ├── Draft Agent (Claude)      │
│       └── Critic Agent              │
└────────────┬────────────────────────┘
             │ Tool calls
┌────────────▼────────────────────────┐
│  MCP Server (FastMCP, Python)       │
│  16 internal tools + 2 geocoding    │
│  mock mode ← → live mode            │
└──┬──────────────────────────────────┘
   │                    │
┌──▼──────┐    ┌────────▼────────────┐
│Dataverse│    │ External MCP:       │
│ Tables  │    │ OpenStreetMap /     │
│(contact │    │ Geocoding Server    │
│ order   │    └─────────────────────┘
│shipment │
│agentrun)│
└─────────┘

┌─────────────────────────────────────┐
│  Governance + Observability         │
│  [App Insights] [Power BI]          │
│  [Key Vault] [Power Automate]       │
│  [Azure AI Foundry Policy Agent]    │
└─────────────────────────────────────┘
```

Future custom-engine agent surface (post-MVP):

```
┌─────────────────────────────────────────┐
│  Microsoft 365 Agents SDK               │
│  Agents Playground / optional Teams     │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│  Azure Function Orchestrator API        │
│  same orchestration and MCP tool layer  │
└─────────────────────────────────────────┘
```

---

## 8 Interview Talking Points

1. **Governed agentic AI** — all LLM actions go through typed MCP tools; no direct database access from agents
2. **Human-in-the-loop** — high-risk actions create approval requests in Dataverse, routed via Power Automate; agent never confirms compensation pre-approval
3. **Provider agnosticism** — Anthropic Claude and OpenAI GPT both run the same SK pipeline; single parameter to switch
4. **Cost engineering** — every token logged, every cost calculated; Power BI shows spend by workflow, model and vendor
5. **Observable by design** — Application Insights traces + Dataverse AgentRun table + quality/groundedness/risk scores per run
6. **Pulumi IaC** — all Azure resources declared in TypeScript, reproducible from scratch with `pulumi up`
7. **Progressive fidelity** — same codebase runs against mock JSON (Day 2) and live Dataverse (Day 7) with a single env var
8. **Policy RAG** — knowledge articles indexed in Azure AI Search with semantic + vector search; Foundry Policy Agent grounds governance decisions in verified documents

---

---

## Post-MVP Phase: Microsoft 365 Agents SDK

Not part of the Day 10 scope. After the MVP is complete and demonstrated, the next phase is:

**Deliverables:**
- Microsoft 365 Agents SDK project in `apps/m365-agent/`
- Test through Microsoft 365 Agents Playground
- Connect to the same Azure Function Orchestrator API
- Reuse the same Semantic Kernel orchestration and MCP tool layer
- Optional Teams deployment if a suitable developer tenant is available
- Screenshots and demo notes

This demonstrates that the architecture is not limited to Copilot Studio as the agent surface.

---

## Next Step

All 10 stages complete. Return to [CLAUDE.md](../CLAUDE.md) for the full project reference.
