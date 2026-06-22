# Stage 10: Observability, Power BI and Demo Polish (Day 10)

Wire Application Insights telemetry, keep one working Power BI Operations page, write the final demo walkthrough, and produce the architecture diagram.

---

## Day 10 Deliverables

- [x] `telemetry.py` sending traces to Application Insights when `APPLICATIONINSIGHTS_CONNECTION_STRING` is configured
- [x] Power BI report connected to Dataverse `cr_agentrun` table
- [x] Power BI Operations page started and usable for the demo
- [x] Final walkthrough documented
- [x] Architecture diagram produced
- [x] Final interview/demo talking points documented

---

## OpenTelemetry + Application Insights

**File:** `mcp-server/src/enterprise_agentops_mcp/services/telemetry.py`

```python
import os
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

_CONFIGURED = False
_PROVIDER = None

def init_telemetry() -> bool:
    global _CONFIGURED, _PROVIDER
    if _CONFIGURED:
        return True
    conn = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if not conn:
        return False
    exporter = AzureMonitorTraceExporter(connection_string=conn)
    _PROVIDER = TracerProvider(resource=Resource.create({"service.name": "enterprise-agentops-mcp"}))
    _PROVIDER.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(_PROVIDER)
    _CONFIGURED = True
    return True

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

## Demo Data

There is no fixed seeded-run milestone anymore. The report only needs enough real `cr_agentrun` rows to prove that telemetry, Dataverse logging and Power BI reporting work.

More runs can be generated through the real workflow endpoint whenever a richer dashboard is useful.

---

## Power BI Desktop Report

The primary workshop reporting path is local Power BI Desktop.

Publishing to the Power BI Service is optional and can be added later if a Power BI Pro, Premium Per User, or Fabric/Premium capacity is available.

Report build guide:

```text
dashboards/powerbi/README.md
```

### Data Source

Connect Power BI Desktop to Dataverse:

1. **Get Data** → **Dataverse** → connect to your environment → select `cr_agentrun`

Offline-only fallback:

1. **Get Data** → **JSON** → select `mcp-server/src/enterprise_agentops_mcp/data/agent_runs.json`

Use Dataverse for the real case walkthrough.

Current checkpoint:

- Power BI Desktop installed.
- Dataverse connector authenticated.
- `cr_agentrun` loaded.
- Operations page created with:
  - Total Runs card
  - Estimated Cost card
  - Average Latency card
  - Runs by Workflow donut chart
  - Agent runs table

Remaining Power BI work:

- Save the report as `dashboards/powerbi/agentops-observability.pbix`.
- Generate more real agent runs only if the demo needs richer data.
- Cost Engineering and Governance pages are optional extensions, not core completion criteria.

### Page 1: Operations Overview

| Visual | Fields |
|---|---|
| Card — Total Runs | COUNT(runId) |
| Card — Avg Latency | AVG(latencyMs) |
| Card — Runs Requiring Approval | COUNT where requiresApproval = true |
| Line Chart — Runs Over Time | startedAt (day), COUNT(runId) |
| Donut — By Workflow | workflowName, COUNT |
| Bar — Avg Quality Score by Workflow | workflowName, AVG(qualityScore) |

### Optional Page 2: Cost Engineering

| Visual | Fields |
|---|---|
| Card — Total Estimated Cost | SUM(estimatedCost) |
| Card — Avg Cost per Run | AVG(estimatedCost) |
| Bar — Cost by Vendor | vendorUsed, SUM(estimatedCost) |
| Bar — Cost by Model | modelUsed, SUM(estimatedCost) |
| Scatter — Latency vs Cost | latencyMs, estimatedCost, workflowName |
| Table — Top 10 Runs by Cost | runId, modelUsed, inputTokens, outputTokens, estimatedCost |

### Optional Page 3: Governance and Quality

| Visual | Fields |
|---|---|
| Gauge — Avg Groundedness Score | AVG(groundednessScore) |
| Gauge — Avg Quality Score | AVG(qualityScore) |
| Bar — Avg Risk Score by Workflow | workflowName, AVG(riskScore) |
| Table — High Risk Runs | filter riskScore > 0.7, all fields |
| Bar — Approvals Required by Workflow | workflowName, COUNT where requiresApproval = true |

---

## Final Walkthrough Script

The final walkthrough is now documented in:

```text
docs/14-final-walkthrough.md
```

It covers the demo path, Power Apps, Copilot Studio, Application Insights, Power BI, architecture diagram, and final talking points.

---

## Architecture Diagram

The architecture artifact now lives in:

```text
docs/architecture/index.html
```

It is an interactive HTML diagram using CDN-hosted Mermaid, jQuery and Panzoom.

Included views:

- Architecture Overview
- Runtime Flow
- Governance Loop
- Observability Flow

Open it directly in a browser. No local web server is required.

---

## 8 Interview Talking Points

1. **Governed agentic AI** — all LLM actions go through typed MCP tools; no direct database access from agents
2. **Human-in-the-loop** — high-risk actions create approval requests in Dataverse, resolved through a Power Apps Approval Console; agent never confirms compensation pre-approval
3. **Provider agnosticism** — Azure OpenAI and Gemini are selected through configuration
4. **Cost engineering** — every token logged, every cost calculated; Power BI shows spend by workflow, model and vendor
5. **Observable by design** — Application Insights traces + Dataverse AgentRun table + quality/groundedness/risk scores per run
6. **Pulumi IaC** — all Azure resources declared in C#, reproducible from scratch with `pulumi up`
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
- Reuse the same Microsoft Agent Framework orchestration and MCP tool layer
- Optional Teams deployment if a suitable developer tenant is available
- Screenshots and demo notes

This demonstrates that the architecture is not limited to Copilot Studio as the agent surface.

---

## Post-Core Governance Phase: Microsoft Purview

After the core workflow, Power Apps approval console and observability dashboard are stable, add Microsoft Purview as the governance/compliance layer.

Purview should be used to document and demonstrate:

- sensitive data discovery and classification
- Dataverse approval/customer data governance
- Power Platform connector DLP considerations
- audit and compliance evidence
- AI data governance narrative for the demo

See [docs/13-purview-governance.md](13-purview-governance.md).

---

## Next Step

Continue with [docs/12-copilot-studio.md](12-copilot-studio.md), then [docs/13-purview-governance.md](13-purview-governance.md) after the core workflow is stable.
