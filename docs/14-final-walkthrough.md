# Final Walkthrough

This is the final demo path for the Enterprise AgentOps Control Tower core MVP.

## Demo Goal

Show a governed Microsoft agentic AI workflow that can:

- understand a customer/order support issue
- retrieve business data and policy knowledge
- create a human approval when risk is high
- let a manager approve or reject the decision
- record audit, telemetry, cost and quality signals
- report the result in Power BI

## Prerequisites

- Azure Function App deployed: `func-agentops-dev-002`
- Dataverse tables populated with demo data
- Copilot Studio agent configured with the approval tools
- Power Apps approval console connected to the custom connector
- Power BI Desktop report connected to Dataverse `cr_agentrun`
- Application Insights receiving `mcp.log_agent_run` telemetry
- Architecture page available at `docs/architecture/index.html`

## Demo Path

### 1. Open the Architecture

Open:

```text
docs/architecture/index.html
```

Show:

- Architecture Overview
- Runtime Flow
- Governance Loop
- Observability Flow

Talk track:

> "This is not just a chatbot. The agent talks to an orchestrator, the orchestrator uses a typed MCP tool layer, and every business action is governed, auditable and observable."

### 2. Run the Customer Support Scenario

Use Copilot Studio or the Function endpoint.

Prompt:

```text
List the current pending approvals and summarize the risk.
```

Or generate a new run through the Function App:

```powershell
$key = az functionapp keys list --resource-group rg-agentops-dev-002 --name func-agentops-dev-002 --query "functionKeys.default" -o tsv

$body = @{
  customerEmail = "john.smith@contoso.com"
  userId = "user-001"
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri "https://func-agentops-dev-002.azurewebsites.net/api/agents/webshop/order-support?code=$key" `
  -ContentType "application/json" `
  -Body $body
```

Show:

- customer context
- latest order issue
- delayed shipment
- pending refund
- approval requirement
- generated approval id

Talk track:

> "The workflow detects that this is not a simple answer. There is a delayed shipment and pending refund, so the system creates a compensation approval instead of letting the model decide alone."

### 3. Show the MCP Tool Layer

Open:

```text
mcp-server/src/enterprise_agentops_mcp/tools
```

Show:

- `customers.py`
- `orders.py`
- `knowledge.py`
- `approvals.py`
- `observability.py`

Talk track:

> "The agent does not query Dataverse directly. It uses governed MCP tools. That gives us typed contracts, testability, observability and a clean boundary between AI reasoning and enterprise systems."

### 4. Show the Power Apps Approval Console

Open the Canvas App.

Show:

- pending approval list
- selected approval details
- comment field
- Approve / Reject buttons

Talk track:

> "High-risk business decisions stay deterministic. The AI can recommend and summarize, but the approval decision is captured through a manager-facing Power Apps console."

### 5. Show Copilot Studio After Approval

Ask:

```text
List the current pending approvals.
```

Show:

- if approved/rejected, the approval no longer appears as pending
- the agent uses the tool result instead of guessing

Talk track:

> "Copilot Studio becomes the conversational operations surface. It can inspect approval state through tools, but it does not own the system of record."

### 6. Show Application Insights

Open Application Insights logs for:

```text
appi-agentops-dev-eus-002
```

Run:

```kusto
dependencies
| where timestamp > ago(2h)
| where name == "mcp.log_agent_run"
| extend runId=tostring(customDimensions["agentops.run_id"])
| project timestamp, runId, duration, success, customDimensions
| order by timestamp desc
```

Show:

- `mcp.log_agent_run`
- run id
- model
- vendor
- latency
- cost
- risk / quality / groundedness scores

Talk track:

> "Dataverse is the business audit view. Application Insights is the operational view. If something breaks or gets slow, this is where engineering investigates."

### 7. Show Power BI

Open the Power BI Desktop report.

Show:

- Total Runs
- Estimated Cost
- Average Latency
- Runs by Workflow
- Agent run table

Talk track:

> "Power BI gives the business a readable operations layer over the same AgentRun records. This is where leadership can understand cost, quality, latency and risk."

## What This Proves

- Microsoft-first agentic AI architecture
- Human-in-the-loop governance
- Dataverse as system of record
- MCP as governed tool boundary
- Azure OpenAI as primary runtime model provider
- Gemini as comparison provider
- Azure AI Search for grounded knowledge
- Application Insights for operational telemetry
- Power BI for business reporting
- Power Apps and Copilot Studio as Power Platform surfaces

## Final Talking Points

1. The project demonstrates agentic AI beyond a chatbot.
2. The agent is not trusted with direct business actions.
3. MCP tools create a governed boundary between AI and enterprise systems.
4. Dataverse provides auditability and Power Platform integration.
5. Azure AI Search provides grounded knowledge retrieval.
6. Azure OpenAI is the primary Microsoft-aligned model provider.
7. Human approval prevents risky compensation automation.
8. Application Insights and Power BI make the workflow observable.
9. The architecture can evolve to Microsoft 365 Agents SDK later.
10. Purview is a future governance phase, not required for the core demo.

## Optional Next Phases

- Microsoft Purview governance and classification
- Microsoft 365 Agents SDK surface
- richer Power BI report pages
- improved Application Insights correlation across requests and MCP spans
- automated demo data generation

