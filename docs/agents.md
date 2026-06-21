# Agent Definitions

All agents in the Enterprise AgentOps Control Tower. Each agent has a defined role, file path, system prompt and example output.

---

## Overview

Default active direction:
- New pro-code agents use Microsoft Agent Framework.
- The Draft Agent is intentionally the only Semantic Kernel agent, kept for comparison, didactics and legacy understanding.
- Azure OpenAI `gpt-5-mini` is the primary model for the Microsoft case.
- Gemini `gemini-3.5-flash` is the secondary comparison model.
- Anthropic/Claude is not part of the active runtime path.

| Agent | Role | Primary Model | File |
|---|---|---|---|
| Intake | Classify request, extract intent | gpt-5-mini | `agents/intake_agent.py` |
| Data | Fetch data via MCP tools | Orchestrator (no LLM) | `agents/data_agent.py` |
| Knowledge | Retrieve policy documents | Azure AI Search | `agents/knowledge_agent.py` |
| Governance | Check approval requirements | Deterministic rules first; AF later if needed | `agents/governance_agent.py` |
| Draft | Generate response summary | gpt-5-mini | `apps/orchestrator-api/src/agents/draft_agent.py` |
| Critic/Evaluator | Evaluate quality and compliance | MCP evaluation tool first; AF later if needed | `agents/critic_agent.py` |
| Cost | Track token usage and cost | No LLM — calculation | `agents/cost_agent.py` |
| Workflow | Log run, manage thread state and trigger approvals | No LLM — orchestration | `agents/workflow_agent.py` |

> **Agent surfaces:** For MVP, agents are invoked through Copilot Studio Test Chat. In the post-MVP phase, Microsoft 365 Agents SDK / Agents Playground is the custom-engine agent surface. All agents, prompts, pipelines and MCP tools are reused unchanged across both surfaces — only the entry point changes.

## Progress Logging

All agents and coding assistants working on this project must update `progress.md` at the repository root after meaningful setup, implementation, verification, decision or blocker events.

Keep entries short, chronological and factual.

## Implementation Quality Rules

Coding agents must choose the project-correct path, not the quickest local shortcut.

- Do not duplicate MCP tool names in prompts or agents when a tool registry/client can provide them.
- If an agent asks the model for `toolsRequired`, inject the exact allowed MCP tool names from the MCP client/tool registry and validate the model response against that list.
- Use typed contracts for agent outputs where practical. In Python, prefer Pydantic models and explicit parse/validation paths.
- Human-in-the-loop must be explicit: approval status, approval ID and pending workflow step are part of the workflow contract.
- Thread-based state is part of the orchestrator design. Agents that participate in multi-turn workflows should preserve `threadId` and update `ThreadState`.
- The project is moving toward an extensive typed domain model. New internal agent boundaries should prefer Pydantic contracts over loose dictionaries.
- Keep business actions behind MCP tools. Agents should not bypass the MCP layer to manipulate Dataverse, approvals, observability, or cost data directly.
- Do not add silent fallback behavior for broken integrations. Fail clearly and record the blocker in `progress.md`.
- Add focused tests for contracts, registry behavior, and orchestration boundaries when changing agent behavior.

## Code Commenting Rule

Agent code must include short step-by-step comments in English.

The comments should make the execution flow easy to follow for learning:
- validate configuration
- build the agent/kernel/client
- prepare grounded context
- call the model or tool
- validate the response
- extract telemetry/cost metadata

Avoid noisy comments that merely repeat the code.

## Thread State and Human Approval

The orchestrator now treats workflow state as an explicit object rather than implicit chat memory.

Current state model:

- `ThreadState`: stores `threadId`, workflow name, current status, customer email, intent, order ID, approval ID, current step and context.
- `GovernanceDecision`: stores risk, approval requirement, approval type, reason and trigger.
- `ApprovalOutcome`: stores approval ID/status and whether human-in-the-loop is active.

High-risk workflows must create a pending approval and return approval state to the caller. Drafts may explain that approval is pending, but agents must not present compensation or exception handling as completed until approval is resolved.

Human approval surface direction:

- Power Apps canvas app is the approval console.
- Dataverse stores the approval request records.
- Orchestrator API exposes approval list/decision endpoints for Power Apps custom connectors.
- The decision endpoint must update both the approval record and thread state.

Thread state storage direction:

- local tests/development may use the file store;
- Azure runtime should use Azure Table Storage;
- Dataverse remains for business records and audit records, not opaque conversational state blobs.

---

## Intake Agent

**Purpose:** Classify the user request and extract structured intent before any data retrieval begins. Runs first in all pipelines.

**File:** `agents/intake_agent.py`

