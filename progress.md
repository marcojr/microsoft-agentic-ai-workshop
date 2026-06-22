# Project Progress

Registro curto do que foi feito, decidido e verificado durante o projeto.

## 2026-06-22 - Linux handover refresh

- Rewrote `pc-transfer.txt` as an updated Linux handover.
- Captured current MVP status, Microsoft Agent Framework-only runtime decision, verification commands, required env vars, and next-phase roadmap.
- Added the recommended prompt for the next Codex session on Linux.

## 2026-06-22 - Copilot skills plan

- Expanded `docs/next-phases.md` with a Copilot Studio skills strategy.
- Defined planned skills for approval review, approval decisions, risk explanation, order triage, policy lookup and escalation recommendation.
- Documented when to use skills, tools or the Orchestrator API.

## 2026-06-22 - Copilot modernization migration plan

- Expanded Phase 2 in `docs/next-phases.md` with an agent migration matrix.
- Defined which responsibilities move to modern Copilot Studio, which are partially migrated, and which stay in backend/MCP.
- Documented that Copilot Studio should become the orchestration/front-door layer, while governed workflow execution remains in the Orchestrator API and MCP tools.

## 2026-06-22 - Next phases roadmap

- Created `docs/next-phases.md` with the post-MVP roadmap.
- Defined future phases for Copilot Studio modernization, Microsoft 365 Agents SDK, RAG expansion, Power Platform tool ecosystem expansion, and Purview governance.
- Kept Purview as the final governance phase because it can involve trial/licensing/pay-as-you-go decisions.

## 2026-06-22 - Removed previous agent SDK from active runtime

- Migrated `DraftAgent` to Microsoft Agent Framework.
- Removed the previous agent SDK dependency from `apps/orchestrator-api/requirements.txt`.
- Updated `agent_runtime.py` so it only builds Microsoft Agent Framework Azure OpenAI clients.
- Updated Stage 9, agent docs, architecture docs and central project instructions so the active runtime is Microsoft Agent Framework only.
- Verified focused orchestrator tests for Draft Agent and runtime helper.



## 2026-06-22

### Architecture artifact

- Created [docs/architecture/index.html](</c:/Users/conta/codebases/MS Agentic AI/docs/architecture/index.html>) as an interactive HTML architecture map using CDN-hosted Mermaid, jQuery and Panzoom.
- Added [docs/architecture/README.md](</c:/Users/conta/codebases/MS Agentic AI/docs/architecture/README.md>) with direct opening instructions.
- Updated [docs/10-observability-polish.md](</c:/Users/conta/codebases/MS Agentic AI/docs/10-observability-polish.md>) to mark the architecture diagram as produced and point to the interactive artifact.
- Created [docs/14-final-walkthrough.md](</c:/Users/conta/codebases/MS Agentic AI/docs/14-final-walkthrough.md>) with the final core MVP demo path, talk track, proof points, and optional next phases.
- Updated [docs/10-observability-polish.md](</c:/Users/conta/codebases/MS Agentic AI/docs/10-observability-polish.md>) to mark the final walkthrough as documented.

## 2026-06-17

### Setup audit

Immediate focus: finish Stage 0 / Group 1 and Group 2 before scaffolding the project.

Installed / verified:

- `uv`: 0.11.19
- `python`: 3.11.9
- Python launcher default: 3.14.5
- `node`: v24.16.0
- `npm`: 11.13.0
- `git`: 2.54.0.windows.1
- Azure CLI: 2.87.0
- VS Code: 1.124.2
- Codex CLI: 0.140.0-alpha.2

Missing or needs action:

- Python 3.12: installed and verified via `py -3.12`
- Node.js 24.x: installed and kept as project baseline
- .NET SDK 8: installed
- Azure Functions Core Tools v4: installed and verified

Later-stage tools missing:

- Docker Desktop

Decision:

- Keep `uv` for this project. It still uses virtual environments, but manages dependencies and commands through `uv sync` and `uv run`.
- Do not install future-stage tools until needed unless setup flow requires them.
- Keep Node.js v24.16.0. Azure Functions Node.js programming model v4 officially supports Node 24.x on Functions runtime 4.25+.

### Documentation changes

- Created this `progress.md` file as the project journal.
- Updated agent instructions so future work records progress here.

### Setup changes

- Installed Python 3.12.10 with `winget install Python.Python.3.12`.
- Paused before changing Node.js because current machine already has Node v24.16.0.
- Verified Python 3.12 is available as `py -3.12`, while `python` still points to 3.11.9 in the current shell.
- Installed .NET SDK 8.0.422 with `winget install Microsoft.DotNet.SDK.8`.
- Installed Azure Functions Core Tools 4.12.0 with `npm install -g azure-functions-core-tools@4 --unsafe-perm true`.
- The npm package downloaded correctly but did not extract `func.exe`; manual extraction of `Azure.Functions.Cli.win-x64.4.12.0.zip` into the package `bin` directory fixed it.
- Installed Pulumi 3.246.0 with `winget install Pulumi.Pulumi`.
- Installed Azure Developer CLI 1.25.6 with `winget install Microsoft.Azd`.
- Installed Azurite 3.35.0 with `npm install -g azurite`.
- Installed Power Platform CLI 2.8.1 using the official Windows MSI from `https://aka.ms/PowerAppsCLI`.
- In the current shell, `pulumi`, `pac`, and `azd` were not immediately available on PATH after installation; verified them using their installed executable paths.

### Documentation updates

- Updated [docs/00-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/00-setup.md>) to use Node.js 24.x instead of Node.js 20 LTS.
- Updated setup verification steps to use `py -3.12 --version` instead of `python --version`.
- Added `ms-CopilotStudio.vscode-copilotstudio` to the recommended VS Code extensions based on current official Microsoft Copilot Studio documentation.
- Replaced the `pac` installation command in [docs/00-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/00-setup.md>) with the current official MSI-based Windows install flow.
- Added short notes to the setup doc that a fresh terminal may be needed before `pulumi`, `pac`, or `azd` are available on PATH.
- Updated [docs/00-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/00-setup.md>), [docs/01-project-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/01-project-setup.md>), [docs/05-pulumi-infrastructure.md](</c:/Users/conta/codebases/MS Agentic AI/docs/05-pulumi-infrastructure.md>), [docs/06-dataverse-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/06-dataverse-setup.md>), [CLAUDE.md](</c:/Users/conta/codebases/MS Agentic AI/CLAUDE.md>) and [context.MD](</c:/Users/conta/codebases/MS Agentic AI/context.MD>) to make Service Principal the standard Dataverse runtime authentication model.
- Shifted the documented flow so Pulumi creates the Entra app registration + Service Principal in Day 5, and Day 6 registers that identity as a Dataverse Application User with the needed security role.
- Clarified the `config.py` example in [docs/01-project-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/01-project-setup.md>) so the Dataverse env vars are explicitly marked as Service Principal runtime credentials.
- Renamed the Dataverse runtime credential examples to `DATAVERSE_SP_CLIENT_ID`, `DATAVERSE_SP_CLIENT_SECRET`, and `DATAVERSE_SP_TENANT_ID` across the docs to reflect the true ownership of those credentials and avoid ambiguous naming.

### Day 1 scaffolding

- Created the Day 1 folder structure for `mcp-server`, `apps`, `agents`, `copilot-studio`, `foundry`, `power-platform`, `infrastructure`, `data`, and `dashboards`.
- Created [README.md](</c:/Users/conta/codebases/MS Agentic AI/README.md>) with the project summary and current runtime notes.
- Created [mcp-server/pyproject.toml](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/pyproject.toml>) with the initial FastMCP/Python dependency set.
- Created [mcp-server/.env.example](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/.env.example>) using the Service Principal Dataverse variable names.
- Created [mcp-server/src/enterprise_agentops_mcp/config.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/config.py>) with env loading and baseline config constants.
- Created the mock data JSON stub files under [mcp-server/src/enterprise_agentops_mcp/data](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/data>) and initialized each file with `[]`.
- Added minimal MCP server base files: [server.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/server.py>), [mock_data_service.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/services/mock_data_service.py>), package `__init__.py` files, and basic tests in [mcp-server/tests](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/tests>).
- Verified the new Python files compile with `py -3.12 -m compileall`.
- `pytest` execution is not available yet because project dependencies have not been installed with `uv sync`.

### Day 2 initial MVP

- Populated the first mock data files: [accounts.json](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/data/accounts.json>), [contacts.json](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/data/contacts.json>), [orders.json](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/data/orders.json>), [order_items.json](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/data/order_items.json>), [shipments.json](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/data/shipments.json>), and [pricing.json](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/data/pricing.json>).
- Implemented the first MCP tools: [customers.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/customers.py>), [orders.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/orders.py>), and [shipments.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/shipments.py>).
- Updated [server.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/server.py>) to include the initial routers.
- Added tests for customers, orders, and shipments in [mcp-server/tests](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/tests>).
- Ran `uv sync` to create the project virtual environment and install base dependencies.
- Ran `uv sync --extra dev` to install `pytest`, `pytest-asyncio`, and `ruff`; `uv sync` alone does not install the optional dev dependency group.
- Verified the initial tools by direct calls through `uv run python`.
- Ran `uv run pytest tests -q` and all tests passed: `11 passed`.
- Updated [server.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/server.py>) to use `FastMCP.mount(...)` instead of `include_router(...)`, matching the installed FastMCP API.
- Validated the server with `uv run fastmcp list` and `uv run fastmcp inspect`.
- Started the MCP Inspector successfully. The UI responds on `localhost:5173` and not `127.0.0.1` because it is listening on IPv6 localhost (`::1`).

### Day 3 extended tools

- Populated [returns.json](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/data/returns.json>), [refunds.json](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/data/refunds.json>), [cases.json](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/data/cases.json>), [activities.json](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/data/activities.json>), and [knowledge_articles.json](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/data/knowledge_articles.json>) with the next mock dataset.
- Added new tool modules: [accounts.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/accounts.py>), [returns.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/returns.py>), [cases.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/cases.py>), [knowledge.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/knowledge.py>), [approvals.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/approvals.py>), [cost.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/cost.py>), [observability.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/observability.py>), and [evaluation.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/evaluation.py>).
- Extended [server.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/server.py>) so the MCP server now mounts all current tool groups.
- Added tests for the new tool set under [mcp-server/tests](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/tests>).
- Verified the full MCP tool set with `uv run fastmcp inspect` and `uv run fastmcp list`.
- Ran `uv run pytest tests -q` and all tests passed: `26 passed`.
- Current MCP server surface now exposes `16` tools.

