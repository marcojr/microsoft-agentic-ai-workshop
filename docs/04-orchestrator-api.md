# Stage 4: Orchestrator API (Day 4)

Build the Azure Functions backend that connects Copilot Studio to the MCP Server and agent orchestration layer.

---

## Day 4 Deliverables

- [ ] Azure Functions project scaffolded (Python)
- [ ] `POST /api/agents/webshop/order-support` endpoint implemented
- [ ] MCP tools called via local wrapper
- [ ] Structured JSON response returned
- [ ] `local.settings.json` configured
- [ ] Tested with `func start` and REST Client

---

## Scaffold Azure Functions

```bash
cd apps/orchestrator-api

func init . --python
func new --name webshop_order_support --template "HTTP trigger" --authlevel "function"
func new --name customer_case_summarise --template "HTTP trigger" --authlevel "function"
func new --name agent_runs --template "HTTP trigger" --authlevel "anonymous"
```

---

## local.settings.json

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "GEMINI_API_KEY": "",
    "AI_PRIMARY_PROVIDER": "azure_openai",
    "AI_PRIMARY_VENDOR": "Azure OpenAI",
    "AI_PRIMARY_MODEL": "gpt-5-mini",
    "AZURE_OPENAI_ENDPOINT": "",
    "AZURE_OPENAI_API_KEY": "",
    "AZURE_OPENAI_DEPLOYMENT_NAME": "gpt-5-mini",
    "AI_SECONDARY_PROVIDER": "gemini",
    "AI_SECONDARY_VENDOR": "Gemini",
    "AI_SECONDARY_MODEL": "gemini-3.5-flash",
    "MCP_DATA_MODE": "mock",
    "POWER_AUTOMATE_APPROVAL_URL": ""
  }
}
```

---

## MCP Client Wrapper

**File:** `apps/orchestrator-api/src/shared/mcp_client.py`

In the MVP, the client imports directly from the MCP Server Python package. In production, it would use the MCP client library or HTTP.

```python
import sys, os

MCP_SERVER_PATH = os.getenv("MCP_SERVER_PATH", "../../mcp-server/src")
sys.path.insert(0, MCP_SERVER_PATH)

class MCPClient:
    def call(self, tool_name: str, params: dict) -> dict:
        from enterprise_agentops_mcp.tools.customers import get_customer_by_email
        from enterprise_agentops_mcp.tools.orders import get_latest_order, get_order_details, get_order_items
        from enterprise_agentops_mcp.tools.shipments import get_shipment_status
        from enterprise_agentops_mcp.tools.returns import get_returns_for_order, get_refunds_for_order
        from enterprise_agentops_mcp.tools.cases import get_open_cases, get_case_details
        from enterprise_agentops_mcp.tools.knowledge import search_knowledge_articles
        from enterprise_agentops_mcp.tools.approvals import create_approval_request, create_follow_up_task
        from enterprise_agentops_mcp.tools.cost import calculate_agent_run_cost
        from enterprise_agentops_mcp.tools.observability import log_agent_run
        from enterprise_agentops_mcp.tools.evaluation import evaluate_response

        tool_map = {
            "get_customer_by_email": get_customer_by_email,
            "get_latest_order": get_latest_order,
            "get_order_details": get_order_details,
            "get_order_items": get_order_items,
            "get_shipment_status": get_shipment_status,
            "get_returns_for_order": get_returns_for_order,
            "get_refunds_for_order": get_refunds_for_order,
            "get_open_cases": get_open_cases,
            "get_case_details": get_case_details,
            "search_knowledge_articles": search_knowledge_articles,
            "create_approval_request": create_approval_request,
            "create_follow_up_task": create_follow_up_task,
            "calculate_agent_run_cost": calculate_agent_run_cost,
            "log_agent_run": log_agent_run,
            "evaluate_response": evaluate_response,
        }
        fn = tool_map.get(tool_name)
        if fn is None:
            return {"error": f"Unknown tool: {tool_name}"}
        return fn(**params)
