# Stage 5: Pulumi Infrastructure (Day 5)

Create Azure resources with Pulumi, but only after the Azure context file is generated.

---

## Day 5 Deliverables

- [x] Pulumi C# project initialised
- [x] `infrastructure/config/azure-context.json` created
- [x] Resource names generated from Microsoft CAF naming guidance
- [x] Sequence-based names generated for disposable resources
- [x] One-line resource-group teardown flow defined
- [x] Persistent recovery storage kept outside the disposable resource group
- [x] Resource Group created
- [x] Storage Account created
- [x] Azure Table Storage table for runtime thread state created
- [x] Azure Function App created
- [x] Application Insights created
- [x] Log Analytics Workspace created
- [x] Key Vault created
- [x] Azure AI Search created
- [x] Azure OpenAI account and chat deployment created
- [x] Service Bus namespace and queues created
- [x] Entra app registration + Service Principal created for Dataverse access
- [x] `pulumi up --stack dev` runs without errors

---

## Current Implementation Status

Already implemented in the Pulumi C# scaffold:

- workload resource group
- persistent recovery resource group
- workload storage account
- persistent recovery storage account
- persistent recovery blob container
- Log Analytics workspace
- Application Insights connected to the workspace
- Key Vault with RBAC enabled
- Entra App Registration for Dataverse runtime
- Entra Service Principal for Dataverse runtime
- client secret generation for the Dataverse runtime identity
- Dataverse SP client ID, client secret, and tenant ID stored as Key Vault secrets
- Flex Consumption Function App plan
- Flex Consumption Linux Function App configured for Python 3.12
- Azure AI Search Free service
- Azure OpenAI account with `gpt-5-mini` deployment, model version `2025-08-07`, SKU `GlobalStandard`
- Service Bus Basic namespace
- Service Bus queues:
  - `approval-requests`
  - `agent-run-events`
  - `workflow-deadletter`
- Service Bus runtime auth rule named `agentops-runtime`
- Service Bus connection string stored in Key Vault as `AZURE-SERVICE-BUS-CONNECTION-STRING`
- Azure OpenAI endpoint, API key, and deployment name stored in Key Vault

Still pending:

- post-provision ingest/restore automation

Already verified in practice:

- `pulumi up` succeeded against a real initialized `infrastructure/config/azure-context.json`
- the disposable workload resource group and persistent recovery resource group were both created
- the Pulumi-managed Dataverse runtime identity was created in Entra ID
- Azure AI Search was provisioned and used by the local MCP knowledge tool
- Azure OpenAI is managed by Pulumi as the primary enterprise LLM provider
- Service Bus was provisioned and verified with a send/receive smoke test

---

## Naming Standard

We will follow Microsoft naming guidance, not ad-hoc names.

Primary sources:

- Microsoft CAF naming guidance: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming
- Microsoft CAF resource abbreviations: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations
- Azure resource name rules and restrictions: https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-name-rules
- Azure resource organization guidance: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-setup-guide/organize-resources

Working convention for this project:

```text
{abbreviation}-{workload}-{environment}-{region}-{instance}
```

Important:

- Not every Azure resource can use the same format.
- Some resources are global and must be unique.
- Some resources do not allow hyphens, such as storage accounts.
- Pulumi must read the generated JSON and use the precomputed names from there.
- The sequence is mandatory for disposable study environments so recreated resources do not collide with soft-deleted names.

Examples for this project:

```text
rg-agentops-dev-001
func-agentops-dev-001
kv-agentops-dev-uks-001
appi-agentops-dev-uks-001
log-agentops-dev-uks-001
sbns-agentops-dev-001
srch-agentops-dev-001
stagentopsdevuks001
```

---

## Azure Context JSON

The bootstrap file lives here:

```text
infrastructure/config/azure-context.json
```

Versioned example:

```text
infrastructure/config/azure-context.example.json
```

This file stores:

- selected subscription
- workload root
- environment
- Azure region
- region short code
- current sequence number
- next sequence number
- base tags
- persistent recovery storage settings
- seed/restore settings
- generated resource names

