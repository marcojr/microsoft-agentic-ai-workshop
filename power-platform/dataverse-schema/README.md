# AgentOps Dataverse Schema

This folder contains the scripted Dataverse schema for the current project implementation.

Current design choice:

- schema is created by script
- schema is versioned in source control
- reference columns in custom `cr_*` tables are stored as text IDs in v1
- this keeps scripted creation simple and repeatable through the Dataverse Web API

Files:

- `schema.v1.json` - source of truth for custom table and column definitions

Scripts:

- `../scripts/Ensure-AgentOpsDataverseSolution.ps1` - creates the project Publisher/Solution and adds the custom tables to it
- `../scripts/Deploy-AgentOpsDataverseSchema.ps1` - creates missing tables and columns
- `../scripts/Clear-AgentOpsDataverseSeed.ps1` - removes the project seed data from standard `accounts` / `contacts` and custom `cr_*` tables
- `../scripts/Seed-AgentOpsDataverseData.ps1` - seeds standard `accounts` / `contacts` and the custom `cr_*` data from the mock JSON files

Run from repo root:

```powershell
powershell -ExecutionPolicy Bypass -File .\power-platform\scripts\Ensure-AgentOpsDataverseSolution.ps1
powershell -ExecutionPolicy Bypass -File .\power-platform\scripts\Deploy-AgentOpsDataverseSchema.ps1 -SolutionUniqueName agentops_workshop
powershell -ExecutionPolicy Bypass -File .\power-platform\scripts\Clear-AgentOpsDataverseSeed.ps1
powershell -ExecutionPolicy Bypass -File .\power-platform\scripts\Seed-AgentOpsDataverseData.ps1
```

The scripts read Dataverse credentials from:

```text
.env at the repository root, with mcp-server/.env kept as a legacy fallback
```

Current unmanaged solution:

- Friendly name: `AgentOps Workshop`
- Unique name: `agentops_workshop`
- Publisher unique name: `agentops_workshop_publisher`

Observed Dataverse naming nuance:

- for v1 reference-like text columns, the effective logical names follow the `SchemaName`
- that means fields such as `cr_ShipmentKeyRef` and `cr_OrderKeyRef` become logical names like `cr_shipmentkeyref` and `cr_orderkeyref`
- the MCP code and seed script are aligned to those real logical names