### Day 4 orchestrator API

- `func init . --python` succeeded in [apps/orchestrator-api](</c:/Users/conta/codebases/MS Agentic AI/apps/orchestrator-api>) and created the base Azure Functions Python v2 project files.
- The `func new ...` trigger scaffolds did not complete, so the route handlers were implemented manually in the Python v2 model instead of waiting on template generation.
- Added [function_app.py](</c:/Users/conta/codebases/MS Agentic AI/apps/orchestrator-api/function_app.py>) routes for:
  - `POST /api/agents/webshop/order-support`
  - `POST /api/agents/customer-case/summarise` placeholder
  - `GET /api/agent-runs/{runId?}` placeholder
- Added [src/shared/mcp_client.py](</c:/Users/conta/codebases/MS Agentic AI/apps/orchestrator-api/src/shared/mcp_client.py>) as the local wrapper that imports the MCP server Python package directly for MVP use.
- Added [src/webshop_order_support.py](</c:/Users/conta/codebases/MS Agentic AI/apps/orchestrator-api/src/webshop_order_support.py>) with the first orchestration flow across customer, order, shipment, returns, refunds, knowledge, evaluation, approval, cost, and logging.
- Updated [local.settings.json](</c:/Users/conta/codebases/MS Agentic AI/apps/orchestrator-api/local.settings.json>) with the local MVP settings and [requirements.txt](</c:/Users/conta/codebases/MS Agentic AI/apps/orchestrator-api/requirements.txt>) with the required dependencies.
- Created a dedicated `.venv` for `apps/orchestrator-api` and installed the app dependencies with `uv`.
- Added tests in [apps/orchestrator-api/tests/test_webshop_order_support.py](</c:/Users/conta/codebases/MS Agentic AI/apps/orchestrator-api/tests/test_webshop_order_support.py>).
- Verified the orchestrator flow with:
  - `.venv\\Scripts\\python.exe -m pytest tests -q` -> `2 passed`
  - direct handler execution returning HTTP-style success payload for `john.smith@contoso.com`
- Fixed an Azure Functions load issue caused by a placeholder route parameter name and confirmed the local endpoint response over HTTP.
- Local `POST http://localhost:7071/api/agents/webshop/order-support` returned the expected JSON payload for `john.smith@contoso.com`.

### Public repo hardening

- Added a root [.gitignore](</c:/Users/conta/codebases/MS Agentic AI/.gitignore>) covering virtual environments, local settings, logs, editor files, and local storage artifacts.
- Updated [README.md](</c:/Users/conta/codebases/MS Agentic AI/README.md>) to present the project safely and clearly for a public audience.
- Confirmed that the repository contains placeholder/example credential fields rather than real secrets in tracked source files.
- Initialized the local Git repository with `git init`.

## 2026-06-18

### Azure naming and bootstrap

- Added [infrastructure/config/azure-context.example.json](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/config/azure-context.example.json>) as the versioned template for Azure subscription, environment, region, tags, and generated resource names.
- Added [infrastructure/scripts/Initialize-AzureContext.ps1](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/scripts/Initialize-AzureContext.ps1>) to log in with Azure CLI if needed, list subscriptions, prompt for workload/environment/region/instance, generate Microsoft CAF-style names, and save `infrastructure/config/azure-context.json`.
- Updated [.gitignore](</c:/Users/conta/codebases/MS Agentic AI/.gitignore>) to keep the real local `azure-context.json` out of source control.
- Updated [docs/00-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/00-setup.md>), [docs/05-pulumi-infrastructure.md](</c:/Users/conta/codebases/MS Agentic AI/docs/05-pulumi-infrastructure.md>), [README.md](</c:/Users/conta/codebases/MS Agentic AI/README.md>), and [context.MD](</c:/Users/conta/codebases/MS Agentic AI/context.MD>) so the project now explicitly uses Microsoft Cloud Adoption Framework naming guidance and links the Microsoft source URLs.
- Replaced the old manual `az group create --name rg-agentops-dev --location uksouth` setup step with the new bootstrap-script flow, so subscription selection and naming are captured once and then reused by Pulumi.
- Shifted the Azure environment model to an ephemeral study setup: the workload resource group is disposable, but recovery dumps must live in persistent blob storage outside the disposable RG.
- Added sequence tracking to the Azure context model so disposable resource names move from `001` to `002`, `003`, and so on after decommissioning, avoiding Azure name reuse collisions.
- Added [infrastructure/scripts/AzureContext.Common.ps1](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/scripts/AzureContext.Common.ps1>) to centralize naming/context generation logic.
- Added [infrastructure/scripts/Remove-AzureEnvironment.ps1](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/scripts/Remove-AzureEnvironment.ps1>) for one-line teardown of the workload resource group plus automatic sequence advancement in `azure-context.json`.
- Switched the planned Pulumi implementation language from TypeScript to C#.
- Added the initial Pulumi C# scaffold in [infrastructure/pulumi](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/pulumi>) with [Pulumi.yaml](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/pulumi/Pulumi.yaml>), [Pulumi.dev.yaml](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/pulumi/Pulumi.dev.yaml>), [EnterpriseAgentOps.Infrastructure.csproj](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/pulumi/EnterpriseAgentOps.Infrastructure.csproj>), [Program.cs](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/pulumi/Program.cs>), [AzureContext.cs](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/pulumi/AzureContext.cs>), and [AzureContextLoader.cs](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/pulumi/AzureContextLoader.cs>).
- The Pulumi C# scaffold now reads `infrastructure/config/azure-context.json` as a required input and currently provisions the disposable workload resource group plus the persistent recovery resource group, recovery storage account, and recovery blob container.
- Corrected the NuGet provider package to `Pulumi.AzureNative` for the C# project and verified the scaffold with `dotnet restore` and `dotnet build`, both successful.
- Expanded [infrastructure/pulumi/Program.cs](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/pulumi/Program.cs>) to provision the core Azure workload resources from `azure-context.json`: workload storage account, Log Analytics workspace, Application Insights, Key Vault, Linux Consumption Function App plan, and Linux Function App configured for Python 3.12.
- Verified the expanded Pulumi C# scaffold still compiles successfully with `dotnet build`.
- Deleted the previously created Azure resource groups `rg-agentops-dev-001` and `rg-agentops-state` after the UK South Function/App Service quota block.
- Updated [infrastructure/scripts/AzureContext.Common.ps1](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/scripts/AzureContext.Common.ps1>) so the default recovery storage account name also follows the active sequence instead of always reusing `001`.
- Rewrote the local [infrastructure/config/azure-context.json](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/config/azure-context.json>) to use `eastus` / `eus` with sequence `002`, producing new resource names such as `rg-agentops-dev-002` and `stagentopsstateeus002`.
- Reworked the Azure Functions infrastructure in [infrastructure/pulumi/Program.cs](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/pulumi/Program.cs>) to stop using legacy Linux Consumption `Y1` and instead use the Microsoft-recommended Flex Consumption shape: `FC1` plan, `functionAppConfig`, deployment blob container, and managed-identity-based storage access.
- Added [infrastructure/pulumi/GuidUtility.cs](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/pulumi/GuidUtility.cs>) to generate deterministic GUIDs for role assignments.
- Verified the Flex Consumption Pulumi C# code compiles successfully with `dotnet build`.
- Added `Pulumi.AzureAD` to the Pulumi C# project and extended [Program.cs](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/pulumi/Program.cs>) to create the Dataverse runtime Entra App Registration, Service Principal, client secret, and corresponding Key Vault secrets for `DATAVERSE-SP-CLIENT-ID`, `DATAVERSE-SP-CLIENT-SECRET`, and `DATAVERSE-SP-TENANT-ID`.
- Verified the identity-enabled Pulumi C# project still builds successfully with `dotnet build`.
- Confirmed the Power Platform admin center didn't immediately surface the Pulumi-created app registration in the Dataverse Application User picker even though the tenant matched.
- Installed the Power Platform PowerShell modules and registered the existing Entra app with Microsoft Power Platform using:
  - `Add-PowerAppsAccount -Endpoint prod -TenantID 153c340e-c72a-4676-a178-2f5cb640bd7c`
  - `New-PowerAppManagementApp -ApplicationId "f6861f6e-c2f3-4b09-b29f-f836d8f7137b"`
  - `Get-PowerAppManagementApp -ApplicationId "f6861f6e-c2f3-4b09-b29f-f836d8f7137b"`
- Updated [docs/06-dataverse-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/06-dataverse-setup.md>) to reflect the real flow: Pulumi creates the Entra identity, Power Platform PowerShell registers that app with Microsoft Power Platform, and only then can the Dataverse Application User be created reliably.
- `pac admin assign-user --application-user` confirmed that it only assigns a role to an existing Dataverse Application User; it does not create one.
- `pac admin create-service-principal --environment "https://marcojrdigitalventuresltddefault.crm11.dynamics.com" --name "agentops-dataverse-dev-002" --role "System Administrator"` succeeded, but created a new Entra app + Service Principal + client secret + Dataverse Application User instead of reusing the Pulumi-created identity.
- The PAC-created Dataverse-ready identity returned:
  - Application Id: `acdfeb48-7b4f-44e6-8a90-dd75d10a7ac5`
  - Service Principal Id: `edc71b3e-4986-4ccd-80a4-2e5d6302b5c4`
  - System User Id: `910c3861-336b-f111-ab0d-7c1e5203a276`
- This means the project currently has two separate identities:
  - Pulumi-created identity for Azure-side IaC ownership
  - PAC-created identity that is actually wired into Dataverse as an Application User
- Re-aligned the docs as a proper case-study record:
  - the intended architecture remains a single Pulumi-owned Service Principal reused by Dataverse
  - the PAC-created identity is now explicitly documented as a workaround experiment, not the final design
  - [docs/05-pulumi-infrastructure.md](</c:/Users/conta/codebases/MS Agentic AI/docs/05-pulumi-infrastructure.md>), [docs/06-dataverse-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/06-dataverse-setup.md>), [docs/07-dataverse-integration.md](</c:/Users/conta/codebases/MS Agentic AI/docs/07-dataverse-integration.md>), and [README.md](</c:/Users/conta/codebases/MS Agentic AI/README.md>) now separate:
    - target architecture
    - observed platform behavior
    - temporary workaround
    - final project direction