**Model:** `gpt-5-mini` through Azure OpenAI.

**Framework:** Microsoft Agent Framework.

**System Prompt:**

```
You are an enterprise AI intake agent.
Your job is to classify incoming support requests and extract structured intent.

Output ONLY valid JSON in this format:
{
  "intent": "what the user wants to achieve",
  "businessDomain": "CustomerService | Logistics | Finance | HR | Legal",
  "urgency": "Low | Medium | High",
  "toolsRequired": ["exact", "registered", "MCP", "tool", "names"],
  "riskLevel": "Low | Medium | High",
  "approvalLikelihood": "Low | Medium | High",
  "contactEmail": "email if provided or null",
  "orderReference": "order ref if mentioned or null"
}

Do not explain. Do not include any text outside the JSON object.

For `toolsRequired`, use only exact tool names from the MCP client/tool registry.
Do not return business system names, categories, or paraphrases.
```

**Example Input:**

```
Can you check what's happening with the order for john.smith@contoso.com?
They've been waiting 2 weeks and the shipment is still showing delayed.
```

**Example Output:**

```json
{
  "intent": "SummariseLatestOrderDeliveryStatus",
  "businessDomain": "Logistics",
  "urgency": "High",
  "toolsRequired": ["get_customer_by_email", "get_latest_order", "get_shipment_status"],
  "riskLevel": "High",
  "approvalLikelihood": "Medium",
  "contactEmail": "john.smith@contoso.com",
  "orderReference": null
}
```

---

## Data Agent

**Purpose:** Execute MCP tool calls to retrieve all data needed for the pipeline. No LLM — pure orchestration.

**File:** `agents/data_agent.py`

**System Prompt:** N/A — deterministic tool execution

**Execution Flow:**

```python
async def run(self, contact_email: str) -> dict:
    customer = self.mcp.call("get_customer_by_email", {"email": contact_email})
    order = self.mcp.call("get_latest_order", {"contact_id": customer["contactId"]})
    return {
        "customer": customer,
        "order": order,
        "items": self.mcp.call("get_order_items", {"order_id": order["orderId"]}),
        "shipment": self.mcp.call("get_shipment_status", {"shipment_id": order["shipmentId"]}),
        "returns": self.mcp.call("get_returns_for_order", {"order_id": order["orderId"]}),
        "refunds": self.mcp.call("get_refunds_for_order", {"order_id": order["orderId"]})
    }
```

---

## Knowledge Agent

**Purpose:** Search enterprise policy documents to ground the response in verified policy.

**File:** `agents/knowledge_agent.py`

**Backed by:** Azure AI Search (Stage 8) or mock JSON keyword search (Stages 1–7)

**Execution:**

```python
def run(self, query: str) -> dict:
    return self.mcp.call("search_knowledge_articles", {"query": query, "max_results": 3})
```

**Example Output:**

```json
{
  "query": "delivery delay compensation approval",
  "results": [
    {
      "articleId": "ka-002",
      "title": "Delivery Delay Policy",
      "category": "Logistics",
      "summary": "Customers must be notified within 24 hours of a confirmed delay...",
      "confidence": 0.91,
      "source": "delivery-delay-policy.md"
    },
    {
      "articleId": "ka-001",
      "title": "Customer Compensation Policy",
      "category": "Customer Service",
      "summary": "Customer compensation requires approval when refund or credit exceeds...",
      "confidence": 0.87,
      "source": "customer-compensation-policy.md"
    }
  ]
}
```

---

## Governance Agent

**Purpose:** Determine whether a human approval is required before the draft can be communicated externally.

**File:** `agents/governance_agent.py`

**Model:** `gpt-5-mini` through Azure OpenAI.

**Framework:** Microsoft Agent Framework.

**System Prompt:**

```
You are an enterprise AI governance agent.
Given a customer scenario, determine if a human approval is required before communicating
any resolution or compensation externally.

Review the order status, refund requests, risk level and policy knowledge provided.
Output ONLY valid JSON:
{
  "requiresApproval": true | false,
  "reason": "brief explanation",
  "approvalType": "Compensation | Refund | Escalation | None",
  "riskLevel": "Low | Medium | High"
}
```

**Example Output:**

```json
{
  "requiresApproval": true,
  "reason": "Refund above standard threshold pending, shipment delayed 14+ days, premium account",
  "approvalType": "Compensation",
  "riskLevel": "High"
}
```

---

## Draft Agent

**Purpose:** Generate a professional, grounded summary for the support agent to review before sending to the customer.

**File:** `apps/orchestrator-api/src/agents/draft_agent.py`

**Model:** `gpt-5-mini` by default. Gemini can be used as the secondary provider.

