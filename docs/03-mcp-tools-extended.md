# Stage 3: MCP Tools Extended (Day 3)

Implement the remaining tools: returns, refunds, support cases, knowledge, approvals, cost calculation, agent run logging and response evaluation.

---

## Day 3 Deliverables

- [ ] Mock data populated: returns, refunds, cases, activities, knowledge_articles, approvals, agent_runs
- [ ] `get_returns_for_order` implemented
- [ ] `get_refunds_for_order` implemented
- [ ] `get_open_cases` implemented
- [ ] `get_case_details` implemented
- [ ] `search_knowledge_articles` implemented (mock mode)
- [ ] `create_approval_request` implemented
- [ ] `create_follow_up_task` implemented
- [ ] `calculate_agent_run_cost` implemented
- [ ] `log_agent_run` implemented
- [ ] `evaluate_response` implemented
- [ ] All tools registered in server.py
- [ ] Basic tests passing

---

## Remaining Mock Data

### returns.json

```json
[
  {
    "returnId": "ret-3001",
    "orderId": "ord-1001",
    "orderItemId": "oi-001",
    "reason": "Delivery delay — product not received in time",
    "status": "Requested",
    "requestedDate": "2026-06-14T11:00:00Z",
    "approvedDate": null,
    "refundRequired": true
  }
]
```

### refunds.json

```json
[
  {
    "refundId": "ref-4001",
    "orderId": "ord-1001",
    "returnId": "ret-3001",
    "amount": 49.99,
    "status": "Pending Approval",
    "reason": "Delivery delay compensation",
    "requiresApproval": true,
    "approvedBy": null
  }
]
```

### cases.json

```json
[
  {
    "caseId": "case-1001",
    "accountId": "acc-001",
    "contactId": "con-001",
    "orderId": "ord-1001",
    "title": "Delayed shipment complaint",
    "description": "Customer reported repeated delivery delays affecting store operations.",
    "status": "Open",
    "priority": "High",
    "createdOn": "2026-06-11T09:00:00Z",
    "slaDeadline": "2026-06-18T17:00:00Z",
    "slaRisk": "High",
    "owner": "Support Team A",
    "category": "Logistics"
  }
]
```

### activities.json

```json
[
  {
    "activityId": "act-001",
    "regardingId": "case-1001",
    "regardingType": "case",
    "type": "email",
    "subject": "Initial complaint received",
    "description": "Customer reported recurring delivery failures.",
    "createdOn": "2026-06-11T09:12:00Z",
    "owner": "Support Team A"
  },
  {
    "activityId": "act-002",
    "regardingId": "case-1001",
    "regardingType": "case",
    "type": "task",
    "subject": "Carrier investigation requested",
    "description": "Internal investigation requested with carrier.",
    "createdOn": "2026-06-12T14:30:00Z",
    "owner": "Support Team A"
  }
]
```

### knowledge_articles.json

```json
[
  {
    "articleId": "ka-001",
    "title": "Customer Compensation Policy",
    "category": "Customer Service",
    "content": "Customer compensation requires approval when refund or credit exceeds the standard threshold. Compensation must be approved by a service manager before being communicated externally. Premium customers may receive up to 20% of invoice value without director sign-off.",
    "effectiveDate": "2026-01-01",
    "riskCategory": "Medium"
  },
  {
    "articleId": "ka-002",
    "title": "Delivery Delay Policy",
    "category": "Logistics",
    "content": "Customers must be notified within 24 hours of a confirmed delivery delay. High-risk delays affecting priority customers require escalation to the service owner. Compensation eligibility begins after 48 hours of confirmed delay.",
    "effectiveDate": "2026-01-01",
    "riskCategory": "High"
  },
  {
    "articleId": "ka-003",
    "title": "Refund Policy",
    "category": "Finance",
    "content": "Refunds below £50 can be approved by team leads. Refunds above £50 require service manager approval. All refunds must be logged with a reason code before processing.",
    "effectiveDate": "2026-01-01",
    "riskCategory": "Medium"
  }
]
```

### approvals.json + agent_runs.json

```json
[]
```

---

## Tool: Returns and Refunds

**File:** `mcp-server/src/enterprise_agentops_mcp/tools/returns.py`

```python
from fastmcp import FastMCP
from enterprise_agentops_mcp.services.mock_data_service import load
from enterprise_agentops_mcp.config import DATA_MODE

router = FastMCP()

@router.tool()
def get_returns_for_order(order_id: str) -> dict:
    """Retrieve return requests linked to an order."""
    if DATA_MODE == "mock":
        returns = load("returns.json")
        return {"orderId": order_id, "returns": [r for r in returns if r["orderId"] == order_id]}
    raise NotImplementedError("Dataverse mode not yet implemented — see Stage 7")

@router.tool()
def get_refunds_for_order(order_id: str) -> dict:
    """Retrieve refund records linked to an order."""
    if DATA_MODE == "mock":
        refunds = load("refunds.json")
        return {"orderId": order_id, "refunds": [r for r in refunds if r["orderId"] == order_id]}
    raise NotImplementedError("Dataverse mode not yet implemented — see Stage 7")
```

---