- Corrected [docs/05-pulumi-infrastructure.md](</c:/Users/conta/codebases/MS Agentic AI/docs/05-pulumi-infrastructure.md>) so it no longer claims `pulumi up` is still pending; the doc now reflects that the real deployment already succeeded.
- Executed the real root-cause investigation for the Pulumi-owned Dataverse identity path:
  - `pac admin application register --application-id "f6861f6e-c2f3-4b09-b29f-f836d8f7137b"` succeeded
  - `pac admin assign-user --application-user` still failed because the Application User did not exist
  - direct `POST /api/data/v9.2/applicationusers` failed with `Create of ApplicationUser is only allowed in FirstPartySolutionContext`
  - direct `POST /api/data/v9.2/systemusers` with the Pulumi app failed with `We didn't find that application ID ... in your Azure Active Directory`
- That test pinned the real blocker: tenant mismatch.
  - Azure / Pulumi tenant: `153c340e-c72a-4676-a178-2f5cb640bd7c`
  - Dataverse / PAC-created identity tenant: `92914f74-fa9a-4710-bf05-c9333cb643c9`
- Added [infrastructure/scripts/Test-DataverseTenantAlignment.ps1](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/scripts/Test-DataverseTenantAlignment.ps1>) so the project can fail fast when Azure and Dataverse are targeting different Entra tenants.
- Updated [docs/05-pulumi-infrastructure.md](</c:/Users/conta/codebases/MS Agentic AI/docs/05-pulumi-infrastructure.md>) and [docs/06-dataverse-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/06-dataverse-setup.md>) to record the tenant-mismatch finding as the concrete reason the single Pulumi-owned identity could not be completed in the current environment pairing.
- Project decision updated: we will keep using the PAC-created Dataverse identity in the current repo/runtime, and document the Pulumi-owned identity as the target architecture that is blocked by tenant mismatch in this environment.
- Updated [docs/06-dataverse-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/06-dataverse-setup.md>), [docs/05-pulumi-infrastructure.md](</c:/Users/conta/codebases/MS Agentic AI/docs/05-pulumi-infrastructure.md>), and [README.md](</c:/Users/conta/codebases/MS Agentic AI/README.md>) so they now clearly separate:
  - target architecture
  - current implementation we are actually using
- Removed the leftover generic `.env` placeholder block from [docs/06-dataverse-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/06-dataverse-setup.md>) so the doc now points only to the PAC-created Dataverse credentials for the current environment.
- Started the real Stage 7 code path:
  - added [mcp-server/src/enterprise_agentops_mcp/services/dataverse_service.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/services/dataverse_service.py>) with MSAL client-credentials auth plus `dv_get` / `dv_post`
  - updated [mcp-server/.env.example](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/.env.example>) to state that the current Dataverse credentials come from the PAC-created identity
  - implemented Dataverse mode in [customers.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/customers.py>), [orders.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/orders.py>), [shipments.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/shipments.py>), [returns.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/returns.py>), and [observability.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/observability.py>)
  - added focused Dataverse-mode tests in [mcp-server/tests/test_dataverse_mode.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/tests/test_dataverse_mode.py>)
  - verified with `uv run pytest tests -q` -> `29 passed`
  - verified Python compilation with `py -3.12 -m compileall src`
- Updated [docs/07-dataverse-integration.md](</c:/Users/conta/codebases/MS Agentic AI/docs/07-dataverse-integration.md>) so the Day 7 checklist now reflects what is already implemented and what is still pending.
- Verified the live Dataverse connection with the PAC-created identity:
  - token acquisition now succeeds
  - direct `contacts` read returns `200 OK`
  - [customers.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/customers.py>) was corrected to use the real standard Dataverse fields `address1_line1` and `address1_postalcode` instead of nonexistent custom contact fields
  - `get_customer_by_email('someone_a@example.com')` now works against live Dataverse and returns the sample contact `Yvonne McKay (sample)`
- Confirmed the next real blocker is no longer auth; it is missing custom Dataverse schema:
  - `cr_order`
  - `cr_orderitem`
  - `cr_shipment`
  - `cr_returnrequest`
  - `cr_refund`
  - `cr_agentrun`
  all return Dataverse `404` because those tables do not exist yet in the current environment.
- Improved [dataverse_service.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/services/dataverse_service.py>) so Dataverse HTTP failures now raise explicit runtime errors with the entity name and response body instead of a vague bare `httpx` status failure.
- Added a scripted Dataverse schema/deploy path:
  - [power-platform/dataverse-schema/schema.v1.json](</c:/Users/conta/codebases/MS Agentic AI/power-platform/dataverse-schema/schema.v1.json>)
  - [power-platform/scripts/Dataverse.Common.ps1](</c:/Users/conta/codebases/MS Agentic AI/power-platform/scripts/Dataverse.Common.ps1>)
  - [power-platform/scripts/Deploy-AgentOpsDataverseSchema.ps1](</c:/Users/conta/codebases/MS Agentic AI/power-platform/scripts/Deploy-AgentOpsDataverseSchema.ps1>)
  - [power-platform/scripts/Seed-AgentOpsDataverseData.ps1](</c:/Users/conta/codebases/MS Agentic AI/power-platform/scripts/Seed-AgentOpsDataverseData.ps1>)
  - [power-platform/dataverse-schema/README.md](</c:/Users/conta/codebases/MS Agentic AI/power-platform/dataverse-schema/README.md>)
- Chose an honest v1 schema design for automation:
  - custom `cr_*` references are stored as text key fields
  - business identifiers use `...key` columns to avoid collision with Dataverse internal `...id` GUID primary keys
- Updated MCP Dataverse code to match that scripted schema shape:
  - [orders.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/orders.py>)
  - [shipments.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/shipments.py>)
  - [returns.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/returns.py>)
  - [observability.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/observability.py>)
- Updated the documentation to point to the scripted schema path instead of hand-building everything in the Maker UI:
  - [docs/06-dataverse-setup.md](</c:/Users/conta/codebases/MS Agentic AI/docs/06-dataverse-setup.md>)
  - [docs/07-dataverse-integration.md](</c:/Users/conta/codebases/MS Agentic AI/docs/07-dataverse-integration.md>)
- Added [mcp-server/tests/conftest.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/tests/conftest.py>) so the test suite still defaults to `mock` mode even when the local `.env` is set to `dataverse`.
- Re-ran MCP tests successfully after the schema/code alignment changes: `29 passed`.
- Dry-ran the schema deploy with:
  - `powershell -ExecutionPolicy Bypass -File .\power-platform\scripts\Deploy-AgentOpsDataverseSchema.ps1 -WhatIf`
  and it produced the full create plan for all AgentOps custom tables and columns without errors.
- Created the local ignored file [mcp-server/.env](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/.env>) with `MCP_DATA_MODE=dataverse` and the Dataverse Service Principal placeholders ready for the PAC-created identity values.
- Investigated the Dataverse schema failure and confirmed `cr_order` had been partially created already; the real blocker was no longer missing auth, but Dataverse customization serialization and a partially-created table.
- Aligned the scripted schema with Dataverse's actual logical-name behavior for reference-like text fields:
  - `cr_shipmentkeyref`
  - `cr_orderkeyref`
  - `cr_orderitemkeyref`
  - `cr_returnkeyref`
- Updated [power-platform/dataverse-schema/schema.v1.json](</c:/Users/conta/codebases/MS Agentic AI/power-platform/dataverse-schema/schema.v1.json>), [orders.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/orders.py>), [shipments.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/shipments.py>), [returns.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/returns.py>), [Seed-AgentOpsDataverseData.ps1](</c:/Users/conta/codebases/MS Agentic AI/power-platform/scripts/Seed-AgentOpsDataverseData.ps1>), and the Dataverse docs to use those real field names.
- Added retry handling for Dataverse `EntityCustomization` locks in [Dataverse.Common.ps1](</c:/Users/conta/codebases/MS Agentic AI/power-platform/scripts/Dataverse.Common.ps1>) so schema deploy no longer dies just because Dataverse is still processing the previous metadata change.
- Successfully completed the real schema deployment with:
  - `powershell -ExecutionPolicy Bypass -File .\power-platform\scripts\Deploy-AgentOpsDataverseSchema.ps1`
- Added [power-platform/scripts/Clear-AgentOpsDataverseSeed.ps1](</c:/Users/conta/codebases/MS Agentic AI/power-platform/scripts/Clear-AgentOpsDataverseSeed.ps1>) to remove only the project's seeded `accounts`, `contacts`, and custom `cr_*` rows before reseeding.
- Fixed the seed script's PowerShell upsert behavior so single-row reads are no longer unwrapped incorrectly, which had been causing repeated duplicate inserts.
- Cleaned the Dataverse environment and re-seeded it successfully:
  - `powershell -ExecutionPolicy Bypass -File .\power-platform\scripts\Clear-AgentOpsDataverseSeed.ps1`
  - `powershell -ExecutionPolicy Bypass -File .\power-platform\scripts\Seed-AgentOpsDataverseData.ps1`
- Verified that reseeding is now idempotent: the second seed run updates rows instead of creating duplicates.
- Corrected the seed linkage so `cr_orders.cr_contactid` and `cr_orders.cr_accountid` now store the real Dataverse GUIDs for the seeded contacts/accounts, making the real tool chain work end-to-end.
- Verified the live Dataverse-backed MCP flow now works for the seeded business scenario:
  - `get_customer_by_email('john.smith@contoso.com')`
  - `get_latest_order(<returned contactId>)`
  - `get_shipment_status('ship-9001')`
  - `get_returns_for_order('ord-1001')`
  - `get_refunds_for_order('ord-1001')`
- Implemented Dataverse mode in [approvals.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/approvals.py>) so `create_approval_request` now writes to `cr_approvalrequests` instead of stopping with `NotImplementedError`.
- Added Dataverse coverage to [mcp-server/tests/test_approvals.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/tests/test_approvals.py>) and verified:
  - `uv run pytest tests/test_approvals.py tests/test_dataverse_mode.py -q` -> `6 passed`
  - `py -3.12 -m compileall src`
