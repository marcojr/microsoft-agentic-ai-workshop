# Stage 9: Microsoft Agent Framework + Copilot Studio (Day 9)

Move the manual orchestration toward Microsoft Agent Framework, the modern Microsoft pro-code agent framework.

Semantic Kernel stays in the project on purpose for exactly one agent: the Draft Agent. This gives us a practical comparison point, shows the evolution path, and keeps legacy understanding visible without making the whole project depend on the older style.

Reference names:
- Microsoft Agent Framework: current strategic framework, successor to Semantic Kernel + AutoGen.
- Semantic Kernel: still a valid SDK/package, used here only by the Draft Agent comparison track.
- Microsoft Foundry (formerly Azure AI Foundry): managed agent and model platform.

Official docs:
- Microsoft Agent Framework overview: https://learn.microsoft.com/en-us/agent-framework/overview/
- Migration from Semantic Kernel: https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-semantic-kernel/
- Microsoft Foundry overview: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

---

## Day 9 Deliverables

- [x] Semantic Kernel installed and configured for the Draft Agent comparison track
- [ ] MCP tools registered for Microsoft Agent Framework
- [x] Intake Agent classifying requests with Microsoft Agent Framework
- [x] Data Agent retrieving data via MCP tools
- [x] Knowledge Agent using Secure RAG through MCP
- [x] Governance Agent checking approval requirements with deterministic rules
- [x] Draft Agent generating summaries with Azure OpenAI through Semantic Kernel
- [x] Critic Agent evaluating the draft through the MCP evaluation tool
- [x] Cost Agent calculating token cost through MCP
- [x] Workflow Agent managing approval, thread state, run logging and events
- [x] Full WebshopOrderSupport pipeline running end-to-end
- [ ] Copilot Studio agent created in test chat
- [ ] Copilot Studio HTTP action calling Orchestrator API
- [ ] Screenshot of agent working

---

## Install Agent SDKs

Semantic Kernel is installed because the Draft Agent intentionally uses it for comparison.

```powershell
cd apps/orchestrator-api
uv pip install --python .\.venv\Scripts\python.exe -r requirements.txt
```

---

## Semantic Kernel Comparison Agent

**Current file:** `apps/orchestrator-api/src/agents/draft_agent.py`

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings

def build_draft_kernel() -> Kernel:
    kernel = Kernel()
    kernel.add_service(AzureChatCompletion(
        service_id="azure-openai",
        deployment_name="gpt-5-mini",
        endpoint="AZURE_OPENAI_ENDPOINT",
        api_key="AZURE_OPENAI_API_KEY",
        api_version="2024-10-21",
    ))
    return kernel
```

Current GPT-5 execution settings:

```python
AzureChatPromptExecutionSettings(
    service_id="azure-openai",
    max_completion_tokens=1600,
    reasoning_effort="low",
)
```

Important: GPT-5 uses `max_completion_tokens`; `max_tokens` is rejected.

---

## Microsoft Agent Framework Direction

The remaining agents should be implemented with Microsoft Agent Framework:

- Intake Agent: classify the request and extract intent.
- Data Agent: call MCP tools deterministically.
- Knowledge Agent: call Azure AI Search through the MCP tool layer.
- Governance Agent: decide whether approval is required.
- Critic Agent: evaluate quality, groundedness and policy risk.
- Workflow Agent: log the run and publish approval/event messages.

The important comparison:

| Area | Draft Agent | New Agents |
|---|---|---|
| Framework | Semantic Kernel | Microsoft Agent Framework |
| Purpose | Legacy/comparison/didactic | Modern project direction |
| Model | Azure OpenAI `gpt-5-mini` | Azure OpenAI `gpt-5-mini` by default |
| Why keep it | Understand what came before | Build the current architecture |

---

## Implementation Rules for Coding Agents

Prefer the correct project architecture over quick local shortcuts.

- MCP tool names must come from the MCP client/tool registry, not from duplicated prompt literals.
- Agent prompts may receive an injected allowed-tool list, but the source of that list must be code-owned and testable.
- `toolsRequired` must contain exact registered MCP tool names only. Do not let the model return business system names such as "Customer Database" or "Shipment Tracking".
- Agent outputs should use typed response contracts where practical. In the current Python path, use Pydantic models and explicit validation.
- Keep Dataverse, approvals, observability, cost, and knowledge retrieval behind MCP tools unless the stage explicitly documents a lower-level integration task.
- Avoid silent fallbacks. If the selected framework, Azure OpenAI API version, MCP integration, or response contract fails, surface the failure and record it in `progress.md`.
- Treat human-in-the-loop as explicit state. Approval status and pending workflow step must be visible in the orchestrator response and thread state.
- Preserve `threadId` for multi-turn workflows and approval continuations.
- Move internal agent contracts toward Pydantic models as boundaries become stable.

---

## Updated Direction: HITL, Thread State, Type Safety

The Stage 9 implementation now includes the first production-shaped building blocks for enterprise agent workflows:

- Human-in-the-loop approval is represented by `ApprovalOutcome`, not just an approval tool side effect.
- Thread-based state is represented by `ThreadState`. Local development can use the file store; Azure runtime should use Azure Table Storage.
- Type safety is represented by Pydantic contracts for LLM outputs and workflow decisions.
- The orchestrator composes specialized agents rather than directly calling every MCP tool inline.

Current sequence:

```text
IntakeAgent -> DataAgent -> GovernanceAgent -> KnowledgeAgent -> DraftAgent -> CriticAgent -> CostAgent -> WorkflowAgent
```

AutoGen remains a conceptual predecessor. The active runtime direction stays Microsoft Agent Framework plus deterministic MCP-backed agents, with exactly one Semantic Kernel comparison agent.

Thread-state storage decision:

```text
Azure Table Storage = runtime thread state
Dataverse = business/audit records
Blob Storage = optional large snapshots/debug traces
Cosmos DB = not part of the current architecture
```

---

## MCP Plugin Pattern

**File:** `agents/plugins/mcp_plugin.py`

```python
import json
from semantic_kernel.functions import kernel_function