```

---

## Endpoint: webshop/order-support

**File:** `apps/orchestrator-api/src/webshop_order_support/__init__.py`

```python
import json, time
import azure.functions as func
from shared.mcp_client import MCPClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    start = time.time()
    client = MCPClient()

    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    customer_email = body.get("customerEmail")
    if not customer_email:
        return func.HttpResponse("customerEmail is required", status_code=400)

    # Step 1: Resolve customer
    customer = client.call("get_customer_by_email", {"email": customer_email})
    if "error" in customer:
        return func.HttpResponse(json.dumps(customer), status_code=404, mimetype="application/json")

    # Step 2: Get latest order
    order = client.call("get_latest_order", {"contact_id": customer["contactId"]})
    if "error" in order:
        return func.HttpResponse(json.dumps(order), status_code=404, mimetype="application/json")

    # Step 3: Order items, shipment, returns, refunds
    order_items = client.call("get_order_items", {"order_id": order["orderId"]})
    shipment = client.call("get_shipment_status", {"shipment_id": order["shipmentId"]})
    returns = client.call("get_returns_for_order", {"order_id": order["orderId"]})
    refunds = client.call("get_refunds_for_order", {"order_id": order["orderId"]})

    # Step 4: Search knowledge
    knowledge = client.call("search_knowledge_articles", {
        "query": "delivery delay compensation refund approval policy",
        "max_results": 3
    })

    # Step 5: Build summary (replaced by SK agents in Stage 9)
    has_delay = shipment.get("status") == "Delayed"
    has_refund = any(r.get("requiresApproval") for r in refunds.get("refunds", []))
    risk = "High" if (has_delay and has_refund) else "Medium"

    summary = (
        f"{customer['fullName']}'s latest order is {order['orderNumber']}. "
        f"Delivery status: {order['deliveryStatus']}."
    )
    if has_delay:
        summary += f" Shipment delayed: {shipment.get('delayReason', 'unknown reason')}."
    if has_refund:
        summary += " A refund request is pending approval."

    # Step 6: Evaluate
    evaluation = client.call("evaluate_response", {
        "response": summary,
        "required_sources": [order["orderId"], order.get("shipmentId", "")],
        "risk_level": risk
    })

    # Step 7: Approval if required
    approval_id = None
    if has_delay and has_refund:
        approval = client.call("create_approval_request", {
            "related_record_id": order["orderId"],
            "related_record_type": "order",
            "approval_type": "Compensation",
            "reason": "Delayed shipment with pending refund",
            "risk_level": "High",
            "requested_by": "orchestrator"
        })
        approval_id = approval.get("approvalId")

    # Step 8: Cost + log
    latency_ms = int((time.time() - start) * 1000)
    model, vendor = config.AI_PRIMARY_MODEL, config.AI_PRIMARY_VENDOR

    cost = client.call("calculate_agent_run_cost", {
        "vendor": vendor, "model": model,
        "input_tokens": 1500, "output_tokens": 400
    })
    log = client.call("log_agent_run", {
        "workflow_name": "WebshopOrderSupport",
        "intent": "SummariseLatestOrderIssue",
        "model_used": model, "vendor": vendor,
        "input_tokens": 1500, "output_tokens": 400,
        "latency_ms": latency_ms,
        "tools_called": ["get_customer_by_email", "get_latest_order", "get_order_items",
                         "get_shipment_status", "get_returns_for_order", "get_refunds_for_order",
                         "search_knowledge_articles", "evaluate_response", "create_approval_request"],
        "requires_approval": approval_id is not None,
        "risk_score": evaluation.get("riskScore", 0.0),
        "quality_score": evaluation.get("qualityScore", 0.0),
        "groundedness_score": evaluation.get("groundednessScore", 0.0)
    })

    return func.HttpResponse(
        json.dumps({
            "runId": log.get("runId"),
            "customerName": customer["fullName"],
            "orderNumber": order["orderNumber"],
            "summary": summary,
            "approvalRequired": approval_id is not None,
            "approvalId": approval_id,
            "qualityScore": evaluation.get("qualityScore"),
            "groundednessScore": evaluation.get("groundednessScore"),
            "estimatedCost": cost.get("estimatedCost"),
            "modelUsed": model,
            "latencyMs": latency_ms
        }),
        mimetype="application/json",
        status_code=200
    )
```

---

## Running Locally

```bash
# Terminal 1: Azurite
azurite --silent --location C:\azurite

# Terminal 2: Azure Functions
cd apps/orchestrator-api
func start

# Terminal 3: Test
curl -X POST http://localhost:7071/api/webshop-order-support \
  -H "Content-Type: application/json" \
  -d '{"customerEmail": "john.smith@contoso.com", "userId": "user-001"}'
```

---

## LLM Summary Generation

The orchestrator now generates the support summary with Azure OpenAI.

Current project standard:

- primary enterprise provider: Azure OpenAI
- secondary provider: Gemini
- direct OpenAI is not active in this case
- Anthropic is not part of the active runtime path

Implementation:

- `apps/orchestrator-api/src/shared/azure_openai_client.py`
- deployment: `gpt-5-mini`
- API parameter: `max_completion_tokens`
- GPT-5 behavior: reasoning tokens count against the same completion token limit
- current request config: `reasoning_effort=low`

Gemini uses `GEMINI_API_KEY`; see the official key setup guide: https://ai.google.dev/gemini-api/docs/api-key

---

## Next Step

[docs/05-pulumi-infrastructure.md](05-pulumi-infrastructure.md) — Day 5: Pulumi + Azure resources.

