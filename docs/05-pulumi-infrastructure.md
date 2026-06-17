# Stage 5: Pulumi Infrastructure (Day 5)

Create all Azure resources via Pulumi. Pulumi is the primary IaC tool for this project — nothing is created manually in the portal.

---

## Day 5 Deliverables

- [ ] Pulumi TypeScript project initialised
- [ ] Resource Group created
- [ ] Storage Account created
- [ ] Azure Function App provisioned
- [ ] Application Insights created
- [ ] Key Vault created
- [ ] Entra app registration + Service Principal created for Dataverse access
- [ ] Dataverse client credentials stored in Key Vault
- [ ] `pulumi up --stack dev` runs without errors
- [ ] Outputs exported (Function URL, App Insights connection string, Key Vault URL, Dataverse client ID, tenant ID)

---

## Pulumi Project Setup

```bash
cd infrastructure/pulumi

# Init TypeScript project
pulumi new azure-typescript --name enterprise-agentops --stack dev

# Install providers
npm install @pulumi/azure-native @pulumi/pulumi @pulumi/azuread

# Login local (no Pulumi Cloud account needed)
pulumi login --local
```

---

## Pulumi.yaml

```yaml
name: enterprise-agentops
runtime: nodejs
description: Enterprise AgentOps Control Tower — Azure Infrastructure
```

---

## Pulumi.dev.yaml

```yaml
config:
  azure-native:location: uksouth
  enterprise-agentops:resourceGroupName: rg-agentops-dev
  enterprise-agentops:prefix: agentops
  enterprise-agentops:environment: dev
```

---

## config.ts

```typescript
import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config();
const azureConfig = new pulumi.Config("azure-native");

export const location = azureConfig.get("location") || "uksouth";
export const resourceGroupName = config.get("resourceGroupName") || "rg-agentops-dev";
export const prefix = config.get("prefix") || "agentops";
export const environment = config.get("environment") || "dev";
export const suffix = `${prefix}-${environment}`;
```

---

## resources/resourceGroup.ts

```typescript
import * as azure from "@pulumi/azure-native";
import { location, resourceGroupName } from "../config";

export const resourceGroup = new azure.resources.ResourceGroup("rg", {
    resourceGroupName,
    location,
});
```

---

## resources/storage.ts

```typescript
import * as azure from "@pulumi/azure-native";
import { resourceGroup } from "./resourceGroup";
import { suffix } from "../config";

export const storageAccount = new azure.storage.StorageAccount("storage", {
    resourceGroupName: resourceGroup.name,
    location: resourceGroup.location,
    accountName: `st${suffix.replace(/-/g, "")}`,
    sku: { name: "Standard_LRS" },
    kind: "StorageV2",
});
```

---

## resources/appInsights.ts

```typescript
import * as azure from "@pulumi/azure-native";
import { resourceGroup } from "./resourceGroup";
import { suffix } from "../config";

export const workspace = new azure.operationalinsights.Workspace("workspace", {
    resourceGroupName: resourceGroup.name,
    location: resourceGroup.location,
    workspaceName: `law-${suffix}`,
    sku: { name: "PerGB2018" },
    retentionInDays: 30,
});

export const appInsights = new azure.insights.Component("appinsights", {
    resourceGroupName: resourceGroup.name,
    location: resourceGroup.location,
    resourceName: `ai-${suffix}`,
    kind: "web",
    applicationType: "web",
    workspaceResourceId: workspace.id,
});

export const connectionString = appInsights.connectionString;
```

---

## resources/keyVault.ts

```typescript
import * as azure from "@pulumi/azure-native";
import { resourceGroup } from "./resourceGroup";
import { suffix } from "../config";

const currentClientConfig = azure.authorization.getClientConfigOutput();

export const keyVault = new azure.keyvault.Vault("keyvault", {
    resourceGroupName: resourceGroup.name,
    location: resourceGroup.location,
    vaultName: `kv-${suffix}`,
    properties: {
        sku: { family: "A", name: "standard" },
        tenantId: currentClientConfig.tenantId,
        accessPolicies: [],
        enableRbacAuthorization: true,
        enableSoftDelete: true,
        softDeleteRetentionInDays: 7,
    },
});

export const keyVaultUri = keyVault.properties.vaultUri;
```