class EnterpriseMCPPlugin:
    """Exposes MCP tools as agent-callable functions."""

    @kernel_function(description="Find a customer by email address")
    def get_customer(self, email: str) -> str:
        from enterprise_agentops_mcp.tools.customers import get_customer_by_email
        return json.dumps(get_customer_by_email(email))

    @kernel_function(description="Get the latest order for a contact")
    def get_latest_order(self, contact_id: str) -> str:
        from enterprise_agentops_mcp.tools.orders import get_latest_order
        return json.dumps(get_latest_order(contact_id))

    @kernel_function(description="Get order line items")
    def get_order_items(self, order_id: str) -> str:
        from enterprise_agentops_mcp.tools.orders import get_order_items
        return json.dumps(get_order_items(order_id))

    @kernel_function(description="Get shipment status and tracking")
    def get_shipment(self, shipment_id: str) -> str:
        from enterprise_agentops_mcp.tools.shipments import get_shipment_status
        return json.dumps(get_shipment_status(shipment_id))

    @kernel_function(description="Get return requests for an order")
    def get_returns(self, order_id: str) -> str:
        from enterprise_agentops_mcp.tools.returns import get_returns_for_order
        return json.dumps(get_returns_for_order(order_id))

    @kernel_function(description="Get refund records for an order")
    def get_refunds(self, order_id: str) -> str:
        from enterprise_agentops_mcp.tools.returns import get_refunds_for_order
        return json.dumps(get_refunds_for_order(order_id))

    @kernel_function(description="Search enterprise policy and knowledge articles")
    def search_knowledge(self, query: str) -> str:
        from enterprise_agentops_mcp.tools.knowledge import search_knowledge_articles
        return json.dumps(search_knowledge_articles(query))

    @kernel_function(description="Create a human approval request")
    def create_approval(self, related_record_id: str, related_record_type: str,
                        approval_type: str, reason: str, risk_level: str) -> str:
        from enterprise_agentops_mcp.tools.approvals import create_approval_request
        return json.dumps(create_approval_request(
            related_record_id, related_record_type,
            approval_type, reason, risk_level, "agent"
        ))

    @kernel_function(description="Evaluate a response for quality and policy compliance")
    def evaluate(self, response: str, required_sources: list[str], risk_level: str) -> str:
        from enterprise_agentops_mcp.tools.evaluation import evaluate_response
        return json.dumps(evaluate_response(response, required_sources, risk_level))
```

---

## Agent Prompts

**File:** `agents/prompts.py`

```python
INTAKE_PROMPT = """
You are an enterprise AI intake agent.
Classify the user request and output JSON:
{
  "intent": "what the user wants",
  "businessDomain": "CustomerService | Logistics | Finance | HR | Legal",
  "urgency": "Low | Medium | High",
  "toolsRequired": ["exact registered MCP tool names only"],
  "riskLevel": "Low | Medium | High",
  "approvalLikelihood": "Low | Medium | High"
}
Only output valid JSON. No explanations.
Use only tool names from the MCP client/tool registry for toolsRequired.
"""

