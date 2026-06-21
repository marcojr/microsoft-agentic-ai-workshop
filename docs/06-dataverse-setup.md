# Stage 6: Dataverse Setup (Day 6)

Create the Power Platform Developer Environment, Dataverse tables and insert sample data.

---

## Day 6 Deliverables

- [ ] Power Platform Developer Environment created
- [ ] Dataverse tables created (Contact, Order, Shipment, Return, Refund, Case, Approval, AgentRun)
- [ ] Sample records inserted
- [ ] Dataverse Web API accessible via token
- [ ] pac CLI authenticated
- [ ] Entra app registration registered with Microsoft Power Platform
- [ ] Dataverse Application User created for the Service Principal
- [ ] Dataverse security role assigned to the Application User

---

## Create the Developer Environment

1. Go to https://make.powerapps.com
2. Select **Environments** → **New**
3. Name: `agentops-dev` | Type: **Developer**
4. Note the URL: `https://yourorg.crm.dynamics.com`

```bash
pac auth create --url https://yourorg.crm.dynamics.com
pac env list
```

`pac auth create` here is for maker/admin setup work only. Runtime code should continue to use the Dataverse Service Principal.

---

## Tables to Create

Preferred path for this repo:

- use the versioned schema file
- deploy it with the provided PowerShell scripts
- avoid hand-creating the schema in the Maker Portal unless you are explicitly studying the UI

Scripted assets:

- schema file: [power-platform/dataverse-schema/schema.v1.json](../power-platform/dataverse-schema/schema.v1.json)
- schema deploy script: [power-platform/scripts/Deploy-AgentOpsDataverseSchema.ps1](../power-platform/scripts/Deploy-AgentOpsDataverseSchema.ps1)
- seed clear script: [power-platform/scripts/Clear-AgentOpsDataverseSeed.ps1](../power-platform/scripts/Clear-AgentOpsDataverseSeed.ps1)
- sample data seed script: [power-platform/scripts/Seed-AgentOpsDataverseData.ps1](../power-platform/scripts/Seed-AgentOpsDataverseData.ps1)

Run from repo root:

```powershell
powershell -ExecutionPolicy Bypass -File .\power-platform\scripts\Deploy-AgentOpsDataverseSchema.ps1
powershell -ExecutionPolicy Bypass -File .\power-platform\scripts\Clear-AgentOpsDataverseSeed.ps1
powershell -ExecutionPolicy Bypass -File .\power-platform\scripts\Seed-AgentOpsDataverseData.ps1
```

On Linux/macOS with PowerShell 7:

```bash
pwsh -File ./power-platform/scripts/Deploy-AgentOpsDataverseSchema.ps1
pwsh -File ./power-platform/scripts/Clear-AgentOpsDataverseSeed.ps1
pwsh -File ./power-platform/scripts/Seed-AgentOpsDataverseData.ps1
```

The scripts read Dataverse credentials from `.env` at the repository root by default. `mcp-server/.env` is still supported as a legacy fallback. Use `-EnvPath <path>` only when intentionally testing another env file.

Important current design choice:

- for v1, custom `cr_*` tables use text reference columns such as `cr_contactid`, `cr_accountid`, `cr_orderkeyref`, `cr_orderitemkeyref`, `cr_returnkeyref`, and `cr_shipmentkeyref`
- this keeps the schema fully scriptable and repeatable through the Dataverse Web API
- standard `accounts` and `contacts` remain standard Dataverse tables

### Contact (standard table)

For the current scripted implementation, the MCP reads from standard Dataverse contact fields:

| Field | Logical Name | Type |
|---|---|---|
| Email | `emailaddress1` | Text |
| Job Title | `jobtitle` | Text |
| Phone | `telephone1` | Text |
| Delivery Address | `address1_line1` | Text |
| Delivery Postcode | `address1_postalcode` | Text |

### cr_order (custom table)

