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