- Verified a real Dataverse approval insert by creating an approval request for `ord-1001` and reading it back from `cr_approvalrequests` with key `apr-4f08a39d`.
- Updated [docs/07-dataverse-integration.md](</c:/Users/conta/codebases/MS Agentic AI/docs/07-dataverse-integration.md>) so Day 7 now records `create_approval_request` as implemented.
- Tested the orchestrator end-to-end in Dataverse mode by running [handle_webshop_order_support](</c:/Users/conta/codebases/MS Agentic AI/apps/orchestrator-api/src/webshop_order_support.py>) directly from the Azure Functions app environment.
- Added `msal` to [apps/orchestrator-api/requirements.txt](</c:/Users/conta/codebases/MS Agentic AI/apps/orchestrator-api/requirements.txt>) and installed it into the local orchestrator virtual environment, because the Function app process also imports the MCP Dataverse client code path.
- Confirmed the Dataverse-backed orchestrator now gets past customer/order/shipment/returns/refunds and then stops exactly at `search_knowledge_articles`.
- Confirmed the current blocker is Stage 8, not Dataverse:
  - `AZURE_AI_SEARCH_ENDPOINT` is empty in the local `.env`
  - `AZURE_AI_SEARCH_KEY` is empty in the local `.env`
  - [knowledge.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/knowledge.py>) intentionally raises `NotImplementedError("Azure AI Search mode not yet implemented - see Stage 8")` for non-mock mode
- Result: the webshop orchestrator is not yet end-to-end complete in `MCP_DATA_MODE=dataverse` until Stage 8 Azure AI Search / Secure RAG is implemented or wired.
- Implemented the Stage 8 Azure AI Search code path:
  - added [azure_search_service.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/services/azure_search_service.py>)
  - updated [knowledge.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/tools/knowledge.py>) to use `MCP_KNOWLEDGE_MODE=search`
  - added sample policy documents under [data/sample-documents](</c:/Users/conta/codebases/MS Agentic AI/data/sample-documents>)
  - added [create_search_index.py](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/scripts/create_search_index.py>) and [ingest_documents.py](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/scripts/ingest_documents.py>)
  - updated [mcp-server/.env.example](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/.env.example>) with `MCP_KNOWLEDGE_MODE`
- Added Azure AI Search to the Pulumi C# infrastructure in [infrastructure/pulumi/Program.cs](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/pulumi/Program.cs>) and verified the Pulumi project still builds with `dotnet build`.
- Added `azure-search-documents` to [apps/orchestrator-api/requirements.txt](</c:/Users/conta/codebases/MS Agentic AI/apps/orchestrator-api/requirements.txt>) and installed it in the local orchestrator environment because the Function runtime imports the MCP knowledge service path too.
- Added knowledge-mode tests in [mcp-server/tests/test_knowledge.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/tests/test_knowledge.py>) and re-ran:
  - `uv run pytest tests/test_knowledge.py tests/test_approvals.py tests/test_dataverse_mode.py -q` -> `9 passed`
  - `py_compile` validation for the new Azure Search scripts and service
- Updated [docs/08-secure-rag.md](</c:/Users/conta/codebases/MS Agentic AI/docs/08-secure-rag.md>) to reflect the real current implementation:
  - Azure AI Search code path is implemented
  - initial retrieval is classic full-text Azure AI Search
  - vector embeddings are intentionally not wired yet
- Attempted to preview the Pulumi stack so the Azure AI Search resource could actually be provisioned, but deployment is currently blocked because the shell does not have `PULUMI_CONFIG_PASSPHRASE` set for the local secrets backend.
- User ran `pulumi up` and created the Azure AI Search service in the workload resource group.
- Verified Azure AI Search exists and is running:
  - service: `srch-agentops-dev-002`
  - resource group: `rg-agentops-dev-002`
  - location: East US
  - SKU: free
- Retrieved the Azure AI Search admin key without printing it and updated the local ignored [mcp-server/.env](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/.env>) with:
  - `MCP_KNOWLEDGE_MODE=search`
  - `AZURE_AI_SEARCH_ENDPOINT=https://srch-agentops-dev-002.search.windows.net`
  - `AZURE_AI_SEARCH_INDEX=enterprise-knowledge`
  - `AZURE_AI_SEARCH_KEY=<local secret>`
- Updated [create_search_index.py](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/scripts/create_search_index.py>) and [ingest_documents.py](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/scripts/ingest_documents.py>) so they load `mcp-server/.env` directly.
- Created the Azure AI Search index with:
  - `uv run --project mcp-server python infrastructure/scripts/create_search_index.py`
- Ingested 10 policy documents into Azure AI Search with:
  - `uv run --project mcp-server python infrastructure/scripts/ingest_documents.py`
- Verified live `search_knowledge_articles('delivery delay compensation refund approval policy', 3)` now returns Azure AI Search results including:
  - `delivery-delay-policy`
  - `refund-policy`
  - `customer-compensation-policy`
- Re-ran the local Azure Functions orchestrator flow against Dataverse + Azure AI Search and it now completes successfully with status `200`.
- Verified the end-to-end response for `john.smith@contoso.com` includes:
  - customer `John Smith`
  - order `WEB-1001`
  - delayed shipment `ship-9001`
  - refund pending approval
  - generated approval request `apr-66b885ad`
  - knowledge results from Azure AI Search
  - agent run id `run-779c333e`
- Updated [docs/08-secure-rag.md](</c:/Users/conta/codebases/MS Agentic AI/docs/08-secure-rag.md>) to mark the Stage 8 Azure AI Search path as provisioned, indexed, ingested, and verified.
- Implemented Service Bus in the Pulumi C# infrastructure:
  - namespace: `sbns-agentops-dev-002`
  - SKU: Basic
  - queues: `approval-requests`, `agent-run-events`, `workflow-deadletter`
  - runtime authorization rule: `agentops-runtime`
  - Key Vault secret: `AZURE-SERVICE-BUS-CONNECTION-STRING`
- Verified the Pulumi Service Bus change with:
  - `dotnet build`
  - `pulumi preview`
  - `pulumi up --yes`
- Verified the deployed Service Bus namespace and queues with Azure CLI.
- Retrieved the Service Bus connection string without printing it and added it to the local ignored [mcp-server/.env](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/.env>) as `AZURE_SERVICE_BUS_CONNECTION_STRING`.
- Added the Service Bus dependency to:
  - [mcp-server/pyproject.toml](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/pyproject.toml>)
  - [apps/orchestrator-api/requirements.txt](</c:/Users/conta/codebases/MS Agentic AI/apps/orchestrator-api/requirements.txt>)
- Installed the Service Bus package in the local orchestrator virtual environment.
- Ran a real Service Bus smoke test by sending and receiving an `AgentRunCompleted` message through the `agent-run-events` queue.
- Updated [docs/05-pulumi-infrastructure.md](</c:/Users/conta/codebases/MS Agentic AI/docs/05-pulumi-infrastructure.md>) so Azure AI Search and Service Bus are documented as implemented infrastructure, not pending items.
- Added Service Bus queue names to the local ignored [mcp-server/.env](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/.env>) and to [mcp-server/.env.example](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/.env.example>):
  - `SERVICE_BUS_APPROVAL_REQUESTS_QUEUE=approval-requests`
  - `SERVICE_BUS_AGENT_RUN_EVENTS_QUEUE=agent-run-events`
  - `SERVICE_BUS_WORKFLOW_DEADLETTER_QUEUE=workflow-deadletter`
- Added Service Bus settings to [mcp-server/src/enterprise_agentops_mcp/config.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/config.py>) and verified it compiles with `uv run python -m py_compile`.
- Added [mcp-server/src/enterprise_agentops_mcp/services/service_bus_service.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/services/service_bus_service.py>) with real Service Bus JSON publishing for:
  - `ApprovalRequestCreated`
  - `AgentRunCompleted`
- Updated [apps/orchestrator-api/src/webshop_order_support.py](</c:/Users/conta/codebases/MS Agentic AI/apps/orchestrator-api/src/webshop_order_support.py>) so the order-support flow now publishes:
  - approval events to `approval-requests`
  - completed run events to `agent-run-events`
- Updated [mcp-server/src/enterprise_agentops_mcp/config.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/config.py>) to explicitly load `mcp-server/.env`, so the orchestrator can find the MCP environment settings even when running from `apps/orchestrator-api`.
- Added [infrastructure/scripts/peek_service_bus_queue.py](</c:/Users/conta/codebases/MS Agentic AI/infrastructure/scripts/peek_service_bus_queue.py>) to inspect Service Bus messages without removing them from the queue.
- Added tests for the Service Bus publisher and protected the orchestrator unit test from publishing to the real queue.
- Verified:
  - MCP focused tests: `3 passed`
  - orchestrator tests: `2 passed`
  - Python compile checks for the new Service Bus service and peek script
- Ran the real Dataverse + Azure AI Search + Service Bus orchestration for `john.smith@contoso.com`.
- Confirmed real Service Bus messages were published and visible:
  - `agent-run-events`: `AgentRunCompleted` for `run-bc338ea9`
  - `approval-requests`: `ApprovalRequestCreated` for `apr-8062a792`
- Changed the active LLM provider strategy from Anthropic + OpenAI to OpenAI + Gemini because Anthropic API credits are not available.
- Updated the local ignored [mcp-server/.env](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/.env>) and versioned [mcp-server/.env.example](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/.env.example>) to use:
  - `OPENAI_API_KEY`
  - `GEMINI_API_KEY`
  - `AI_PRIMARY_PROVIDER=openai`
  - `AI_PRIMARY_MODEL=gpt-5-mini`
  - `AI_SECONDARY_PROVIDER=gemini`
  - `AI_SECONDARY_MODEL=gemini-3.5-flash`
- Removed Anthropic from the active MCP Python dependency set and added `google-genai`.
- Added [docs/ai-gemini.md](</c:/Users/conta/codebases/MS Agentic AI/docs/ai-gemini.md>) with the Gemini setup path and official Google documentation links.
- Updated the orchestrator so `modelUsed` and `vendor` now come from [config.py](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/src/enterprise_agentops_mcp/config.py>) instead of being hardcoded to Claude/Anthropic.
- Updated active docs to describe OpenAI as primary provider and Gemini as secondary provider.
- Updated mock pricing/data so workshop examples no longer report Claude/Anthropic as the active model path.
- Verified:
  - MCP tests: `33 passed`
  - orchestrator tests: `2 passed`
  - `config.py` compile check passed
- Corrected the LLM provider strategy for the Microsoft case:
  - Azure OpenAI is now the primary enterprise provider
  - direct OpenAI remains a dev/lab comparison path
  - Gemini remains the secondary comparison/lab provider
