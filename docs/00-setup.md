# Stage 0: Environment Setup

Everything you need to install before starting development on the Enterprise AgentOps Control Tower.

---

## Overview

| Category | Tool | Required |
|---|---|---|
| Runtime | Python 3.12 | Yes |
| Runtime | Node.js 24.x | Yes |
| Runtime | .NET SDK 8 | Yes |
| Package manager | uv | Yes |
| Azure | Azure CLI | Yes |
| Azure | Azure Functions Core Tools v4 | Yes |
| Azure | Azure Developer CLI (azd) | Recommended |
| IaC | Pulumi CLI | Yes |
| Power Platform | Power Platform CLI (pac) | Yes |
| Editor | VS Code | Yes |
| Storage emulator | Azurite | Yes |
| Containers | Docker Desktop | Recommended |
| AI | Anthropic SDK | Yes |
| AI | OpenAI SDK + Codex CLI | Yes |
| Cloud | Azure subscription | Yes |
| Cloud | M365 Developer Tenant | Yes |
| Cloud | Copilot Studio trial | Yes |
| Cloud | Azure AI Foundry | Recommended |

---

## Installation Order

Follow this sequence. Tools within each group can be installed in parallel, but respect the order between groups.

---

## Group 1 — Runtimes and Package Managers

Install these first. Everything else depends on them.

### Python 3.12

Use Python 3.12 for this project. On Windows, `python` can still point to another installed version, so verify with `py -3.12`.

```powershell
winget install Python.Python.3.12
```

Verify:
```bash
py -3.12 --version   # 3.12.x
```

### Node.js 24.x

Current project baseline: Node.js 24.x. This is supported by Azure Functions Node.js programming model v4 on Functions runtime 4.25+.

```powershell
winget install OpenJS.NodeJS
```

Verify:
```bash
node --version   # v24.x
npm --version
```

### .NET SDK 8

```powershell
winget install Microsoft.DotNet.SDK.8
```

Verify:
```bash
dotnet --version   # 8.0.x
```

### uv (Python package manager — replaces pip)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:
```bash
uv --version
```

---

## Group 2 — Git and Editor

### Git

```powershell
winget install Git.Git
```

Verify:
```bash
git --version
```

### VS Code

```powershell
winget install Microsoft.VisualStudioCode
```

**Required extensions:**

```
ms-python.python
ms-python.pylance
ms-azuretools.vscode-azurefunctions
ms-azuretools.vscode-azureresourcegroups
ms-vscode.powershell
humao.rest-client
pulumi.pulumi-lsp-client
```

**Recommended extensions:**

```
ms-azuretools.azure-dev
github.copilot
ms-azuretools.vscode-bicep
ms-powerplatform.vscode-powerplatform
ms-CopilotStudio.vscode-copilotstudio
```

> `ms-powerplatform.vscode-powerplatform` — Power Platform Tools, includes Microsoft Copilot Studio authoring support directly in VS Code.
>
> `ms-CopilotStudio.vscode-copilotstudio` — dedicated Microsoft Copilot Studio extension for cloning, editing, diffing and updating Copilot Studio agents directly from VS Code.

---

## Group 3 — Azure CLI and Tools

### Azure CLI

```powershell
winget install Microsoft.AzureCLI
```

Verify and login:
```bash
az --version
az login
```

### Azure Functions Core Tools v4 (required)