---

## resources/identity.ts

Create the Dataverse application identity with Pulumi so backend access uses a Service Principal instead of interactive user auth.

```typescript
import * as azuread from "@pulumi/azuread";

export const dataverseApp = new azuread.Application("dataverseApp", {
    displayName: "agentops-dataverse-sp",
});

export const dataverseSp = new azuread.ServicePrincipal("dataverseSp", {
    clientId: dataverseApp.clientId,
});

export const dataverseSpSecret = new azuread.ApplicationPassword("dataverseSpSecret", {
    applicationId: dataverseApp.id,
    displayName: "default",
});
```

This identity is later registered as a Dataverse Application User during Day 6.

---

## resources/functionApp.ts

```typescript
import * as azure from "@pulumi/azure-native";
import { resourceGroup } from "./resourceGroup";
import { storageAccount } from "./storage";
import { connectionString } from "./appInsights";
import { suffix } from "../config";

const plan = new azure.web.AppServicePlan("plan", {
    resourceGroupName: resourceGroup.name,
    location: resourceGroup.location,
    name: `asp-${suffix}`,
    kind: "FunctionApp",
    sku: { name: "Y1", tier: "Dynamic" },
});

export const functionApp = new azure.web.WebApp("funcapp", {
    resourceGroupName: resourceGroup.name,
    location: resourceGroup.location,
    name: `func-${suffix}`,
    kind: "FunctionApp",
    serverFarmId: plan.id,
    siteConfig: {
        appSettings: [
            { name: "FUNCTIONS_WORKER_RUNTIME", value: "python" },
            { name: "FUNCTIONS_EXTENSION_VERSION", value: "~4" },
            { name: "AzureWebJobsStorage", value: storageAccount.name.apply(
                n => `DefaultEndpointsProtocol=https;AccountName=${n};EndpointSuffix=core.windows.net`
            )},
            { name: "APPLICATIONINSIGHTS_CONNECTION_STRING", value: connectionString },
            { name: "MCP_DATA_MODE", value: "mock" },
        ],
        pythonVersion: "3.12",
    },
    httpsOnly: true,
});

export const functionAppUrl = functionApp.defaultHostName.apply(h => `https://${h}`);
```

---

## index.ts

```typescript
import { resourceGroup } from "./resources/resourceGroup";
import { storageAccount } from "./resources/storage";
import { connectionString } from "./resources/appInsights";
import { keyVaultUri } from "./resources/keyVault";
import { functionApp, functionAppUrl } from "./resources/functionApp";
import { dataverseApp } from "./resources/identity";
import * as azure from "@pulumi/azure-native";

export const rgName = resourceGroup.name;
export const storageAccountName = storageAccount.name;
export const appInsightsConnectionString = connectionString;
export const keyVaultUrl = keyVaultUri;
export const functionAppEndpoint = functionAppUrl;
export const dataverseClientId = dataverseApp.clientId;
export const tenantId = azure.authorization.getClientConfigOutput().tenantId;
```

---

## Deploy

```bash
cd infrastructure/pulumi

az login

pulumi preview --stack dev
pulumi up --stack dev
pulumi stack output --stack dev
```

---

## Add Secrets to Key Vault

```bash
az keyvault secret set --vault-name kv-agentops-dev --name anthropic-api-key --value "sk-ant-..."
az keyvault secret set --vault-name kv-agentops-dev --name openai-api-key --value "sk-..."
az keyvault secret set --vault-name kv-agentops-dev --name dataverse-client-id --value "<client-id>"
az keyvault secret set --vault-name kv-agentops-dev --name dataverse-client-secret --value "<client-secret>"
az keyvault secret set --vault-name kv-agentops-dev --name dataverse-tenant-id --value "<tenant-id>"
az keyvault secret set --vault-name kv-agentops-dev --name dataverse-url --value "https://yourorg.crm.dynamics.com"
```

---

## Destroy When No Longer Needed

```bash
pulumi destroy --stack dev
```

---

## Next Step

[docs/06-dataverse-setup.md](06-dataverse-setup.md) — Day 6: Dataverse tables and sample data.