| Field | Logical Name | Type |
|---|---|---|
| Order Key | `cr_orderkey` | Text (primary name) |
| Order Number | `cr_ordernumber` | Text |
| Account ID | `cr_accountid` | Text |
| Contact ID | `cr_contactid` | Text |
| Order Date | `cr_orderdate` | DateTime |
| Status | `cr_status` | Choice: Pending / Shipped / Delivered / Cancelled |
| Total Amount | `cr_totalamount` | Currency |
| Payment Status | `cr_paymentstatus` | Choice: Unpaid / Paid / Refunded |
| Delivery Status | `cr_deliverystatus` | Choice: Pending / InTransit / Delayed / Delivered |
| Shipment Key | `cr_shipmentkeyref` | Text |
| Risk Level | `cr_risklevel` | Choice: Low / Medium / High |
| Delivery Address | `cr_deliveryaddress` | Text |
| Delivery Postcode | `cr_deliverypostcode` | Text |

### cr_shipment (custom table)

| Field | Logical Name | Type |
|---|---|---|
| Shipment Key | `cr_shipmentkey` | Text (primary name) |
| Order Key | `cr_orderkeyref` | Text |
| Carrier | `cr_carrier` | Text |
| Tracking Number | `cr_trackingnumber` | Text |
| Status | `cr_status` | Choice: Pending / InTransit / Delayed / Delivered |
| Estimated Delivery | `cr_estimateddeliverydate` | Date Only |
| Delivered Date | `cr_delivereddate` | DateTime |
| Delay Reason | `cr_delayreason` | Text |
| Origin Postcode | `cr_originpostcode` | Text |
| Destination Postcode | `cr_destinationpostcode` | Text |
| Route Distance Km | `cr_routedistancekm` | Decimal |

### cr_returnrequest (custom table)

| Field | Logical Name | Type |
|---|---|---|
| Return Key | `cr_returnkey` | Text (primary name) |
| Order Key | `cr_orderkeyref` | Text |
| Order Item Key | `cr_orderitemkeyref` | Text |
| Reason | `cr_reason` | Text |
| Status | `cr_status` | Choice: Requested / Approved / Rejected |
| Requested Date | `cr_requesteddate` | DateTime |
| Refund Required | `cr_refundrequired` | Boolean |

### cr_refund (custom table)

| Field | Logical Name | Type |
|---|---|---|
| Refund Key | `cr_refundkey` | Text (primary name) |
| Order Key | `cr_orderkeyref` | Text |
| Return Key | `cr_returnkeyref` | Text |
| Amount | `cr_amount` | Currency |
| Status | `cr_status` | Choice: PendingApproval / Approved / Processed / Rejected |
| Reason | `cr_reason` | Text |
| Requires Approval | `cr_requiresapproval` | Boolean |
| Approved By | `cr_approvedby` | Text |

### cr_approvalrequest (custom table)

| Field | Logical Name | Type |
|---|---|---|
| Approval Key | `cr_approvalkey` | Text (primary name) |
| Related Record ID | `cr_relatedrecordid` | Text |
| Related Record Type | `cr_relatedrecordtype` | Text |
| Requested By | `cr_requestedby` | Text |
| Approval Type | `cr_approvaltype` | Text |
| Status | `cr_status` | Choice: Pending / Approved / Rejected |
| Risk Level | `cr_risklevel` | Choice: Low / Medium / High |
| Reason | `cr_reason` | Multiline Text |
| Approved By | `cr_approvedby` | Text |
| Thread ID | `cr_threadid` | Text |
| Customer Name | `cr_customername` | Text |
| Customer Email | `cr_customeremail` | Text |
| Order Number | `cr_ordernumber` | Text |
| Decision Comment | `cr_decisioncomment` | Multiline Text |
| Decided On | `cr_decidedon` | DateTime |

These additional approval columns support the Power Apps Approval Console. Power Apps can show useful pending-approval context without re-running the agent workflow, while the Orchestrator remains responsible for applying approval decisions to thread state.