Pulumi should treat this file as the source of truth for naming and deployment context.

---

## Ephemeral Environment Rule

This Azure setup is for study and lab work.

That means:

- the workload resource group is disposable
- all workload resources inside that resource group must be safe to delete together
- recovery data must not live in the same disposable resource group

Disposable:

- workload resource group
- function app
- workload storage account
- app insights
- log analytics workspace
- key vault
- service bus
- AI Search
- Azure OpenAI

Persistent:

- recovery resource group
- recovery storage account
- recovery blob container

The recovery storage is where we keep:

- exported Dataverse data files
- blob/file dumps
- knowledge document copies
- resumable environment state for reseed

If the whole study environment is destroyed, the recovery storage survives and the next environment can be rebuilt from it.

---

## Bootstrap Script

Run this before starting the Pulumi project:

```powershell
powershell -ExecutionPolicy Bypass -File .\infrastructure\scripts\Initialize-AzureContext.ps1
```

What it does:

1. Uses Azure CLI login if needed.
2. Lists subscriptions.
3. Lets you choose the target subscription.
4. Asks for workload root, environment, region, and instance number.
5. Generates CAF-style names.
6. Saves everything into `infrastructure/config/azure-context.json`.

The script also captures the initial sequence number. Example:

- first lab environment: `001`
- after destroy: `002`
- next rebuild: `003`

This avoids failures caused by Azure resources that keep names reserved for a while after deletion.

---

## One-Line Teardown

To delete the disposable workload resource group and advance the sequence:

```powershell
powershell -ExecutionPolicy Bypass -File .\infrastructure\scripts\Remove-AzureEnvironment.ps1
```

This script:

1. reads `infrastructure/config/azure-context.json`
2. deletes the current workload resource group
3. increments the sequence
4. recalculates all disposable resource names
5. writes the updated JSON back

So the next `pulumi up` uses fresh names automatically.

---

## Pulumi Project Setup

```bash
cd infrastructure/pulumi

pulumi new azure-csharp --name enterprise-agentops --stack dev
dotnet restore
pulumi login --local
```

Current repo choice:

```text
Pulumi in C#
```

---

## Expected Pulumi Config Shape

Pulumi will read the JSON file and use those values instead of hardcoded names.

Expected fields:

```json
{
  "subscription": {
    "id": "...",
    "name": "..."
  },
  "workload": {
    "root": "agentops"
  },
  "environment": "dev",
  "location": {
    "name": "uksouth",
    "short": "uks"
  },
  "sequence": {
    "current": "001",
    "next": "002",
    "padTo": 3
  },
  "tags": {
    "workload": "agentops",
    "environment": "dev"
  },
  "recovery": {
    "resourceGroup": "rg-agentops-state",
    "storageAccount": "stagentopsstateuks001",
    "container": "environment-dumps"
  },
  "bootstrapData": {
    "ingestOnProvision": true
  },
  "resources": {
    "resourceGroup": "rg-agentops-dev-001",
    "storageAccount": "stagentopsdevuks001",
    "functionApp": "func-agentops-dev-001",
    "appInsights": "appi-agentops-dev-uks-001",
    "logAnalyticsWorkspace": "log-agentops-dev-uks-001",
    "keyVault": "kv-agentops-dev-uks-001",
    "azureOpenAi": "oai-agentops-dev-uks-001",
    "serviceBusNamespace": "sbns-agentops-dev-001",
    "aiSearch": "srch-agentops-dev-001"
  }
}
```

---

## Resource Scope

Initial Pulumi scope:

- Resource Group
- Storage Account
- Azure Table Storage table for thread state
- Azure Function App
- Application Insights
- Log Analytics Workspace
- Key Vault
- Azure AI Search
- Service Bus
- Entra app registration
- Service Principal

Optional later:

- API Management

Current Function App shape:

- runtime: Python 3.12
- hosting: Flex Consumption
- app settings:
  - `AzureWebJobsStorage__accountName`
  - `APPLICATIONINSIGHTS_CONNECTION_STRING`
  - `MCP_DATA_MODE=mock`

Flex-specific notes:

- the Function App no longer uses legacy Linux Consumption `Y1`
- the hosting plan now uses `FC1` with tier `FlexConsumption`
- deployment storage is configured through `functionAppConfig.deployment.storage`
- the Function App uses a system-assigned managed identity with Storage Blob Data Owner on the workload storage account

Current Service Bus shape:

- namespace SKU: Basic
- runtime rule: `agentops-runtime`
- runtime rights: `Send`, `Listen`
- queues:
  - `approval-requests`
  - `agent-run-events`
  - `workflow-deadletter`
- local producer service: `mcp-server/src/enterprise_agentops_mcp/services/service_bus_service.py`
- local peek script: `infrastructure/scripts/peek_service_bus_queue.py`

To inspect messages without removing them:

```powershell
uv run --project mcp-server python infrastructure\scripts\peek_service_bus_queue.py --queue agent-run-events --max-messages 5
uv run --project mcp-server python infrastructure\scripts\peek_service_bus_queue.py --queue approval-requests --max-messages 5
```

Current Azure AI Search shape:

- SKU: Free
- index: `enterprise-knowledge`
- ingestion script: `infrastructure/scripts/ingest_documents.py`
- index creation script: `infrastructure/scripts/create_search_index.py`

---

## Dataverse Identity

Pulumi will create the Entra app registration and Service Principal for Dataverse runtime access.

Runtime auth standard:

```text
Service Principal
```

That identity is later registered in Dataverse as an Application User.

Current secret material written to Key Vault:

- `DATAVERSE-SP-CLIENT-ID`
- `DATAVERSE-SP-CLIENT-SECRET`
- `DATAVERSE-SP-TENANT-ID`
- `AZURE-OPENAI-ENDPOINT`
- `AZURE-OPENAI-API-KEY`
- `AZURE-OPENAI-DEPLOYMENT-NAME`

To sync Azure OpenAI values into the local ignored `.env`:

```powershell
powershell -ExecutionPolicy Bypass -File infrastructure/scripts/Sync-AzureOpenAiEnv.ps1
```

## Case Decision

For this case study, the intended architecture is:

1. Pulumi creates the Entra app registration
2. Pulumi creates the Service Principal
3. Pulumi stores the runtime credentials in Key Vault
4. Day 6 maps that same identity into Dataverse as an Application User

Important:

- this is the clean target model for the case
- Dataverse must consume the same identity that Pulumi created
- creating a second identity outside IaC is considered a temporary experiment, not the final architecture
- Azure and Dataverse must point to the same Entra tenant for this to work

What happened in practice:

- Pulumi successfully created the Entra app + Service Principal
- Power Platform registration also succeeded
- but the Dataverse Application User flow did not attach cleanly to that identity from the normal admin UI / CLI path
- `pac admin create-service-principal` worked only by creating a second identity

So the current repo documents both:

- the intended Pulumi-owned identity model
- the observed Dataverse behavior that currently pushes toward a second identity unless we solve the registration path more cleanly

Current implementation decision:

- keep the Pulumi-created identity documented as the intended IaC-owned model
- but use the PAC-created Dataverse identity for the actual running project in this environment

## Tenant Alignment Check

Before trying to map the Pulumi-created identity into Dataverse, verify tenant parity:

```powershell
powershell -ExecutionPolicy Bypass -File .\infrastructure\scripts\Test-DataverseTenantAlignment.ps1 -DataverseTenantId <dataverse-tenant-id>
```

If this check fails, stop there.

Do not expect Dataverse to accept an app registration created in a different Entra tenant.

---

## Rule For This Repo

Do not invent Azure names manually in code or in the portal.

The flow is:

1. Run `Initialize-AzureContext.ps1`
2. Review `azure-context.json`
3. Let Pulumi read that file
4. Provision the disposable resource group
5. Ingest local seed files and recovery dumps when the environment comes up
6. When finished studying, run `Remove-AzureEnvironment.ps1`

Important design rule:

- recovery dumps must live in persistent blob storage outside the disposable workload resource group
- Pulumi source code lives in C#, not TypeScript
