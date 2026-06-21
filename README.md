# Enterprise AgentOps Control Tower

Enterprise reference architecture for Microsoft Agentic AI focused on governed, auditable, cost-aware agent workflows across the Microsoft stack.

## What This Project Demonstrates

- MCP tool layer with FastMCP
- Azure Functions orchestration API
- Dataverse as the business data layer
- Azure AI Search for grounded knowledge retrieval
- Azure OpenAI as the primary enterprise LLM provider, with direct OpenAI and Gemini for comparison/lab use
- Power Apps browser-based approval console
- Power Automate / Logic Apps remain optional integration channels
- Pulumi-managed infrastructure
- observability, evaluation, and cost tracking patterns
- human-in-the-loop approval gates
- thread-based workflow state
- Azure Table Storage for runtime thread state
- typed internal agent contracts with Pydantic

## Current Scope

The repository currently includes:

- a local MCP server with mock business data
- core business tools for customers, orders, shipments, refunds, approvals, knowledge, cost, and evaluation
- a local Azure Functions orchestrator endpoint for the webshop support flow
- a local browser approval console at `/api/approval-console` for learning before building the Power Apps canvas app

## Repository Layout

- `mcp-server/` - FastMCP server, tools, services, and mock data
- `apps/orchestrator-api/` - Azure Functions backend entry point
- `apps/frontend-demo/` - optional demo UI
- `agents/` - future agent definitions and orchestration assets
- `power-platform/` - Dataverse schema and Power Platform assets
- `power-platform/custom-connectors/` - Power Apps custom connector OpenAPI contracts
- `power-platform/power-apps/` - Canvas App formulas and build notes
- `infrastructure/pulumi/` - Azure infrastructure as code
- `docs/` - build plan, architecture, and implementation notes

## Local Development

The project starts in mock mode:

```text
MCP_DATA_MODE=mock
```

Dataverse runtime authentication standard:

```text
Service Principal
```

## Important Notes

- No real secrets are stored in the repository.
- The active enterprise LLM provider path is Azure OpenAI. Direct OpenAI and Gemini remain useful for comparison/lab use.
- Local-only files such as `.env`, `local.settings.json`, logs, and virtual environments are ignored.
- Azure naming follows Microsoft Cloud Adoption Framework guidance plus Azure resource-specific naming rules.
- Bootstrap Azure naming/context with `infrastructure/scripts/Initialize-AzureContext.ps1`, which writes the local `infrastructure/config/azure-context.json`.
- The Azure lab environment is intentionally disposable; recovery dumps must live in persistent blob storage outside the workload resource group.
- Target Dataverse runtime identity model: one Service Principal created by Pulumi and then mapped into Dataverse as an Application User.
- Current project runtime identity: the PAC-created Dataverse Service Principal, because it matches the environment that exists today and is the identity that actually works.
- Progress is tracked in [progress.md](./progress.md).
- Architectural direction changes are captured in [changeOfDirection.md](./changeOfDirection.md).

## Key References

- [context.md](./context.md)
- [progress.md](./progress.md)
- [changeOfDirection.md](./changeOfDirection.md)
- [docs/00-setup.md](./docs/00-setup.md)
- [docs/01-project-setup.md](./docs/01-project-setup.md)
- [docs/05-pulumi-infrastructure.md](./docs/05-pulumi-infrastructure.md)
- [docs/ai-azure-openai.md](./docs/ai-azure-openai.md)