- Updated [mcp-server/.env.example](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/.env.example>) and local ignored [mcp-server/.env](</c:/Users/conta/codebases/MS Agentic AI/mcp-server/.env>) so the active provider settings are:
  - `AI_PRIMARY_PROVIDER=azure_openai`
  - `AI_PRIMARY_VENDOR=Azure OpenAI`
  - `AI_PRIMARY_MODEL=gpt-5-mini`
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_API_KEY`
  - `AZURE_OPENAI_DEPLOYMENT_NAME`
- Added [docs/ai-azure-openai.md](</c:/Users/conta/codebases/MS Agentic AI/docs/ai-azure-openai.md>) and linked it from the repo docs.
- Added `Azure OpenAI / gpt-5-mini` to the pricing table so cost calculation works when the orchestrator logs the enterprise provider.
- Re-verified:
  - MCP config/cost tests: `5 passed`
  - orchestrator tests: `2 passed`
  - `pricing.json` is valid JSON
- Updated Pulumi C# infrastructure to provision Azure OpenAI as part of the Microsoft Agentic AI case:
  - Azure OpenAI account: `oai-agentops-dev-eus-002`
  - deployment: `gpt-5-mini`
  - model: `gpt-5-mini`
  - Key Vault secrets: `AZURE-OPENAI-ENDPOINT`, `AZURE-OPENAI-API-KEY`, `AZURE-OPENAI-DEPLOYMENT-NAME`
- Updated CAF-style naming generation to include `resources.azureOpenAi`.
- Updated `infrastructure/config/azure-context.example.json` and local ignored `infrastructure/config/azure-context.json` with the Azure OpenAI resource name.
- Removed direct OpenAI API usage from the active runtime environment example and config checks; Azure OpenAI is now the primary provider and Gemini is the comparison provider.
- Added `infrastructure/scripts/Sync-AzureOpenAiEnv.ps1` to sync Azure OpenAI endpoint/key/deployment into the local ignored `.env` without printing secrets.
- Ran:
  - `dotnet build` for Pulumi: passed
  - MCP tests: `33 passed`
  - orchestrator tests: `2 passed`
  - `pulumi preview`: planned 5 Azure OpenAI/Key Vault resources
  - `pulumi up --yes`: created 5 resources
  - Azure OpenAI smoke test: returned `azure-openai-ok`
- Persisted `PULUMI_CONFIG_PASSPHRASE` in the Windows user environment to avoid typing the Pulumi passphrase in future terminals.
- Investigated modern Azure OpenAI model deployment support after `gpt-5-mini` initially failed.
- Confirmed through Azure ARM model availability API that GPT-5 family models are visible in multiple regions, including East US, East US 2, Sweden Central, South Central US, Poland Central, UK South, and West Europe.
- Confirmed the real issue was missing `model.version` in Pulumi, not model age, quota, or basic region support.
- Created a temporary CLI probe deployment for `gpt-5-mini` with:
  - model version: `2025-08-07`
  - SKU: `GlobalStandard`
- Updated Pulumi C# to deploy Azure OpenAI as:
  - deployment: `gpt-5-mini`
  - model: `gpt-5-mini`
  - version: `2025-08-07`
  - SKU: `GlobalStandard`
- Removed the temporary CLI probe deployment after Pulumi successfully created the managed deployment.
- Synced local `.env` to `AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5-mini`.
- Verified Azure has exactly one deployment on the account:
  - `gpt-5-mini`
  - model `gpt-5-mini`
  - version `2025-08-07`
  - SKU `GlobalStandard`
- Observed GPT-5 API behavior:
  - `max_tokens` is rejected
  - `max_completion_tokens` is required
  - low token limits can be consumed entirely as reasoning tokens
  - this SKU currently exposes tight rate limits in the test subscription
- Re-verified:
  - Pulumi `dotnet build`: passed
  - MCP tests: `33 passed`
  - orchestrator tests: `2 passed`
- Added real Azure OpenAI summary generation to the orchestrator:
  - new client: `apps/orchestrator-api/src/shared/azure_openai_client.py`
  - model/deployment: `gpt-5-mini`
  - API uses `max_completion_tokens`, not `max_tokens`
  - request uses `reasoning_effort=low`
- Replaced the handcrafted order support summary in `apps/orchestrator-api/src/webshop_order_support.py` with Azure OpenAI generated text.
- Updated orchestrator tests to mock only the LLM call while keeping the rest of the flow covered.
- Ran a real Azure OpenAI client smoke test:
  - model returned: `gpt-5-mini-2025-08-07`
  - summary generated successfully
- Ran the full real orchestration for `john.smith@contoso.com`:
  - status: `200`
  - run id: `run-29db5384`
  - approval id: `apr-ba893474`
  - model used: `gpt-5-mini`
  - generated support summary from live Dataverse, Azure AI Search, Service Bus, and Azure OpenAI
- Re-verified:
  - MCP tests: `33 passed`
  - orchestrator tests: `2 passed`
- Installed the previous agent SDK in the orchestrator API virtual environment:
  - package: `previous-agent-sdk[azure]`
  - installed version observed locally: `previous-agent-sdk 1.36.0`
- Added the first the previous agent SDK agent:
  - `apps/orchestrator-api/src/agents/draft_agent.py`
  - class: `DraftAgent`
  - service: `AzureChatCompletion`
  - deployment: `gpt-5-mini`
  - API version: `2024-10-21`
  - settings: `max_completion_tokens=1600`, `reasoning_effort=low`
- Updated `apps/orchestrator-api/src/shared/azure_openai_client.py` so the existing orchestrator path now delegates summary generation to `DraftAgent`.
- Inspected the previous agent SDK `FunctionResult` and confirmed token usage/model are available through `result.get_inner_content()`.
- Ran a real Draft Agent smoke test:
  - model: `gpt-5-mini-2025-08-07`
  - prompt tokens: `192`
  - completion tokens: `207`
  - summary generated successfully
- Re-verified:
  - orchestrator tests: `2 passed`
  - MCP tests: `33 passed`

## 2026-06-20 - Documentation naming and agent framework alignment

- Updated project documentation to use `Microsoft Foundry (formerly Azure AI Foundry)` as the primary product name.
- Updated active model references to Azure OpenAI `gpt-5-mini`.
- Clarified that Microsoft Agent Framework is the modern pro-code direction.
- Documented that only the Draft Agent remains on the previous agent SDK, intentionally, for comparison, didactics and legacy understanding.
- Removed Claude/Anthropic from active agent definitions; Anthropic remains only as an optional legacy reference.
- Corrected Pulumi documentation to C# and kept Azure OpenAI + Gemini as the active comparison path.

## 2026-06-20 - Agent code commenting rule

- Updated agent instruction docs to require short step-by-step English comments in agent/orchestration code.
- Added educational step comments to `apps/orchestrator-api/src/agents/draft_agent.py`.
- Verified `draft_agent.py` syntax with `python -m py_compile`.

## 2026-06-20 - PC transfer handoff

- Created `pc-transfer.txt` at the repository root for continuing the project on another Linux machine.
- Included current architecture decisions, implemented components, required local env vars, Linux setup commands, smoke tests, and the recommended next prompt for the next Codex.

## 2026-06-21 - Windows resume after Linux work

- Read the updated handoff/progress from the other PC and confirmed the new Approval Console work is present locally.
- Verified MCP tests: `35 passed`.
- Initial orchestrator test run failed because the local Windows venv did not have `agent_framework` installed.
- Installed orchestrator dependencies and found the unpinned `agent-framework` requirement resolved to an incompatible API.
- Updated Agent Framework imports to match the installed SDK API:
  - `ChatAgent`
  - `AzureOpenAIChatClient`
- Initially pinned `agent-framework==1.0.0b251120`, then replaced it with the smaller `agent-framework-core==1.0.0b251001` package for Azure Function deployment.
- Verified orchestrator tests: `29 passed`.

## 2026-06-21 - Azure Function App deployment

- Published the orchestrator API to Azure Function App `func-agentops-dev-002`.
- Applied live App Settings from local `.env` without printing secret values.
- Removed unsupported Flex Consumption app settings:
  - `FUNCTIONS_WORKER_RUNTIME`
  - `SCM_DO_BUILD_DURING_DEPLOYMENT`
  - `ENABLE_ORYX_BUILD`
- Enabled `AzureWebJobsFeatureFlags=EnableWorkerIndexing` for Python v2 function indexing.
- Fixed `function_app.py` so business imports happen inside handlers; this allowed the Function host to index routes even if a runtime dependency fails later.
- Added `apps/orchestrator-api/static/approval-console.html` so `/api/approval-console` is included in the deployed package.
- Added `.funcignore` for the Function App package.
- Built `.python_packages` for Linux from Windows using:
  - `uv pip install --python-platform x86_64-unknown-linux-gnu --target .python_packages/lib/site-packages ...`
- Installed the local `mcp-server` package into `.python_packages` so `enterprise_agentops_mcp` is available in Azure.
- Fixed Azure package dependency conflict by pinning:
  - `agent-framework-core==1.0.0b251001`
  - `fastmcp==3.4.2`
  - `mcp[cli]<2`
- Verified deployed functions are indexed:
  - `approval_console`
  - `approvals_pending`
  - `approvals_decision`
  - `webshop_order_support`
  - `customer_case_summarise`
  - `agent_runs`
- Verified public routes:
  - `GET /api/approval-console` -> `200`
  - `GET /api/approvals/pending?code=<function-key>` -> `200`, returned 40 pending approvals.
- Updated the Power Apps Custom Connector OpenAPI host to `func-agentops-dev-002.azurewebsites.net`.
- Re-verified:
  - OpenAPI JSON is valid.
  - Approval console focused tests: `3 passed`.

## 2026-06-20 - Stage 9 intake agent start

- Read `pc-transfer.txt`, `CLAUDE.md`, `context.MD`, `docs/09-agent-framework.md`, and the current `draft_agent.py` to resume from the other machine without restarting the project.
- Confirmed the next meaningful Stage 9 step is the Microsoft Agent Framework `IntakeAgent`, while keeping `DraftAgent` on the previous agent SDK as the historical comparison path.
- Installed `agent-framework` into the orchestrator API environment and verified the real Python package surface locally before implementing against it.
- Added `apps/orchestrator-api/src/agents/intake_agent.py` using Microsoft Agent Framework with Azure OpenAI routing and short step-by-step English comments.
- Added `apps/orchestrator-api/tests/test_intake_agent.py` to cover strict JSON parsing and basic input validation for the new intake agent.
- Verified the Linux orchestrator environment after the new agent work:
  - `python -m compileall src tests`: passed
  - orchestrator tests: `4 passed`
- Found that the installed Agent Framework 1.9.0 Python surface differs from the simplified docs examples:
  - used `agent_framework.Agent`
  - used `agent_framework.openai.OpenAIChatClient`
  - routed Azure OpenAI through `azure_endpoint` + `api_version`
- Reinstalled the missing `azure-servicebus` dependency in the orchestrator virtual environment after the Linux transfer so the existing webshop tests could import `service_bus_service` again.

## 2026-06-20 - Draft agent structured output for didactics

- Updated `apps/orchestrator-api/src/agents/draft_agent.py` so the the previous agent SDK comparison agent now requests a structured contract instead of free-form text.
- Added a simple didactic response contract with:
  - `summary`
  - `approvalRequired`
- Configured the the previous agent SDK Azure OpenAI execution settings to use `response_format=DraftSummaryContract` and `structured_json_response=True`.
- Added `apps/orchestrator-api/tests/test_draft_agent.py` to validate the contract parsing path independently of live model calls.
- Simplified the didactic contract again so it now contains only `summary` and `approvalRequired`.

## 2026-06-20 - Intake agent runtime fix

- Confirmed the local `.env` is being loaded correctly for Azure OpenAI.
- Ran a real `IntakeAgent` smoke test and found the first implementation was using the Agent Framework Responses-style client path, which failed against the current Azure OpenAI setup with `API version not supported`.
- Updated `apps/orchestrator-api/src/agents/intake_agent.py` to use `agent_framework.openai.OpenAIChatCompletionClient` instead of `OpenAIChatClient`.
- Re-ran the real `IntakeAgent` smoke test successfully; it returned a structured classification JSON for the delayed-order scenario.
- Re-ran orchestrator tests after the client swap: `5 passed`.

## 2026-06-21 - Intake agent structured contract alignment

- Updated `apps/orchestrator-api/src/agents/intake_agent.py` to use a Pydantic output contract for consistency with `DraftAgent`.
- Added `IntakeClassificationContract` and wired the Agent Framework call with `options={"response_format": IntakeClassificationContract}`.
- Replaced the manual required-key validation with a typed `_parse_contract(...)` validation path.
- Added a dedicated intake contract parsing test in `apps/orchestrator-api/tests/test_intake_agent.py`.

## 2026-06-21 - Coding agent best-practice guidance

- Confirmed the authoritative project spec file is now `context.md` on Linux; `context.MD` is no longer present in the working tree.
- Updated `CLAUDE.md`, `README.md`, and `docs/01-project-setup.md` to reference `context.md`.
- Added explicit guidance for future coding agents to prefer the correct project architecture over quick local shortcuts.
- Documented that MCP tool names must come from the MCP client/tool registry, not duplicated prompt literals.
- Documented that `toolsRequired` must use exact registered MCP tool names and should be validated against the registry.

## 2026-06-21 - Intake agent MCP tool registry enforcement

- Refactored `apps/orchestrator-api/src/shared/mcp_client.py` so the local MCP wrapper exposes registered tool names through `list_tool_names()`.
- Updated `apps/orchestrator-api/src/agents/intake_agent.py` to inject the registered MCP tool list into the intake prompt.
- Added validation so `toolsRequired` rejects hallucinated/non-registered tool names instead of passing them through.
- Added tests covering MCP tool-name listing and rejection of invented Intake tool names.
- Fixed the intake prompt builder so JSON braces in the schema example are escaped correctly when injecting registered MCP tool names.

## 2026-06-21 - Intake wired into webshop orchestrator

- Added the `IntakeAgent` as the first step in `apps/orchestrator-api/src/webshop_order_support.py`.
- The order-support handler now accepts a natural-language `message`, `userMessage`, or `prompt`, and can use `contactEmail` extracted by Intake when `customerEmail` is not provided directly.
- The orchestrator now logs the Intake-derived `intent` instead of the previous fixed intent string.
- Added Intake diagnostics to the response and Service Bus event payload through `intake` / `intakeToolsRequired`.
- Updated actual `tools_called` telemetry so `create_approval_request` is included only when an approval is created.
- Recreated the ignored local Azure Functions `apps/orchestrator-api/local.settings.json` on the Linux machine so `func start` can detect the Python worker runtime.
- Removed `MCP_DATA_MODE` from `apps/orchestrator-api/local.settings.json` because it was overriding the root `.env`; verified the effective runtime config now reads `DATA_MODE=dataverse` and `KNOWLEDGE_MODE=search`.
- Reduced `apps/orchestrator-api/local.settings.json` to Azure Functions host-only settings (`FUNCTIONS_WORKER_RUNTIME`, `AzureWebJobsStorage`) so application/runtime settings come only from the root `.env`.

## 2026-06-21 - Shared Azure OpenAI agent runtime

- Added `apps/orchestrator-api/src/shared/agent_runtime.py` with `AzureOpenAIAgentRuntime`.
- Centralized Azure OpenAI config validation and client/kernel construction for Microsoft Agent Framework and the previous agent SDK.
- Updated `IntakeAgent` to build its Agent Framework client through the shared runtime.
- Updated `DraftAgent` to build its the previous agent SDK kernel/settings through the shared runtime while keeping it as the only previous SDK comparison agent.
- Added focused runtime tests for missing configuration and the previous agent SDK settings construction.

## 2026-06-21 - Data agent extraction

- Added `apps/orchestrator-api/src/agents/data_agent.py` as a deterministic MCP-backed agent for order-support data retrieval.
- Moved customer, latest order, items, shipment, returns, and refunds retrieval out of `webshop_order_support.py`.
- Updated the orchestrator to consume the shaped `DataAgent` payload and reuse `toolsCalled` for telemetry.
- Added focused `DataAgent` tests for successful sequencing and missing-customer early exit.

## 2026-06-21 - Knowledge agent extraction

- Added `apps/orchestrator-api/src/agents/knowledge_agent.py` as a deterministic MCP-backed policy retrieval agent.
- Moved direct `search_knowledge_articles` orchestration out of `webshop_order_support.py`.
- The new `KnowledgeAgent` builds the policy search query from shipment, refund, return, risk, and intake context.
- Added focused `KnowledgeAgent` tests for contextual query construction and MCP tool usage.

## 2026-06-21 - Governance agent extraction

- Added `apps/orchestrator-api/src/agents/governance_agent.py` with deterministic order-support risk and approval rules.
- Moved delay/refund approval decision logic out of `webshop_order_support.py`.
- The orchestrator now consumes a shaped governance decision for risk, approval type, approval reason, and approval trigger.
- Added governance metadata to the endpoint response and agent-run event payload.
- Added focused `GovernanceAgent` tests for high, medium, and low risk paths.

## 2026-06-21 - Critic agent extraction

- Added `apps/orchestrator-api/src/agents/critic_agent.py` as a deterministic MCP-backed evaluator for generated summaries.
- Moved direct `evaluate_response` calls out of `webshop_order_support.py`.
- The new `CriticAgent` builds required source references and preserves `toolsCalled` metadata for telemetry.
- Added focused `CriticAgent` tests for evaluation input shaping and missing-source handling.

## 2026-06-21 - Cost agent extraction

- Added `apps/orchestrator-api/src/agents/cost_agent.py` as a deterministic MCP-backed cost calculation agent.
- Moved direct `calculate_agent_run_cost` calls out of `webshop_order_support.py`.
- The new `CostAgent` preserves `toolsCalled` metadata for telemetry.
- Added a focused `CostAgent` test for MCP pricing-tool delegation.

## 2026-06-21 - Direction expansion: HITL, thread state, type safety

- Adopted human-in-the-loop, thread-based state management, stronger type safety, and a richer domain/workflow model as explicit project direction.
- Added typed workflow models in `apps/orchestrator-api/src/agents/models.py`: `GovernanceDecision`, `ApprovalOutcome`, and `ThreadState`.
- Added local MVP thread persistence in `apps/orchestrator-api/src/shared/thread_state_store.py`.
- Added `apps/orchestrator-api/src/agents/workflow_agent.py` to coordinate approval creation, approval events, run logging, run events, and thread-state updates.
- Updated `webshop_order_support.py` to accept/reuse `threadId`, return thread and approval state, and delegate workflow side effects to `WorkflowAgent`.
- Updated docs to document human-in-the-loop, thread state, typed contracts and AutoGen positioning.
- Created `changeOfDirection.md` at the repository root to explain what changed, why it changed, and the reasoning behind the decisions.

## 2026-06-21 - Thread state storage direction: Azure Table Storage

- Confirmed Cosmos DB is not currently part of the project docs, Pulumi infrastructure, or deployed local configuration.
- Chose Azure Table Storage as the production-shaped runtime store for thread state, using Dataverse for business/audit records and Blob Storage only for larger snapshots if needed.
- Updated `ThreadStateStore` to support explicit `THREAD_STATE_STORE=file|table` modes.
- Added Azure Table Storage dependencies to `apps/orchestrator-api/requirements.txt`.
- Updated Pulumi to create a `threadStateTable`, configure the Function App for `THREAD_STATE_STORE=table`, and assign the Function managed identity the `Storage Table Data Contributor` role.
- Updated docs and `changeOfDirection.md` to remove Cosmos DB as the near-term direction for thread state.

## 2026-06-21 - Thread state import cycle fix

- Found a circular import when using `ThreadStateStore` directly: importing `src.agents.models` executed `src/agents/__init__.py`, which imported `WorkflowAgent`, which imported `ThreadStateStore`.
- Removed eager agent imports from `apps/orchestrator-api/src/agents/__init__.py`; agents should be imported from their concrete modules.
- Re-ran the direct `ThreadStateStore(mode="file")` smoke test successfully.
- Re-ran orchestrator tests successfully: `26 passed`.

## 2026-06-21 - Power Apps approval console direction

- Decided to use a browser-based Power Apps Approval Console as the primary human-in-the-loop approval surface.
- Added MCP approval tools to list pending approval requests and approve/reject them.
- Added Orchestrator API endpoints:
  - `GET /api/approvals/pending`
  - `POST /api/approvals/decision`
- Extended approval records with Power Apps-friendly fields: thread ID, customer name/email, order number, decision comment and decision timestamp.
- Updated Dataverse schema v1 so `cr_approvalrequest` includes the new approval console fields.
- Added `docs/11-power-apps-approval-console.md` with the target flow, API contract and Canvas App design.
- Isolated mock JSON data in test fixtures so approval and run tests no longer mutate versioned data files.
- Verified MCP tests with `uv run pytest tests -q` -> `35 passed`.
- Verified Orchestrator tests with `.venv/bin/python -m pytest tests -q` -> `29 passed`.

## 2026-06-21 - Documentation alignment for Power Apps HITL

- Audited docs for stale Power Automate/Teams-first human approval language after adopting the Power Apps Approval Console direction.
- Updated `README.md`, `CLAUDE.md`, `context.md`, `docs/08-secure-rag.md`, and `docs/10-observability-polish.md` so the primary HITL UX is Power Apps, with Power Automate kept as optional integration/notification.
- Updated demo/interview wording so the approval walkthrough now shows Power Apps listing pending Dataverse approval requests and calling the Orchestrator decision endpoint.
- Removed the obsolete `POST /api/agents/approval/create` contract from current API docs and updated examples to include thread/approval state.

## 2026-06-21 - Power Platform script env path fix

- Fixed Power Platform Dataverse scripts so they read `.env` from the repository root by default.
- Kept `mcp-server/.env` as a legacy fallback and documented `-EnvPath` as an override.
- Updated `docs/06-dataverse-setup.md` with Linux `pwsh` commands.
- Verified `pwsh -File ./power-platform/scripts/Deploy-AgentOpsDataverseSchema.ps1 -WhatIf` succeeds on Linux and detects the 6 pending approval-console columns on `cr_approvalrequest`.
- Confirmed after real schema deploy that `cr_threadid`, `cr_customername`, `cr_customeremail`, `cr_ordernumber`, `cr_decisioncomment`, and `cr_decidedon` now exist on `cr_approvalrequest`.

## 2026-06-21 - Approval decision endpoint smoke test

- Confirmed local Function app `GET /api/approvals/pending` returns Dataverse approval requests with thread, customer and order fields.
- Approved `apr-87c90251` through `POST /api/approvals/decision`.
- Verified the approval returned `status=Approved`, `threadStatus=Completed`, and `threadCurrentStep=human_approval_approved`.
- Verified the approved request no longer appears in `GET /api/approvals/pending`.
- Verified local thread state for `thread-ef1cb85c` contains the approval decision metadata.

## 2026-06-21 - Local HTML approval console

- Added `apps/frontend-demo/approval-console.html` as a browser-based learning console over the same approval endpoints planned for Power Apps.
- Added `GET /api/approval-console` to serve the HTML through Azure Functions so browser calls remain same-origin.
- Verified `http://localhost:7071/api/approval-console` returns `200`.
- Verified the HTML references `/api/approvals/pending` and `/api/approvals/decision`.
- Verified focused approval-console tests still pass: `3 passed`.