## Tool: Support Cases

**File:** `mcp-server/src/enterprise_agentops_mcp/tools/cases.py`

```python
from fastmcp import FastMCP
from enterprise_agentops_mcp.services.mock_data_service import load
from enterprise_agentops_mcp.config import DATA_MODE

router = FastMCP()

@router.tool()
def get_open_cases(account_id: str) -> dict:
    """Retrieve all open support cases for an account."""
    if DATA_MODE == "mock":
        cases = load("cases.json")
        open_cases = [c for c in cases if c["accountId"] == account_id and c["status"] == "Open"]
        return {"accountId": account_id, "openCases": open_cases}
    raise NotImplementedError("Dataverse mode not yet implemented — see Stage 7")

@router.tool()
def get_case_details(case_id: str) -> dict:
    """Retrieve full support case details including activities."""
    if DATA_MODE == "mock":
        cases = load("cases.json")
        activities = load("activities.json")
        case = next((c for c in cases if c["caseId"] == case_id), None)
        if not case:
            return {"error": f"Case not found: {case_id}"}
        return {**case, "activities": [a for a in activities if a["regardingId"] == case_id]}
    raise NotImplementedError("Dataverse mode not yet implemented — see Stage 7")
```

---

## Tool: Knowledge Search

**File:** `mcp-server/src/enterprise_agentops_mcp/tools/knowledge.py`

```python
from fastmcp import FastMCP
from enterprise_agentops_mcp.services.mock_data_service import load
from enterprise_agentops_mcp.config import DATA_MODE

router = FastMCP()

@router.tool()
def search_knowledge_articles(query: str, max_results: int = 3) -> dict:
    """Search internal policy documents and knowledge articles."""
    if DATA_MODE == "mock":
        articles = load("knowledge_articles.json")
        query_lower = query.lower()
        results = [
            {
                "articleId": a["articleId"],
                "title": a["title"],
                "category": a["category"],
                "summary": a["content"][:300],
                "confidence": 0.85,
                "source": a["title"]
            }
            for a in articles
            if query_lower in a["content"].lower() or query_lower in a["title"].lower()
        ]
        return {"query": query, "results": results[:max_results]}

    from enterprise_agentops_mcp.services.azure_search_service import search_knowledge
    return {"query": query, "results": search_knowledge(query, max_results)}
```

---

## Tool: Approvals and Tasks

**File:** `mcp-server/src/enterprise_agentops_mcp/tools/approvals.py`

```python
import uuid
from datetime import datetime, timezone
from fastmcp import FastMCP
from enterprise_agentops_mcp.services.mock_data_service import load, save
from enterprise_agentops_mcp.config import DATA_MODE, POWER_AUTOMATE_APPROVAL_URL

router = FastMCP()

@router.tool()
def create_approval_request(
    related_record_id: str,
    related_record_type: str,
    approval_type: str,
    reason: str,
    risk_level: str,
    requested_by: str = "agent"
) -> dict:
    """Create a human approval request for high-risk or sensitive actions."""
    approval_id = f"apr-{str(uuid.uuid4())[:4]}"
    approval = {
        "approvalId": approval_id,
        "relatedRecordId": related_record_id,
        "relatedRecordType": related_record_type,
        "requestedBy": requested_by,
        "approvalType": approval_type,
        "status": "Pending",
        "riskLevel": risk_level,
        "reason": reason,
        "createdOn": datetime.now(timezone.utc).isoformat(),
        "approvedBy": None
    }

    if DATA_MODE == "mock":
        approvals = load("approvals.json")
        approvals.append(approval)
        save("approvals.json", approvals)

    if POWER_AUTOMATE_APPROVAL_URL:
        import httpx
        try:
            httpx.post(POWER_AUTOMATE_APPROVAL_URL, json=approval, timeout=5)
        except Exception:
            pass  # Non-blocking

    return {
        "approvalId": approval_id,
        "status": "Pending",
        "relatedRecordId": related_record_id,
        "riskLevel": risk_level,
        "createdOn": approval["createdOn"]
    }

@router.tool()
def create_follow_up_task(
    related_record_id: str,
    related_record_type: str,
    subject: str,
    due_date: str,
    owner: str
) -> dict:
    """Create a follow-up task linked to a record."""
    return {
        "taskId": f"task-{str(uuid.uuid4())[:4]}",
        "status": "Created",
        "subject": subject,
        "dueDate": due_date,
        "owner": owner,
        "relatedRecordId": related_record_id
    }
```

---

## Tool: Cost Calculation

**File:** `mcp-server/src/enterprise_agentops_mcp/tools/cost.py`

```python
from fastmcp import FastMCP
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()

@router.tool()
def calculate_agent_run_cost(vendor: str, model: str, input_tokens: int, output_tokens: int) -> dict:
    """Calculate estimated LLM cost from token usage and model pricing."""
    pricing = load("pricing.json")
    rate = next((p for p in pricing if p["vendor"] == vendor and p["model"] == model), None)
    if not rate:
        return {"error": f"No pricing data found for {vendor}/{model}"}

    total = round(
        (input_tokens / 1_000_000) * rate["inputTokenPricePer1M"] +
        (output_tokens / 1_000_000) * rate["outputTokenPricePer1M"],
        6
    )
    return {
        "vendor": vendor, "model": model,
        "inputTokens": input_tokens, "outputTokens": output_tokens,
        "estimatedCost": total, "currency": rate["currency"]
    }
```

