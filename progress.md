# Project Progress

Registro curto do que foi feito, decidido e verificado durante o projeto.

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
- Installed Semantic Kernel in the orchestrator API virtual environment:
  - package: `semantic-kernel[azure]`
  - installed version observed locally: `semantic-kernel 1.36.0`
- Added the first Semantic Kernel agent:
  - `apps/orchestrator-api/src/agents/draft_agent.py`
  - class: `DraftAgent`
  - service: `AzureChatCompletion`
  - deployment: `gpt-5-mini`
  - API version: `2024-10-21`
  - settings: `max_completion_tokens=1600`, `reasoning_effort=low`
- Updated `apps/orchestrator-api/src/shared/azure_openai_client.py` so the existing orchestrator path now delegates summary generation to `DraftAgent`.
- Inspected Semantic Kernel `FunctionResult` and confirmed token usage/model are available through `result.get_inner_content()`.
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
- Documented that only the Draft Agent remains on Semantic Kernel, intentionally, for comparison, didactics and legacy understanding.
- Removed Claude/Anthropic from active agent definitions; Anthropic remains only as an optional legacy reference.
- Corrected Pulumi documentation to C# and kept Azure OpenAI + Gemini as the active comparison path.

## 2026-06-20 - Agent code commenting rule

- Updated agent instruction docs to require short step-by-step English comments in agent/orchestration code.
- Added educational step comments to `apps/orchestrator-api/src/agents/draft_agent.py`.
- Verified `draft_agent.py` syntax with `python -m py_compile`.

## 2026-06-20 - PC transfer handoff

- Created `pc-transfer.txt` at the repository root for continuing the project on another Linux machine.
- Included current architecture decisions, implemented components, required local env vars, Linux setup commands, smoke tests, and the recommended next prompt for the next Codex.

## 2026-06-20 - Stage 9 intake agent start

- Read `pc-transfer.txt`, `CLAUDE.md`, `context.MD`, `docs/09-agent-framework.md`, and the current `draft_agent.py` to resume from the other machine without restarting the project.
- Confirmed the next meaningful Stage 9 step is the Microsoft Agent Framework `IntakeAgent`, while keeping `DraftAgent` on Semantic Kernel as the comparison track.
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

- Updated `apps/orchestrator-api/src/agents/draft_agent.py` so the Semantic Kernel comparison agent now requests a structured contract instead of free-form text.
- Added a simple didactic response contract with:
  - `summary`
  - `approvalRequired`
- Configured the Semantic Kernel Azure OpenAI execution settings to use `response_format=DraftSummaryContract` and `structured_json_response=True`.
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
- Centralized Azure OpenAI config validation and client/kernel construction for Microsoft Agent Framework and Semantic Kernel.
- Updated `IntakeAgent` to build its Agent Framework client through the shared runtime.
- Updated `DraftAgent` to build its Semantic Kernel kernel/settings through the shared runtime while keeping it as the only SK comparison agent.
- Added focused runtime tests for missing configuration and Semantic Kernel settings construction.

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