## 2026-06-21 - Power Apps connector assets

- Added `power-platform/custom-connectors/agentops-approval-console.openapi.json` for the Power Apps custom connector.
- Added `power-platform/custom-connectors/README.md` with import/host/key notes.
- Added `power-platform/power-apps/approval-console-formulas.md` with Canvas App formulas for gallery, detail, approve and reject actions.
- Verified the OpenAPI JSON parses and exposes `/approvals/pending` and `/approvals/decision`.

## 2026-06-21T20:14:32+01:00 - Handover to other PC

Session objective:

- Continue the project on this Linux PC after transfer from the other machine.
- Move Human-in-the-Loop from a JSON-only concept toward a real approval surface.
- Keep final frontend direction as Power Apps, while using local HTML only as a learning/smoke-test surface.

Major decisions:

- Final approver UX is Power Apps Canvas App, not the local HTML page.
- Power Apps will use a Custom Connector over the Orchestrator API.
- Dataverse stores approval business/audit records in `cr_approvalrequest`.
- Azure Table Storage remains the production-shaped technical thread-state store.
- Local HTML console exists only to feel/test the flow before building the Power Apps canvas app.
- `.env` at repository root is the canonical local env file. `mcp-server/.env` is legacy fallback only.

Implemented in this session:

- Added approval decision/list capabilities to MCP:
  - `list_pending_approval_requests`
  - `decide_approval_request`