```bash
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

Verify:
```bash
func --version   # 4.x
```

### Azure Developer CLI — azd (recommended)

```powershell
winget install Microsoft.Azd
```

Verify:
```bash
azd version
```

> If `azd` is not found right after install on Windows, open a fresh terminal and try again.

---

## Group 4 — Pulumi

Pulumi is the primary IaC tool for this project. All Azure resources are created via Pulumi.

### Pulumi CLI

```powershell
winget install Pulumi.Pulumi
```

Or via script:
```powershell
(Invoke-WebRequest -Uri https://get.pulumi.com/install.ps1 -UseBasicParsing).Content | powershell -Command -
```

Verify:
```bash
pulumi version
```

> If `pulumi` is not found right after install on Windows, open a fresh terminal and try again.

### Pulumi Login (local state — free)

```bash
# Store state locally (no Pulumi Cloud account needed)
pulumi login --local

# Or with Pulumi Cloud account (recommended for team use)
pulumi login
```

### Install Pulumi Azure Provider

```bash
# Inside infrastructure/pulumi/
npm install @pulumi/azure-native @pulumi/pulumi
```

---

## Group 5 — Power Platform CLI

### pac CLI

```powershell
$msi = Join-Path $env:TEMP 'powerapps-cli-1.0.msi'
Invoke-WebRequest -Uri 'https://aka.ms/PowerAppsCLI' -OutFile $msi
Start-Process msiexec.exe -ArgumentList @('/i', $msi, '/qn', '/norestart') -Wait
```

Verify:
```bash
pac
```

> The current official Windows install path is the MSI linked from Microsoft Learn. If `pac` is not found right after install, open a fresh terminal and try again.

Authenticate (after creating the Developer Environment):
```bash
pac auth create --url https://yourorg.crm.dynamics.com
```

> Use `pac auth create` for admin and maker tasks only. Backend code should use a Service Principal for Dataverse access.

---

## Group 6 — Local Emulators

### Azurite (Azure Storage emulator — required for local Azure Functions)

```bash
npm install -g azurite
```

**Start in a separate terminal before using Azure Functions:**
```bash
azurite --silent --location C:\azurite --debug C:\azurite\debug.log
```

### Docker Desktop (recommended)

Download: https://www.docker.com/products/docker-desktop

Alternative — run Azurite via Docker:
```bash
docker run -p 10000:10000 -p 10001:10001 -p 10002:10002 mcr.microsoft.com/azure-storage/azurite
```

---

## Group 7 — AI SDKs and Codex CLI

### Anthropic SDK (Python)

Installed automatically via `uv sync` in the MCP Server project.
To install globally:
```bash
pip install anthropic
```

See full guide: [docs/ai-anthropic.md](ai-anthropic.md)

### OpenAI SDK (Python)

```bash
pip install openai
```

### OpenAI Codex CLI (required for code generation)

```bash
npm install -g @openai/codex
```

Verify:
```bash
codex --version
```

Set API key:
```powershell
# PowerShell (session)
$env:OPENAI_API_KEY="sk-..."

# Or add to PowerShell profile (persistent)
Add-Content $PROFILE '$env:OPENAI_API_KEY="sk-..."'
```

See full guide: [docs/ai-codex.md](ai-codex.md)

---

## Group 8 — Cloud Accounts (configuration, not installation)

### Azure Subscription

1. Create a free account at https://azure.microsoft.com/free — $200 credit
2. Or use an existing subscription.
3. Create the resource group:

```bash
az group create --name rg-agentops-dev --location uksouth
```

### Microsoft 365 Developer Tenant (required for Copilot Studio + Dataverse)

1. Join M365 Developer Program: https://developer.microsoft.com/en-us/microsoft-365/dev-program
2. Create an Instant Sandbox — includes 25 M365 licences, Teams, SharePoint, Dataverse, Power Platform.
3. Note the tenant ID and Dataverse URL: `https://yourorg.crm.dynamics.com`

### Copilot Studio Trial

1. Go to https://copilotstudio.microsoft.com
2. Sign in with your M365 Developer account.
3. Start the trial.

### Azure AI Foundry (recommended from Day 9)

1. Go to https://ai.azure.com
2. Create a Foundry project.
3. Deploy a model: `gpt-4o-mini` or `gpt-4.1-mini`.
4. Note the endpoint and API key.

---

## Group 9 — FastMCP (after creating the MCP Server project)

FastMCP is installed as a project dependency, not globally.

```bash
cd mcp-server
uv sync
```

Verify:
```bash
uv run fastmcp --version
```

---

## Local .env File

Copy `.env.example` to `.env` in the MCP Server root:

```env
# AI Providers
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# MCP Server mode
MCP_DATA_MODE=mock

# Azure (fill in from Day 5)
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_AI_SEARCH_ENDPOINT=
AZURE_AI_SEARCH_KEY=
AZURE_AI_SEARCH_INDEX=enterprise-knowledge

# Dataverse (fill in from Day 6)
DATAVERSE_URL=https://yourorg.crm.dynamics.com
DATAVERSE_SP_CLIENT_ID=
DATAVERSE_SP_CLIENT_SECRET=
DATAVERSE_SP_TENANT_ID=

# Power Automate
POWER_AUTOMATE_APPROVAL_URL=

# Azure Resources
APPLICATION_INSIGHTS_CONNECTION_STRING=
AZURE_SERVICE_BUS_CONNECTION_STRING=
AZURE_KEY_VAULT_URL=
AZURE_FUNCTION_KEY=
```

---

## Final Verification

Run after installing everything:

```bash
py -3.12 --version        # 3.12.x
node --version            # v24.x
dotnet --version          # 8.0.x
uv --version
git --version
az --version
func --version            # 4.x
pulumi version
pac --version
codex --version
azurite --version
docker --version          # optional
```

---

## Do NOT Install Yet

Do not install or provision these resources before the indicated days:

| Resource | When to create |
|---|---|
| Azure AI Search | Day 8 |
| Application Insights | Day 5 (via Pulumi) |
| Key Vault | Day 5 (via Pulumi) |
| Service Bus | Day 5 (via Pulumi) |
| Dataverse tables | Day 6 |
| Copilot Studio agent | Day 9 |
| Azure AI Foundry agent | Day 9 |
| Power BI dashboard | Day 10 |

---

## Next Step

[docs/01-project-setup.md](01-project-setup.md) — Day 1: repository structure and contracts.