---

## Tool: Agent Run Logging

**File:** `mcp-server/src/enterprise_agentops_mcp/tools/observability.py`

```python
import uuid
from datetime import datetime, timezone
from fastmcp import FastMCP
from enterprise_agentops_mcp.services.mock_data_service import load, save
from enterprise_agentops_mcp.tools.cost import calculate_agent_run_cost

router = FastMCP()

@router.tool()
def log_agent_run(
    workflow_name: str, intent: str, model_used: str, vendor: str,
    input_tokens: int, output_tokens: int, latency_ms: int, tools_called: list[str],
    requires_approval: bool = False, risk_score: float = 0.0,
    quality_score: float = 0.0, groundedness_score: float = 0.0
) -> dict:
    """Log agent execution telemetry for observability and cost tracking."""
    cost_result = calculate_agent_run_cost(vendor, model_used, input_tokens, output_tokens)
    estimated_cost = cost_result.get("estimatedCost", 0.0)
    run_id = f"run-{str(uuid.uuid4())[:8]}"

    run = {
        "runId": run_id, "workflowName": workflow_name, "intent": intent,
        "modelUsed": model_used, "vendorUsed": vendor,
        "startedAt": datetime.now(timezone.utc).isoformat(), "status": "Completed",
        "inputTokens": input_tokens, "outputTokens": output_tokens,
        "estimatedCost": estimated_cost, "latencyMs": latency_ms,
        "toolsCalled": tools_called, "requiresApproval": requires_approval,
        "riskScore": risk_score, "qualityScore": quality_score,
        "groundednessScore": groundedness_score
    }

    runs = load("agent_runs.json")
    runs.append(run)
    save("agent_runs.json", runs)

    return {"logged": True, "runId": run_id, "estimatedCost": estimated_cost}
```

---

## Tool: Response Evaluation

**File:** `mcp-server/src/enterprise_agentops_mcp/tools/evaluation.py`

```python
from fastmcp import FastMCP

router = FastMCP()

@router.tool()
def evaluate_response(response: str, required_sources: list[str], risk_level: str = "Medium") -> dict:
    """Evaluate a generated response for quality, groundedness and policy compliance."""
    issues = []
    if len(response.strip()) < 50:
        issues.append("Response is too short to be useful.")
    if risk_level == "High" and "approval" not in response.lower():
        issues.append("High-risk response must mention that approval is required before actioning.")
    if not required_sources:
        issues.append("No source references provided — groundedness cannot be confirmed.")

    return {
        "qualityScore": round(max(0.3, 0.92 - len(issues) * 0.12), 2),
        "groundednessScore": 0.88 if required_sources else 0.55,
        "riskScore": {"Low": 0.2, "Medium": 0.5, "High": 0.82}.get(risk_level, 0.5),
        "issues": issues,
        "approvedForUser": len(issues) == 0
    }
```

---

## Updated server.py

```python
from fastmcp import FastMCP

mcp = FastMCP("enterprise-agentops-mcp-server")

from enterprise_agentops_mcp.tools.customers import router as customers_router
from enterprise_agentops_mcp.tools.accounts import router as accounts_router
from enterprise_agentops_mcp.tools.orders import router as orders_router
from enterprise_agentops_mcp.tools.shipments import router as shipments_router
from enterprise_agentops_mcp.tools.returns import router as returns_router
from enterprise_agentops_mcp.tools.cases import router as cases_router
from enterprise_agentops_mcp.tools.knowledge import router as knowledge_router
from enterprise_agentops_mcp.tools.approvals import router as approvals_router
from enterprise_agentops_mcp.tools.cost import router as cost_router
from enterprise_agentops_mcp.tools.observability import router as observability_router
from enterprise_agentops_mcp.tools.evaluation import router as evaluation_router

for r in [customers_router, accounts_router, orders_router, shipments_router,
          returns_router, cases_router, knowledge_router, approvals_router,
          cost_router, observability_router, evaluation_router]:
    mcp.include_router(r)

if __name__ == "__main__":
    mcp.run()
```

---

## Tests

```bash
cd mcp-server
uv run pytest tests/ -v
```

Sample test:

```python
# tests/test_orders.py
from enterprise_agentops_mcp.tools.orders import get_latest_order, get_order_items

def test_get_latest_order_found():
    result = get_latest_order("con-001")
    assert result["orderId"] == "ord-1001"
    assert result["deliveryStatus"] == "Delayed"

def test_get_latest_order_not_found():
    result = get_latest_order("con-999")
    assert "error" in result

def test_get_order_items():
    result = get_order_items("ord-1001")
    assert len(result["items"]) == 2
    assert result["items"][0]["productName"] == "Premium Coffee Machine"
```

---

## Next Step

[docs/04-orchestrator-api.md](04-orchestrator-api.md) — Day 4: Azure Function Orchestrator API.