### cr_agentrun (custom table — observability)

| Field | Logical Name | Type |
|---|---|---|
| Run Key | `cr_runkey` | Text (primary name) |
| Workflow Name | `cr_workflowname` | Text |
| Intent | `cr_intent` | Text |
| Model Used | `cr_modelused` | Text |
| Vendor Used | `cr_vendorused` | Text |
| Started At | `cr_startedat` | DateTime |
| Status | `cr_status` | Text |
| Input Tokens | `cr_inputtokens` | Integer |
| Output Tokens | `cr_outputtokens` | Integer |
| Estimated Cost | `cr_estimatedcost` | Decimal |
| Latency Ms | `cr_latencyms` | Integer |
| Tools Called | `cr_toolscalled` | Multiline Text (JSON) |
| Requires Approval | `cr_requiresapproval` | Boolean |
| Risk Score | `cr_riskscore` | Decimal |
| Quality Score | `cr_qualityscore` | Decimal |
| Groundedness Score | `cr_groundednessscore` | Decimal |

---

## Inserting Sample Data

### Option A: Power Automate (simplest)

Create a manual flow with "Create a new row" actions for each table.

### Option B: pac data import

```bash
pac data export --environment agentops-dev --table cr_order
pac data import --environment agentops-dev --data ./data/sample-dataverse-records/orders.csv
```

### Option C: Python seed script

```bash
cd mcp-server
uv run python ../../data/seed-scripts/seed_dataverse.py
```

---

## Verify Access via pac CLI

```bash
pac data list --table contact --environment agentops-dev
pac data list --table cr_order --environment agentops-dev
```

---

## Register the Service Principal in Dataverse

The Entra app registration and Service Principal should already be created by Pulumi in Day 5.

This stage is where the clean architecture either holds together or breaks.

For this case, the preferred design is:

- one identity
- created by Pulumi
- stored by Pulumi in Key Vault
- reused by Dataverse as the Application User

Hard requirement:

- the Azure tenant used by Pulumi and the Dataverse environment tenant must be the same

Important: creating the Entra app and Service Principal is not enough by itself.

The identity must first be registered with Microsoft Power Platform, and only then mapped as a Dataverse Application User.

Official references:

- PowerShell registration flow: https://learn.microsoft.com/en-us/power-platform/admin/powershell-create-service-principal
- `New-PowerAppManagementApp`: https://learn.microsoft.com/en-us/powershell/module/microsoft.powerapps.administration.powershell/new-powerappmanagementapp
- Application users: https://learn.microsoft.com/en-us/power-platform/admin/manage-application-users

### Step 1 — Register the existing Entra app with Power Platform

Install the Power Platform PowerShell modules if needed:

```powershell
Install-Module Microsoft.PowerApps.Administration.PowerShell -Scope CurrentUser
Install-Module Microsoft.PowerApps.PowerShell -Scope CurrentUser -AllowClobber
```

Sign in as a human Power Platform admin in the same tenant:

```powershell
Add-PowerAppsAccount -Endpoint prod -TenantID <tenant-id>
```

Register the existing app created by Pulumi:

```powershell
New-PowerAppManagementApp -ApplicationId <pulumi-created-client-id>
Get-PowerAppManagementApp -ApplicationId <pulumi-created-client-id>
```

Without this step, the app might not show up correctly in the Power Platform / Dataverse UI even when the tenant is correct.

### Step 2 — Create the Dataverse Application User

After the Power Platform registration step succeeds, enable that identity inside the Dataverse environment:

1. Open the Power Platform admin center.
2. Open the target environment.
3. Go to **Users + permissions** -> **Application users**.
4. Create a new Application User mapped to the Pulumi-created app registration / Service Principal.
5. Assign the minimum Dataverse security role required for MCP reads/writes.

For the first end-to-end test, using `System Administrator` is acceptable to unblock the integration. Tighten it later.

### Important current behavior