- Extended Dataverse approval record support with:
  - `cr_threadid`
  - `cr_customername`
  - `cr_customeremail`
  - `cr_ordernumber`
  - `cr_decisioncomment`
  - `cr_decidedon`
- Added Orchestrator approval endpoints:
  - `GET /api/approvals/pending`
  - `POST /api/approvals/decision`
- Added local browser smoke-test console:
  - `apps/frontend-demo/approval-console.html`
  - served from `GET /api/approval-console`
- Added Power Apps Custom Connector assets:
  - `power-platform/custom-connectors/agentops-approval-console.openapi.json`
  - `power-platform/custom-connectors/README.md`
  - `power-platform/power-apps/approval-console-formulas.md`
- Updated Power Platform scripts so `Deploy-AgentOpsDataverseSchema.ps1`, `Seed-AgentOpsDataverseData.ps1`, and `Clear-AgentOpsDataverseSeed.ps1` read root `.env` by default.
- Updated MCP config loading so `mcp-server/src/enterprise_agentops_mcp/config.py` loads root `.env` first, then `mcp-server/.env` fallback.
- Updated docs to make Power Apps the primary HITL direction and Power Automate optional:
  - `README.md`
  - `CLAUDE.md`
  - `context.md`
  - `changeOfDirection.md`
  - `docs/01-project-setup.md`
  - `docs/04-orchestrator-api.md`
  - `docs/06-dataverse-setup.md`
  - `docs/08-secure-rag.md`
  - `docs/10-observability-polish.md`
  - `docs/11-power-apps-approval-console.md`
  - `docs/agents.md`

Environment/setup fixed on this Linux PC:

- Installed PowerShell 7.6.2.
- Fixed Microsoft package repo usage enough to install/run `pwsh`.
- Dataverse schema deploy now works from Linux using:

```bash
pwsh -File ./power-platform/scripts/Deploy-AgentOpsDataverseSchema.ps1
```

Verified during this session:

- `pwsh -File ./power-platform/scripts/Deploy-AgentOpsDataverseSchema.ps1 -WhatIf`
  - confirmed the approval-console columns exist after real deploy.
- `GET /api/approvals/pending`
  - returned Dataverse approval records with thread/customer/order fields.
- `POST /api/approvals/decision`
  - approved `apr-87c90251`.
  - response included `threadStatus=Completed` and `threadCurrentStep=human_approval_approved`.
  - approval disappeared from pending list.
  - local thread state for `thread-ef1cb85c` recorded approval metadata.
- `GET /api/approval-console`
  - returned `200` and served the local HTML console.
- OpenAPI validation:

```bash
python3 -m json.tool power-platform/custom-connectors/agentops-approval-console.openapi.json >/tmp/agentops-openapi.json
```

- Focused tests:

```bash
cd mcp-server
uv run pytest tests/test_config.py tests/test_approvals.py -q
# 8 passed

cd apps/orchestrator-api
.venv/bin/python -m pytest tests/test_approval_console.py tests/test_webshop_order_support.py -q
# 6 passed

cd apps/orchestrator-api
.venv/bin/python -m pytest tests/test_approval_console.py -q
# 3 passed
```

- General hygiene:

```bash
git diff --check
# ok
```

Important runtime state:

- A local Function process was already listening on `localhost:7071` during tests.
- The local HTML console can be opened at:

```text
http://localhost:7071/api/approval-console
```

- The Power Apps Custom Connector cannot use `localhost`; it needs a public Function App host or a tunnel.

Next steps for the other PC:

1. Pull/receive this repo state, including uncommitted/new files.
2. Review `git status --short`; many files are intentionally changed/untracked from the larger direction shift.
3. Run full verification:

```bash
cd mcp-server
uv run pytest tests -q

cd ../apps/orchestrator-api
.venv/bin/python -m pytest tests -q
```

4. Decide deploy path for public Orchestrator URL:
   - If Pulumi local state exists on the other PC, use that state.
   - If not, either transfer Pulumi state or deploy/publish the Function pragmatically with Azure Functions Core Tools.
5. Once a public Function host exists, update `power-platform/custom-connectors/agentops-approval-console.openapi.json`:

```text
REPLACE_WITH_FUNCTION_HOST
```

6. Import the OpenAPI file as a Power Apps Custom Connector.
7. Create Canvas App `AgentOps Approval Console` using formulas from:

```text
power-platform/power-apps/approval-console-formulas.md
```

8. Use the app to list approvals, approve/reject, and confirm Dataverse + thread state change.

Known caveats:

- `az functionapp list` should be used on the other PC to see whether a Function App already exists.
- User does not use Pulumi Cloud. If Pulumi is needed, use `pulumi login --local`, but beware local state mismatch between PCs.
- Power Apps cloud connector will not call the Linux machine's `localhost`.
- Some older Dataverse approval rows do not have thread/customer/order fields because they were created before the schema/contract expansion. New rows include them.

## 2026-06-21T21:58:22+01:00 - Windows continuation: public Function and connector readiness

Validated after returning to the Windows PC:

- `power-platform/custom-connectors/agentops-approval-console.openapi.json` is valid JSON.
- The connector OpenAPI host is already set to `func-agentops-dev-002.azurewebsites.net`.
- `GET https://func-agentops-dev-002.azurewebsites.net/api/approval-console` returned `200`.
- `GET https://func-agentops-dev-002.azurewebsites.net/api/approvals/pending` without a Function key returned `401`, confirming the Custom Connector must provide the `code` query key.

Documentation update:

- Updated `power-platform/custom-connectors/README.md` so it no longer says the OpenAPI file still contains the placeholder host.

Next practical step:

- Import the OpenAPI file as a Power Apps Custom Connector.
- Create a connection using an Azure Functions host/function key as the `code` query parameter.
- Test `ListPendingApprovals` from the connector before building the Canvas App.

## 2026-06-21T22:33:08+01:00 - Dataverse solution created for project assets

Decision:

- Stop leaving project Dataverse customizations only in the Default Solution.
- Use a dedicated unmanaged solution for the workshop/case assets.

Created and verified:

- Publisher friendly name: `AgentOps Workshop Publisher`
- Publisher unique name: `agentops_workshop_publisher`
- Solution friendly name: `AgentOps Workshop`
- Solution unique name: `agentops_workshop`
- Verified with `pac solution list`.

Implemented:

- Added `power-platform/scripts/Ensure-AgentOpsDataverseSolution.ps1`.
- The script creates the Publisher/Solution if missing.
- The script adds the custom tables to the solution:
  - `cr_order`
  - `cr_orderitem`
  - `cr_shipment`
  - `cr_returnrequest`
  - `cr_refund`
  - `cr_approvalrequest`
  - `cr_agentrun`

Verification:

- Ran `pwsh -File ./power-platform/scripts/Ensure-AgentOpsDataverseSolution.ps1`.
- Ran `pwsh -File ./power-platform/scripts/Deploy-AgentOpsDataverseSchema.ps1 -SolutionUniqueName agentops_workshop`.
- Schema deploy completed with all existing tables/columns recognized.