DRAFT_PROMPT = """
You are an enterprise customer support agent.
Write a concise professional summary (3-5 sentences) based only on provided data.
Rules:
- Never promise compensation before it has been approved
- If approval is required, say: "An approval request has been created and must be confirmed before any compensation is communicated"
- Cite data sources at the end (e.g., "Sources: ord-1001, ship-9001, ka-001")
"""

CRITIC_PROMPT = """
You are an enterprise AI quality evaluator.
Review the draft and output JSON:
{
  "qualityScore": 0.0-1.0,
  "groundednessScore": 0.0-1.0,
  "issues": ["list of specific problems"],
  "approvedForUser": true | false
}
Output only valid JSON.
"""
```

---

## Full Pipeline: Webshop Order Support

**File:** `agents/pipelines/webshop_pipeline.py`

```python
import json, time
from agents.kernel_setup import build_kernel
from agents.plugins.mcp_plugin import EnterpriseMCPPlugin
from agents.prompts import DRAFT_PROMPT

async def run_webshop_pipeline(customer_email: str, provider: str = "azure_openai") -> dict:
    start = time.time()
    kernel = build_kernel(provider)
    plugin = EnterpriseMCPPlugin()
    kernel.add_plugin(plugin, plugin_name="enterprise")

    # 1. Resolve customer
    customer = json.loads(plugin.get_customer(customer_email))
    if "error" in customer:
        return customer

    # 2. Get order and details
    order = json.loads(plugin.get_latest_order(customer["contactId"]))
    if "error" in order:
        return order

    items = json.loads(plugin.get_order_items(order["orderId"]))
    shipment = json.loads(plugin.get_shipment(order["shipmentId"]))
    returns = json.loads(plugin.get_returns(order["orderId"]))
    refunds = json.loads(plugin.get_refunds(order["orderId"]))
    knowledge = json.loads(plugin.search_knowledge("delivery delay compensation refund approval"))

    # 3. Draft with LLM through the Semantic Kernel comparison agent
    from semantic_kernel.agents import ChatCompletionAgent
    from semantic_kernel.contents import ChatHistory

    draft_agent = ChatCompletionAgent(kernel=kernel, name="DraftAgent", instructions=DRAFT_PROMPT)
    history = ChatHistory()
    history.add_user_message(f"""
Customer: {json.dumps(customer)}
Order: {json.dumps(order)}
Items: {json.dumps(items)}
Shipment: {json.dumps(shipment)}
Returns: {json.dumps(returns)}
Refunds: {json.dumps(refunds)}
Policy: {json.dumps(knowledge)}

Write the summary.
""")
    draft = (await draft_agent.get_response(history)).content

    # 4. Evaluate
    has_high_risk = order.get("riskLevel") == "High"
    evaluation = json.loads(plugin.evaluate(
        draft, [order["orderId"], order.get("shipmentId", "")],
        "High" if has_high_risk else "Medium"
    ))

    # 5. Approval
    approval_id = None
    has_refund_pending = any(r.get("requiresApproval") for r in refunds.get("refunds", []))
    if has_refund_pending or has_high_risk:
        approval = json.loads(plugin.create_approval(
            order["orderId"], "order",
            "Compensation", "Delayed shipment with pending refund", "High"
        ))
        approval_id = approval.get("approvalId")

    # 6. Cost + log
    latency_ms = int((time.time() - start) * 1000)
    model = os.getenv("AI_PRIMARY_MODEL", "gpt-5-mini")
    vendor = os.getenv("AI_PRIMARY_VENDOR", "Azure OpenAI")

    from enterprise_agentops_mcp.tools.cost import calculate_agent_run_cost
    from enterprise_agentops_mcp.tools.observability import log_agent_run

    cost = calculate_agent_run_cost(vendor, model, 1800, 450)
    log = log_agent_run(
        workflow_name="WebshopOrderSupport", intent="SummariseLatestOrderIssue",
        model_used=model, vendor=vendor, input_tokens=1800, output_tokens=450,
        latency_ms=latency_ms,
        tools_called=["get_customer_by_email", "get_latest_order", "get_order_items",
                      "get_shipment_status", "get_returns_for_order", "get_refunds_for_order",
                      "search_knowledge_articles", "evaluate_response", "create_approval_request"],
        requires_approval=approval_id is not None,
        risk_score=evaluation.get("riskScore", 0.0),
        quality_score=evaluation.get("qualityScore", 0.0),
        groundedness_score=evaluation.get("groundednessScore", 0.0)
    )

    return {
        "runId": log["runId"],
        "customerName": customer["fullName"],
        "orderNumber": order["orderNumber"],
        "summary": draft,
        "approvalRequired": approval_id is not None,
        "approvalId": approval_id,
        "qualityScore": evaluation.get("qualityScore"),
        "estimatedCost": cost.get("estimatedCost"),
        "modelUsed": model,
        "latencyMs": latency_ms
    }