In practice, `pac admin create-service-principal` creates a new Entra application, a new Service Principal, and the Dataverse Application User in one flow.

That means it does **not** reuse the Pulumi-created app registration automatically.

So there are currently two possible patterns:

1. **Pulumi-owned identity path**
   - Pulumi creates the Entra app + Service Principal
   - Power Platform / Dataverse registration must be completed separately
   - preferred architecture for this case
   - keeps the identity under IaC ownership
   - this is the path we want the final workshop to teach

2. **PAC-owned identity path**
   - `pac admin create-service-principal` creates the Entra app, Service Principal, client secret, and Dataverse Application User together
   - fastest way to unblock Dataverse access
   - but it introduces a second identity outside Pulumi control
   - treat this as a workaround experiment, not the final model

## Case Study Finding

What we verified:

1. Pulumi-created identity existed in Entra ID
2. Tenant alignment was correct
3. `New-PowerAppManagementApp` succeeded
4. the Dataverse admin picker still did not surface the Pulumi-created app
5. `pac admin assign-user --application-user` did not create the Application User
6. `pac admin create-service-principal` succeeded only by creating a second identity

This is an important workshop finding:

- "Entra app exists" is not the same thing as "Dataverse Application User is ready"
- Power Platform adds an extra registration/mapping step
- the simple CLI happy-path tends to create its own identity instead of adopting the IaC one
- if the Pulumi identity lives in a different Entra tenant, Dataverse rejects it outright

### Verified root cause in this project

We directly tested the Dataverse Web API and got the real blocking error for the Pulumi-created app:

```text
We didn't find that application ID ... in your Azure Active Directory (Azure AD)
```

That means the Pulumi-created app registration was not in the same Entra tenant that the Dataverse environment was validating against.

Observed tenants in this case:

- Azure / Pulumi tenant: `153c340e-c72a-4676-a178-2f5cb640bd7c`
- Dataverse / PAC-created identity tenant: `92914f74-fa9a-4710-bf05-c9333cb643c9`

Because of that mismatch, the one-identity Pulumi-owned model is currently impossible in this exact environment pairing.

## Official Project Direction

For this project as it exists today, the official runtime identity for Dataverse is the PAC-created Service Principal.

That is the identity that actually works with the current environment pairing.

So the project now distinguishes between:

1. **Target architecture**
   - one Pulumi-owned Service Principal reused by Dataverse
   - still a valid design goal
   - not what this environment pairing can support today

2. **Current implementation**
   - PAC-created Service Principal
   - registered and accepted by the current Dataverse environment
   - this is the identity we will actually use in the running project

Current project status:

- Pulumi-owned identity exists, but cannot be used with the current Dataverse tenant pairing
- PAC-owned identity is the working Dataverse runtime identity for this repo
- the real blocker is identified as tenant mismatch, not a mystery UI problem
- documentation must describe the current implementation honestly

## Current Runtime Credentials

In this environment, use the PAC-created Dataverse identity in `.env`:

```env
DATAVERSE_URL=https://yourorg.crm.dynamics.com
DATAVERSE_SP_CLIENT_ID=<pac-created-client-id>
DATAVERSE_SP_CLIENT_SECRET=<pac-created-client-secret>
DATAVERSE_SP_TENANT_ID=<pac-created-tenant-id>
```

For this project's current setup, these values do **not** come from the Pulumi-managed identity.

Rule:

- in the current repo state, these values should come from the PAC-created Dataverse identity
- if tenant alignment is fixed later, we can switch back to the Pulumi-owned identity and document that transition in `progress.md`

---

## Export Dataverse Schema

```bash
pac solution export \
  --path ./power-platform/solutions/ \
  --name AgentOpsSchema \
  --managed false

# Import to another environment
pac solution import \
  --path ./power-platform/solutions/AgentOpsSchema.zip
```

---

## Next Step

[docs/07-dataverse-integration.md](07-dataverse-integration.md) — Day 7: replace mocks with Dataverse.