Documentation:

- Updated `docs/06-dataverse-setup.md`.
- Updated `power-platform/dataverse-schema/README.md`.

## 2026-06-21T23:59:07+01:00 - Copilot Studio path selected

Decision:

- Use the current Power Platform Custom Connector as the first Copilot Studio tool path.
- In the new Copilot Studio experience, this means adding the connector under the agent's `Tools` area.
- The current connector exposes approval console operations:
  - `ListPendingApprovals`
  - `SubmitApprovalDecision`

Reason:

- This proves the Power Platform connector/tool integration before adding a separate customer order support endpoint.
- A second connector/tool can be added later for `POST /api/webshop/order-support`.

Current Power Apps status:

- Canvas App can call the connector.
- Pending approval records render in a gallery.
- Item selection and detail labels work.
- Approve/Reject buttons are still pending and can be resumed later.

## 2026-06-22T00:18:13+01:00 - Function App thread-state fix and clean approval generated

Problem found:

- Calling `POST /api/agents/webshop/order-support` failed in Azure Functions.
- First exception: `TableClient` did not have `create_table_if_not_exists`.
- After switching to `TableServiceClient`, Azure returned `AuthorizationPermissionMismatch` when the Function tried to create the table at runtime.

Decision:

- Runtime code should not provision Azure Table Storage during a request.
- The table is an infrastructure resource and belongs in Pulumi/infra provisioning.

Fix:

- Updated `apps/orchestrator-api/src/shared/thread_state_store.py`.
- Removed runtime table creation from `ThreadStateStore`.
- Runtime now assumes the table already exists and only performs entity reads/writes.
- Verified Pulumi already declares:
  - `threadStateTable`
  - `Storage Table Data Contributor` role assignment for the Function App identity.

Operational repair:

- Created the existing environment table explicitly:

```powershell
az storage table create --name AgentThreadState --account-name stagentopsdeveus002 --auth-mode login
```

Validation:

- Ran focused test:

```powershell
cd apps/orchestrator-api
.\.venv\Scripts\python.exe -m pytest tests\test_thread_state_store.py -q
# 2 passed
```

- Rebuilt Linux-target packages.
- Republished `func-agentops-dev-002`.
- Retried `POST /api/agents/webshop/order-support`.
- It succeeded and generated:
  - `runId`: `run-867bccc3`
  - `threadId`: `thread-73c56a7e`
  - `approvalId`: `apr-4874e82a`
  - `customerName`: `John Smith`
  - `orderNumber`: `WEB-1001`
  - `approvalStatus`: `Pending`

Next:

- Ask Copilot Studio again to list pending approvals.
- It should now include the clean approval with customer/order/thread context.

## 2026-06-22T00:30:35+01:00 - Copilot Studio approval tools documented

Validated Copilot Studio flow:

- `ListPendingApprovals` tool works.
- `SubmitApprovalDecision` tool works.
- Clean approval was approved through the agent.
- Follow-up approval listing returned no pending approvals.

Documentation updated:

- Added `docs/12-copilot-studio.md` with the validated approval tools and test prompts.
- Linked `docs/12-copilot-studio.md` from `README.md`.

Deferred:

- Azure AI Search as Copilot Studio Knowledge is paused for now.
- A future search/knowledge path can be revisited after the approval workflow and agent surface are stable.

## 2026-06-22T20:21:25+01:00 - Microsoft Purview added to roadmap

Decision:

- Add Microsoft Purview as a post-core-workflow governance/compliance phase.
- Do not implement it before the Power Apps approval console and observability dashboard are stable.

Documentation updated:

- Added `docs/13-purview-governance.md`.
- Linked it from `README.md`.
- Added Purview as a post-core governance phase in `docs/10-observability-polish.md`.
- Added Purview to the next steps in `docs/12-copilot-studio.md`.

Purview scope:

- data discovery and catalog
- sensitive data classification
- Dataverse approval/customer data governance
- Power Platform connector DLP considerations
- audit/compliance evidence
- AI governance narrative for the final demo

## 2026-06-22T21:00:04+01:00 - Power Apps approval button formulas corrected

Updated the Canvas App formula documentation after validating the real Power Apps custom connector signature.

Finding:

- The OpenAPI operation uses a JSON body, but Power Apps exposes `SubmitApprovalDecision` as required parameters plus an optional record:

```powerfx
SubmitApprovalDecision(approvalId, decision, approvedBy, {comment: commentText})
```

Documentation updated:

- `power-platform/power-apps/approval-console-formulas.md`
- `docs/11-power-apps-approval-console.md`

Current Power Apps status:

- Gallery can list pending approvals.
- Detail labels can show selected approval fields.
- Approve/Reject formulas now use the signature proven in Canvas Studio.
- After a decision, the app refreshes pending approvals, clears the comment and clears the selected approval.

## 2026-06-22T21:06:21+01:00 - Power BI Desktop selected for observability reports

Decision:

- Use local Power BI Desktop for the observability and cost engineering report.
- Do not require Power BI Service publishing for the workshop flow.
- Publishing/sharing can be added later if a Power BI Pro, Premium Per User, or Fabric/Premium capacity is available.

Documentation updated:

- Added `dashboards/powerbi/README.md`.
- Updated `docs/10-observability-polish.md` to make Power BI Desktop the primary reporting path.
- Updated `README.md` with the dashboard folder and Stage 10 link.

Report scope:

- Operations page: total runs, latency, approvals, workflow distribution.
- Cost Engineering page: total cost, cost by model/vendor/workflow, high-cost runs.
- Governance page: risk, quality, groundedness and approval pressure.

Preferred data source:

- Dataverse table `cr_agentrun`.

Offline fallback:

- `mcp-server/src/enterprise_agentops_mcp/data/agent_runs.json`.

## 2026-06-22T21:08:41+01:00 - Power BI Desktop prerequisite documented

Updated setup/reporting documentation to explicitly include Power BI Desktop installation.

Documentation updated:

- `docs/00-setup.md`
- `dashboards/powerbi/README.md`

Install command:

```powershell
winget install Microsoft.PowerBI
```

## 2026-06-22T21:40:24+01:00 - Power BI Operations page started

Power BI Desktop work completed:

- Installed/opened Power BI Desktop.
- Connected Power BI Desktop to Dataverse.
- Loaded the `cr_agentrun` table.
- Created the first report page: `Operations`.
- Added initial visuals:
  - Total Runs card
  - Estimated Cost card
  - Average Latency card
  - Runs by Workflow donut chart
  - Agent runs table

Notes:

- Current dataset has only 2 agent runs, so visual distribution is limited.
- Estimated cost appears as `0.00` unless decimal formatting is increased, because the values are very small.

Remaining report work:

- Save the report as `dashboards/powerbi/agentops-observability.pbix`.
- Generate more agent runs for a better demo dataset.
- Complete `Cost Engineering` page.
- Complete `Governance` page.
- Document the final walkthrough across Copilot Studio, Orchestrator, MCP, Dataverse, Power Apps and Power BI.

## 2026-06-22T22:05:00+01:00 - Stage 10 scope aligned and telemetry implemented

Decision:

- Keep Stage 10 focused on the planned deliverable, not perfection.
- Remove `25 seeded agent runs` as a milestone.
- Treat one working Power BI Operations page as sufficient for the core case.
- Keep Cost Engineering and Governance Power BI pages as optional extensions.
- Keep Microsoft Purview as a separate future phase.
- Treat the final walkthrough as a demo script/document, not a runtime feature.

Implemented:

- Added `mcp-server/src/enterprise_agentops_mcp/services/telemetry.py`.
- Wired `log_agent_run` to create an Application Insights/OpenTelemetry span named `mcp.log_agent_run`.
- Captured workflow, intent, model, vendor, token counts, latency, tool list, approval flag, risk, quality, groundedness, run id and estimated cost as span attributes.
- Enabled `azure-monitor-opentelemetry-exporter>=1.0.0b53` in `apps/orchestrator-api/requirements.txt` so the Azure Function deployment has the telemetry dependency.

Documentation updated:

- `docs/10-observability-polish.md`
- `dashboards/powerbi/README.md`

Verification:

```powershell
cd mcp-server
uv run pytest tests/test_observability.py tests/test_dataverse_mode.py -q
# 4 passed
```

Implementation note:

- The first attempt used the higher-level `azure-monitor-opentelemetry` package.
- The Orchestrator venv exposed an import failure around `opentelemetry.sdk._logs.LogData`.
- The implementation was corrected to use `azure-monitor-opentelemetry-exporter>=1.0.0b53` directly with `opentelemetry-sdk`.
- Focused Orchestrator verification now passes:

```powershell
cd apps/orchestrator-api
.\.venv\Scripts\python.exe -m pytest tests\test_webshop_order_support.py tests\test_approval_console.py -q
# 6 passed
```

## 2026-06-22T22:18:00+01:00 - Telemetry tested in Azure Application Insights

Problem found during Azure test:

- A normal `func azure functionapp publish ... --python` remote build did not include the local `enterprise_agentops_mcp` package.
- The Azure Function failed with `ModuleNotFoundError: No module named 'enterprise_agentops_mcp'`.

Deployment fix:

- Rebuilt local Linux-compatible `.python_packages` for the Function App and included the local MCP package:

```powershell
cd apps/orchestrator-api
uv pip install --python-platform x86_64-unknown-linux-gnu --python-version 3.12 --target .python_packages/lib/site-packages -r requirements.txt ..\..\mcp-server
func azure functionapp publish func-agentops-dev-002 --no-build
```

Telemetry reliability fix:

- Switched the telemetry provider from batch sending to `SimpleSpanProcessor`.
- Added explicit `force_flush()` after `log_agent_run`.
- This makes the Application Insights span visible immediately enough for serverless request testing.

Azure validation:

- Called the public Azure Function endpoint:

```text
POST /api/agents/webshop/order-support
```

- The endpoint succeeded and produced:
  - `runId`: `run-5de611ba`
  - `threadId`: `thread-ebecf698`
  - `approvalId`: `apr-1f116a6e`
  - `approvalStatus`: `Pending`
  - `modelUsed`: `gpt-5-mini`

- Queried Application Insights and confirmed a telemetry row:
  - `itemType`: `dependency`
  - `name`: `mcp.log_agent_run`
  - `agentops.run_id`: `run-5de611ba`
  - attributes included workflow, intent, model, vendor, token counts, latency, approval flag, risk, quality, groundedness, tools called and estimated cost.
