# Stage 6: Dataverse Setup (Day 6)

Create the Power Platform Developer Environment, Dataverse tables and insert sample data.

---

## Day 6 Deliverables

- [ ] Power Platform Developer Environment created
- [ ] Dataverse tables created (Contact, Order, Shipment, Return, Refund, Case, Approval, AgentRun)
- [ ] Sample records inserted
- [ ] Dataverse Web API accessible via token
- [ ] pac CLI authenticated
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

Create via Power Apps Maker Portal (make.powerapps.com → Tables) or via pac CLI.

### Contact (extend standard table)

Add custom fields to the standard Contact table:

| Field | Logical Name | Type |
|---|---|---|
| Delivery Address | `cr_deliveryaddress` | Multiline Text |
| Delivery Postcode | `cr_deliverypostcode` | Text |
| Risk Level | `cr_risklevel` | Choice: Low / Medium / High |

### cr_order (custom table)

| Field | Logical Name | Type |
|---|---|---|
| Order ID | `cr_orderid` | Text (primary) |
| Order Number | `cr_ordernumber` | Text |
| Account | `cr_accountid` | Lookup → Account |
| Contact | `cr_contactid` | Lookup → Contact |
| Order Date | `cr_orderdate` | DateTime |
| Status | `cr_status` | Choice: Pending / Shipped / Delivered / Cancelled |
| Total Amount | `cr_totalamount` | Currency |
| Payment Status | `cr_paymentstatus` | Choice: Unpaid / Paid / Refunded |
| Delivery Status | `cr_deliverystatus` | Choice: Pending / InTransit / Delayed / Delivered |
| Shipment ID | `cr_shipmentid` | Text |
| Risk Level | `cr_risklevel` | Choice: Low / Medium / High |
| Delivery Address | `cr_deliveryaddress` | Text |
| Delivery Postcode | `cr_deliverypostcode` | Text |

### cr_shipment (custom table)

| Field | Logical Name | Type |
|---|---|---|
| Shipment ID | `cr_shipmentid` | Text (primary) |
| Order | `cr_orderid` | Lookup → cr_order |
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
| Return ID | `cr_returnid` | Text (primary) |
| Order | `cr_orderid` | Lookup → cr_order |
| Reason | `cr_reason` | Text |
| Status | `cr_status` | Choice: Requested / Approved / Rejected |
| Requested Date | `cr_requesteddate` | DateTime |
| Refund Required | `cr_refundrequired` | Boolean |

### cr_refund (custom table)

| Field | Logical Name | Type |
|---|---|---|
| Refund ID | `cr_refundid` | Text (primary) |
| Order | `cr_orderid` | Lookup → cr_order |
| Amount | `cr_amount` | Currency |
| Status | `cr_status` | Choice: PendingApproval / Approved / Processed / Rejected |
| Reason | `cr_reason` | Text |
| Requires Approval | `cr_requiresapproval` | Boolean |
| Approved By | `cr_approvedby` | Text |

### cr_approvalrequest (custom table)

| Field | Logical Name | Type |
|---|---|---|
| Approval ID | `cr_approvalid` | Text (primary) |
| Related Record ID | `cr_relatedrecordid` | Text |
| Related Record Type | `cr_relatedrecordtype` | Text |
| Requested By | `cr_requestedby` | Text |
| Approval Type | `cr_approvaltype` | Text |
| Status | `cr_status` | Choice: Pending / Approved / Rejected |
| Risk Level | `cr_risklevel` | Choice: Low / Medium / High |
| Reason | `cr_reason` | Multiline Text |
| Approved By | `cr_approvedby` | Text |

### cr_agentrun (custom table — observability)

| Field | Logical Name | Type |
|---|---|---|
| Run ID | `cr_runid` | Text (primary) |
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

This step is about enabling that identity inside Dataverse:

1. Open the Power Platform admin center.
2. Open the target environment.
3. Go to **Users + permissions** -> **Application users**.
4. Create a new Application User mapped to the Pulumi-created Service Principal.
5. Assign the minimum Dataverse security role required for MCP reads/writes.

Add to `.env`:
```env
DATAVERSE_URL=https://yourorg.crm.dynamics.com
DATAVERSE_SP_CLIENT_ID=<pulumi-created-service-principal-client-id>
DATAVERSE_SP_CLIENT_SECRET=<pulumi-created-service-principal-client-secret>
DATAVERSE_SP_TENANT_ID=<service-principal-tenant-id>
```

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
