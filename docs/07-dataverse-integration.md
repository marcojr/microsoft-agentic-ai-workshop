# Stage 7: Dataverse Integration (Day 7)

Replace mock JSON data with live Dataverse Web API calls. Keep mock mode as a fallback.

---

## Day 7 Deliverables

- [ ] `dataverse_service.py` implemented with MSAL authentication
- [ ] `get_customer_by_email` reading from Dataverse
- [ ] `get_latest_order` reading from Dataverse
- [ ] `get_shipment_status` reading from Dataverse
- [ ] `get_returns_for_order` reading from Dataverse
- [ ] `get_refunds_for_order` reading from Dataverse
- [ ] `log_agent_run` writing to Dataverse AgentRun table
- [ ] `create_approval_request` writing to Dataverse ApprovalRequest table
- [ ] Mock mode still functional with `MCP_DATA_MODE=mock`

---

## Dataverse Service

**File:** `mcp-server/src/enterprise_agentops_mcp/services/dataverse_service.py`

```python
import httpx
import msal
from enterprise_agentops_mcp.config import (
    DATAVERSE_URL, DATAVERSE_SP_CLIENT_ID,
    DATAVERSE_SP_CLIENT_SECRET, DATAVERSE_SP_TENANT_ID
)

def _get_token() -> str:
    app = msal.ConfidentialClientApplication(
        client_id=DATAVERSE_SP_CLIENT_ID,
        client_credential=DATAVERSE_SP_CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{DATAVERSE_SP_TENANT_ID}"
    )
    result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
    if "access_token" not in result:
        raise RuntimeError(f"Failed to acquire Dataverse token: {result.get('error_description')}")
    return result["access_token"]

def _headers() -> dict:
    return {
        "Authorization": f"Bearer {_get_token()}",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

def dv_get(entity: str, filter_query: str = "", select: str = "") -> list[dict]:
    url = f"{DATAVERSE_URL}/api/data/v9.2/{entity}"
    params = []
    if filter_query:
        params.append(f"$filter={filter_query}")
    if select:
        params.append(f"$select={select}")
    if params:
        url += "?" + "&".join(params)
    response = httpx.get(url, headers=_headers(), timeout=15)
    response.raise_for_status()
    return response.json().get("value", [])

def dv_post(entity: str, data: dict) -> dict:
    url = f"{DATAVERSE_URL}/api/data/v9.2/{entity}"
    response = httpx.post(url, json=data, headers=_headers(), timeout=15)
    response.raise_for_status()
    return response.json() if response.content else {"status": "created"}
```

---

## Updated Tool: get_customer_by_email

```python
@router.tool()
def get_customer_by_email(email: str) -> dict:
    if DATA_MODE == "mock":
        # ... unchanged mock implementation ...
        pass

    from enterprise_agentops_mcp.services.dataverse_service import dv_get
    results = dv_get(
        "contacts",
        filter_query=f"emailaddress1 eq '{email}'",
        select="contactid,fullname,emailaddress1,jobtitle,telephone1,_accountid_value"
    )
    if not results:
        return {"error": f"Customer not found: {email}"}
    row = results[0]

    account_results = dv_get(
        "accounts",
        filter_query=f"accountid eq {row['_accountid_value']}",
        select="accountid,name,cr_risklevel"
    ) if row.get("_accountid_value") else []
    account = account_results[0] if account_results else {}

    return {
        "contactId": row["contactid"],
        "accountId": row.get("_accountid_value", ""),
        "fullName": row["fullname"],
        "email": row["emailaddress1"],
        "role": row.get("jobtitle", ""),
        "phone": row.get("telephone1", ""),
        "accountName": account.get("name", ""),
        "riskLevel": account.get("cr_risklevel", "Unknown")
    }
```

---

## Updated Tool: get_latest_order

```python
@router.tool()
def get_latest_order(contact_id: str) -> dict:
    if DATA_MODE == "mock":
        # ... unchanged mock implementation ...
        pass

    from enterprise_agentops_mcp.services.dataverse_service import dv_get
    results = dv_get(
        "cr_orders",
        filter_query=f"_cr_contactid_value eq {contact_id}",
        select="cr_orderid,cr_ordernumber,cr_orderdate,cr_status,cr_totalamount,cr_deliverystatus,cr_shipmentid,cr_risklevel,cr_deliverypostcode"
    )
    if not results:
        return {"error": f"No orders found for contact: {contact_id}"}

    latest = sorted(results, key=lambda o: o.get("cr_orderdate", ""), reverse=True)[0]
    return {
        "orderId": latest["cr_orderid"],
        "orderNumber": latest["cr_ordernumber"],
        "orderDate": latest.get("cr_orderdate"),
        "status": latest.get("cr_status"),
        "totalAmount": latest.get("cr_totalamount"),
        "deliveryStatus": latest.get("cr_deliverystatus"),
        "shipmentId": latest.get("cr_shipmentid"),
        "riskLevel": latest.get("cr_risklevel"),
        "deliveryPostcode": latest.get("cr_deliverypostcode")
    }
```

---

## Updated Tool: log_agent_run (writes to Dataverse)

```python
# Inside log_agent_run, after building the run dict:
if DATA_MODE == "mock":
    runs = load("agent_runs.json")
    runs.append(run)
    save("agent_runs.json", runs)
else:
    import json as _json
    from enterprise_agentops_mcp.services.dataverse_service import dv_post
    dv_post("cr_agentruns", {
        "cr_runid": run_id,
        "cr_workflowname": workflow_name,
        "cr_intent": intent,
        "cr_modelused": model_used,
        "cr_vendorused": vendor,
        "cr_startedat": run["startedAt"],
        "cr_status": "Completed",
        "cr_inputtokens": input_tokens,
        "cr_outputtokens": output_tokens,
        "cr_estimatedcost": estimated_cost,
        "cr_latencyms": latency_ms,
        "cr_toolscalled": _json.dumps(tools_called),
        "cr_requiresapproval": requires_approval,
        "cr_riskscore": risk_score,
        "cr_qualityscore": quality_score,
        "cr_groundednessscore": groundedness_score
    })
```

---

## Switching Between Mock and Dataverse

`.env`:
```env
MCP_DATA_MODE=mock       # Use local JSON files
MCP_DATA_MODE=dataverse  # Use Dataverse Web API
```

---

## Next Step

[docs/08-secure-rag.md](08-secure-rag.md) — Day 8: Azure AI Search + Secure RAG.
