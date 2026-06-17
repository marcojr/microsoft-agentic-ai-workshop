# Enterprise AgentOps Control Tower

Enterprise reference architecture for Microsoft Agentic AI focused on governed, auditable, cost-aware agent workflows across the Microsoft stack.

## What This Project Demonstrates

- MCP tool layer with FastMCP
- Azure Functions orchestration API
- Dataverse as the business data layer
- Azure AI Search for grounded knowledge retrieval
- Power Automate approval integration
- Pulumi-managed infrastructure
- observability, evaluation, and cost tracking patterns

## Current Scope

The repository currently includes:

- a local MCP server with mock business data
- core business tools for customers, orders, shipments, refunds, approvals, knowledge, cost, and evaluation
- a local Azure Functions orchestrator endpoint for the webshop support flow

## Repository Layout

- `mcp-server/` - FastMCP server, tools, services, and mock data
- `apps/orchestrator-api/` - Azure Functions backend entry point
- `apps/frontend-demo/` - optional demo UI
- `agents/` - future agent definitions and orchestration assets
- `power-platform/` - Dataverse schema and Power Platform assets
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
- Local-only files such as `.env`, `local.settings.json`, logs, and virtual environments are ignored.
- Progress is tracked in [progress.md](./progress.md).

## Key References

- [context.MD](./context.MD)
- [progress.md](./progress.md)
- [docs/00-setup.md](./docs/00-setup.md)
- [docs/01-project-setup.md](./docs/01-project-setup.md)