```

---

## Copilot Studio: Create the Agent

> **VS Code extension:** Install `ms-powerplatform.vscode-powerplatform` (Power Platform Tools) to author and inspect Copilot Studio agents without leaving VS Code.

1. Go to https://copilotstudio.microsoft.com
2. **Agents** -> **New agent**
3. Name: `AgentOps Support Agent`
4. Description: _Enterprise support operations agent for approval review, policy lookup and agentic workflow coordination._
5. Instructions:

```text
You are an enterprise support operations agent. Help users review pending approval requests,
understand customer/order risk context, and decide whether approvals should be accepted or
rejected. Use available tools when approval data is needed. Be concise and ask for
clarification when required.
```

The current validated Copilot Studio integration uses **Tools** as the main extension point.

### Tools: Approval Console Connector

Add the existing Power Platform Custom Connector as tools:

```text
Agent -> Tools -> Add a tool -> Connector -> AgentOps Approval Console
```

Add these operations:

- `ListPendingApprovals`
- `SubmitApprovalDecision`

For `SubmitApprovalDecision`, configure input descriptions:

```text
approvalId: The approval request ID to approve or reject. Example: apr-4874e82a.
decision: The decision to apply. Must be exactly Approved or Rejected.
approvedBy: Email address of the human approver. Use the current user's email when available.
comment: Short explanation for the approval or rejection decision.
threadId: Workflow thread ID linked to the approval. If unknown, use the threadId from the approval request.
```

Keep inputs filled by AI for the first workshop version.

If the tool settings expose credential behavior, use maker-provided credentials for the workshop connection.

### Verified Test Prompts

Approval list:

```text
List the current pending approvals and summarize the risk.
```

Approval decision:

```text
Approve approval apr-4874e82a because the delayed shipment compensation is valid and the refund amount is within policy.
```

### Topic: Order Support

Trigger phrases:
- _Find the latest order for [email]_
- _Check delivery status for [customer]_
- _Summarise the order situation for [email]_

Flow:
```
[Ask] What is the customer email address? → {customerEmail}
[Action] Call Webshop Order Support API
[Message] {summary}
[Condition] If approvalRequired == true
  [Message] Approval request created. ID: {approvalId}
[Message] Quality score: {qualityScore} | Estimated cost: ${estimatedCost}
```

### HTTP Action

- Status: deferred.
- The first Copilot Studio integration uses the Power Platform Custom Connector tools above.
- A later endpoint/tool can expose `POST /api/agents/webshop/order-support` directly for order-support conversations.

---

## Microsoft Foundry (formerly Azure AI Foundry): Policy Agent

1. Go to https://ai.azure.com
2. Create **Agent**: _Policy and Governance Agent_
3. System prompt:

```
You are an enterprise AI policy and governance agent.
Answer questions about refund policy, delivery policy, compensation rules and approval requirements.
Answer ONLY based on your knowledge source. Cite document name and section.
Output JSON: { "answer": "...", "requiresApproval": true/false, "source": "...", "confidence": 0.0-1.0 }
```

4. Knowledge source: Azure AI Search index `enterprise-knowledge`
5. Note the agent ID for calling from the Orchestrator

---

---

## Post-MVP: Microsoft 365 Agents SDK

Microsoft 365 Agents SDK is not part of the Day 9 deliverables. It is a post-MVP phase.

The same Azure Function Orchestrator API, Microsoft Agent Framework orchestration and Enterprise AgentOps MCP Server will be reused. The M365 agent surface replaces Copilot Studio as the entry point without changing anything below it.

Initial testing is done through **Microsoft 365 Agents Playground**. Optional Teams deployment follows if a suitable developer tenant is available.

See `apps/m365-agent/` in the repository structure.

---

## Next Step

[docs/10-observability-polish.md](10-observability-polish.md) — Day 10: observability, cost dashboard, demo polish.