**Framework:** Semantic Kernel. This is intentional. It is the single comparison agent kept so we can study how Semantic Kernel maps to the newer Microsoft Agent Framework direction.

**System Prompt:**

```
You are an enterprise customer support agent writing internal briefing notes.
Write a concise professional summary (3-5 sentences) based ONLY on the data provided.

Rules:
1. Never promise compensation, refunds or credits before they have been formally approved
2. If an approval is pending, say: "An approval request has been created and is awaiting
   manager sign-off before any resolution can be communicated to the customer"
3. State the order status, delivery status and any pending actions factually
4. Cite the sources used at the end: "Sources: [record IDs, document names]"
5. Do not add information not present in the provided data
```

**Example Output:**

```
John Smith's latest order (ORD-2026-8821) placed on 10 June 2026 is currently in Delayed status.
The shipment (SHIP-9001) was due for delivery on 13 June but carrier DHL reported a warehouse
sortation issue. A return request (ret-3001) and refund request (ref-4001) for £49.99 are on
record and pending approval. An approval request has been created and is awaiting manager
sign-off before any resolution can be communicated to the customer.
Sources: ord-1001, ship-9001, ret-3001, ref-4001, ka-001, ka-002
```

---

## Critic / Evaluator Agent

**Purpose:** Score the draft for quality, groundedness and policy compliance. Blocks low-quality responses from being returned.

**File:** `agents/critic_agent.py`

**Model:** `gpt-5-mini` through Azure OpenAI.

**Framework:** Microsoft Agent Framework.

**System Prompt:**

```
You are an enterprise AI quality evaluator.
Review the draft response against the source data and output ONLY valid JSON:
{
  "qualityScore": 0.0-1.0,
  "groundednessScore": 0.0-1.0,
  "riskScore": 0.0-1.0,
  "issues": ["list of specific issues if any"],
  "approvedForUser": true | false
}

approvedForUser must be false if:
- qualityScore < 0.7
- groundednessScore < 0.6
- The response promises compensation that has not been approved
- The response is shorter than 2 sentences
```

**Example Output:**

```json
{
  "qualityScore": 0.94,
  "groundednessScore": 0.91,
  "riskScore": 0.72,
  "issues": [],
  "approvedForUser": true
}
```

---

## Cost Agent

**Purpose:** Calculate estimated LLM cost from token usage. No LLM — pure arithmetic using pricing.json.

**File:** `agents/cost_agent.py`

Delegates to `calculate_agent_run_cost` MCP tool. See [docs/03-mcp-tools-extended.md](03-mcp-tools-extended.md).

**Example Output:**

```json
{
  "vendor": "OpenAI",
  "model": "gpt-5-mini",
  "inputTokens": 1800,
  "outputTokens": 450,
  "estimatedCost": 0.00144,
  "currency": "USD"
}
```

---

## Workflow Agent

**Purpose:** Log the run, write telemetry, create approval requests and update thread state after approval decisions. No LLM — pure side-effects.

**File:** `agents/workflow_agent.py`

Delegates to `log_agent_run` and `create_approval_request` MCP tools. See [docs/03-mcp-tools-extended.md](03-mcp-tools-extended.md).

---

## Microsoft Foundry (formerly Azure AI Foundry): Policy Agent

**Purpose:** A standalone RAG agent in Microsoft Foundry (formerly Azure AI Foundry) that answers governance and policy questions grounded in enterprise documents.

**Setup:** See [docs/09-agent-framework.md](09-agent-framework.md)

**System Prompt:**

```
You are an enterprise AI policy and governance agent.
Answer questions about refund policy, delivery policy, compensation rules, approval thresholds
and responsible AI guidelines.

Rules:
- Answer ONLY based on your knowledge source — never invent policy
- Cite the document name and section in every answer
- If you cannot find relevant policy, say so explicitly
- Flag any action that requires human approval

Output JSON:
{
  "answer": "...",
  "requiresApproval": true | false,
  "source": "document name and section",
  "confidence": 0.0-1.0
}
```

---

## Provider Switching

All agents that use an LLM should read provider settings from `.env`.

```python
pipeline = WebshopOrderSupportPipeline(provider="azure_openai")
secondary_pipeline = WebshopOrderSupportPipeline(provider="gemini")
```

Model mapping:

| Provider | Draft Agent | Intake / Critic / Governance |
|---|---|---|
| `azure_openai` | gpt-5-mini | gpt-5-mini |
| `gemini` | gemini-3.5-flash | gemini-3.5-flash |

See [docs/ai-azure-openai.md](ai-azure-openai.md) and [docs/ai-gemini.md](ai-gemini.md) for provider guides.
