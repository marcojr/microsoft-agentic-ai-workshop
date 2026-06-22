# AgentOps Power BI Report

Build the observability report locally in Power BI Desktop.

This project does not require publishing to the Power BI Service for the workshop flow. Publishing and sharing can be added later if a Power BI Pro, Premium Per User, or Fabric/Premium capacity is available.

## Install Power BI Desktop

Windows:

```powershell
winget install Microsoft.PowerBI
```

## Report File

Save the local report as:

```text
dashboards/powerbi/agentops-observability.pbix
```

## Data Source

Preferred source:

```text
Dataverse table: cr_agentrun
```

Power BI Desktop path:

```text
Get data -> Dataverse -> select the current Power Platform environment -> select cr_agentrun
```

Fallback source for offline demo:

```text
mcp-server/src/enterprise_agentops_mcp/data/agent_runs.json
```

Use the Dataverse source for the real case walkthrough.

## Required Columns

Use these Dataverse columns from `cr_agentrun`:

| Display | Logical name |
|---|---|
| Run Key | `cr_runkey` |
| Workflow Name | `cr_workflowname` |
| Intent | `cr_intent` |
| Model Used | `cr_modelused` |
| Vendor Used | `cr_vendorused` |
| Started At | `cr_startedat` |
| Status | `cr_status` |
| Input Tokens | `cr_inputtokens` |
| Output Tokens | `cr_outputtokens` |
| Estimated Cost | `cr_estimatedcost` |
| Latency Ms | `cr_latencyms` |
| Tools Called | `cr_toolscalled` |
| Requires Approval | `cr_requiresapproval` |
| Risk Score | `cr_riskscore` |
| Quality Score | `cr_qualityscore` |
| Groundedness Score | `cr_groundednessscore` |

## Page 1: Operations

Purpose: show how the agentic workflow is behaving operationally.

Current status:

- Dataverse connection created.
- `cr_agentrun` loaded into Power BI Desktop.
- Operations page started.
- Current visuals created:
  - Total Runs card
  - Estimated Cost card
  - Average Latency card
  - Runs by Workflow donut chart
  - Agent runs table

Suggested visuals:

| Visual | Fields |
|---|---|
| Card | Count of `cr_runkey` |
| Card | Average `cr_latencyms` |
| Card | Count where `cr_requiresapproval = true` |
| Line chart | `cr_startedat` by count of `cr_runkey` |
| Donut chart | `cr_workflowname` by count of `cr_runkey` |
| Table | latest runs: `cr_runkey`, `cr_workflowname`, `cr_status`, `cr_latencyms` |

## Optional Page 2: Cost Engineering

Purpose: show AI spend by model, vendor and workflow.

Status: optional extension.

Suggested visuals:

| Visual | Fields |
|---|---|
| Card | Sum of `cr_estimatedcost` |
| Card | Average `cr_estimatedcost` |
| Bar chart | `cr_vendorused` by sum of `cr_estimatedcost` |
| Bar chart | `cr_modelused` by sum of `cr_estimatedcost` |
| Scatter chart | `cr_latencyms` vs `cr_estimatedcost`, legend `cr_workflowname` |
| Table | top runs by `cr_estimatedcost` |

## Optional Page 3: Governance

Purpose: show risk, quality, groundedness and human approval pressure.

Status: optional extension.

Suggested visuals:

| Visual | Fields |
|---|---|
| Gauge | Average `cr_groundednessscore` |
| Gauge | Average `cr_qualityscore` |
| Bar chart | `cr_workflowname` by average `cr_riskscore` |
| Table | filter `cr_riskscore > 0.7` |
| Bar chart | `cr_workflowname` by count of `cr_requiresapproval = true` |

## Demo Talking Point

Use this line during the demo:

```text
Every agent run is logged to Dataverse with token counts, estimated cost, latency, risk, quality and groundedness. Power BI Desktop gives the business a local report showing operational health, AI spend and governance signals without requiring a Power BI Service subscription for this workshop.
```
