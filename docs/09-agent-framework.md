# Stage 9: Microsoft Agent Framework + Copilot Studio (Day 9)

Move the manual orchestration toward Microsoft Agent Framework, the modern Microsoft pro-code agent framework.

The Draft Agent was migrated to Microsoft Agent Framework so every pro-code agent now follows the same direction.

Reference names:
- Microsoft Agent Framework: current strategic pro-code agent framework.
- Microsoft Foundry (formerly Azure AI Foundry): managed agent and model platform.

Official docs:
- Microsoft Agent Framework overview: https://learn.microsoft.com/en-us/agent-framework/overview/
- Microsoft Foundry overview: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry

---

## Day 9 Deliverables

- [x] Shared Azure OpenAI runtime helper for Microsoft Agent Framework agents
- [x] Intake Agent classifying requests with Microsoft Agent Framework
- [x] Data Agent retrieving data via MCP tools
- [x] Knowledge Agent using Secure RAG through MCP
- [x] Governance Agent checking approval requirements with deterministic rules
- [x] Draft Agent generating summaries with Microsoft Agent Framework
- [x] Critic Agent evaluating the draft through the MCP evaluation tool
- [x] Cost Agent calculating token cost through MCP
- [x] Workflow Agent managing approval, thread state, run logging and events
- [x] Full WebshopOrderSupport pipeline running end-to-end
- [x] Copilot Studio agent created and validated with connector tools

---

## Install Agent SDKs

```powershell
cd apps/orchestrator-api
uv pip install --python .\.venv\Scripts\python.exe -r requirements.txt
```

---

## Microsoft Agent Framework Runtime

**Runtime helper:** `apps/orchestrator-api/src/shared/agent_runtime.py`

The runtime helper validates Azure OpenAI configuration and builds the `AzureOpenAIChatClient` used by Microsoft Agent Framework agents.

```python
runtime = AzureOpenAIAgentRuntime()
client = runtime.build_agent_framework_client()
```

Important: GPT-5 deployments use the Azure OpenAI deployment name configured in `AZURE_OPENAI_DEPLOYMENT_NAME`.

---

## Draft Agent

**Current file:** `apps/orchestrator-api/src/agents/draft_agent.py`

The Draft Agent now uses Microsoft Agent Framework directly:

```python
agent = ChatAgent(
    chat_client=runtime.build_agent_framework_client(),
    name="DraftAgent",
    instructions=instructions,
    response_format=DraftSummaryContract,
)
```

It returns a typed `DraftSummaryContract`:

```json
{
  "summary": "string",
  "approvalRequired": true
}
```

---

## Active Agent Direction

All active pro-code agents use Microsoft Agent Framework or deterministic MCP-backed execution.

| Agent | Runtime |
|---|---|
| Intake Agent | Microsoft Agent Framework |
| Data Agent | Deterministic MCP calls |
| Knowledge Agent | MCP + Azure AI Search |
| Governance Agent | Deterministic rules first |
| Draft Agent | Microsoft Agent Framework |
| Critic Agent | MCP evaluation tool |
| Cost Agent | MCP cost tool |
| Workflow Agent | Deterministic orchestration |

---

## Implementation Rules for Coding Agents

Prefer the correct project architecture over quick local shortcuts.

- MCP tool names must come from the MCP client/tool registry, not from duplicated prompt literals.
- Agent prompts may receive an injected allowed-tool list, but the source of that list must be code-owned and testable.
- `toolsRequired` must contain exact registered MCP tool names only.
- Agent outputs should use typed response contracts where practical.
- Keep Dataverse, approvals, observability, cost, and knowledge retrieval behind MCP tools unless the stage explicitly documents a lower-level integration task.
- Avoid silent fallbacks. If the selected framework, Azure OpenAI API version, MCP integration, or response contract fails, surface the failure and record it in `progress.md`.
- Treat human-in-the-loop as explicit state. Approval status and pending workflow step must be visible in the orchestrator response and thread state.
- Preserve `threadId` for multi-turn workflows and approval continuations.
- Move internal agent contracts toward Pydantic models as boundaries become stable.

---

## Updated Direction: HITL, Thread State, Type Safety

The Stage 9 implementation includes production-shaped building blocks for enterprise agent workflows:

- Human-in-the-loop approval is represented by `ApprovalOutcome`.
- Thread-based state is represented by `ThreadState`.
- Type safety is represented by Pydantic contracts for LLM outputs and workflow decisions.
- The orchestrator composes specialized agents rather than directly calling every MCP tool inline.

Current sequence:

```text
IntakeAgent -> DataAgent -> GovernanceAgent -> KnowledgeAgent -> DraftAgent -> CriticAgent -> CostAgent -> WorkflowAgent
```

Thread-state storage decision:

```text
Azure Table Storage = runtime thread state
Dataverse = business/audit records
Blob Storage = optional large snapshots/debug traces
Cosmos DB = not part of the current architecture
```

---

## Copilot Studio: Create the Agent

The current validated Copilot Studio integration uses **Tools** as the main extension point.

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

### Verified Test Prompts

```text
List the current pending approvals and summarize the risk.
```

```text
Approve approval apr-4874e82a because the delayed shipment compensation is valid and the refund amount is within policy.
```

---

## Microsoft Foundry (formerly Azure AI Foundry): Policy Agent

1. Go to https://ai.azure.com
2. Create **Agent**: _Policy and Governance Agent_
3. System prompt:

```text
You are an enterprise AI policy and governance agent.
Answer questions about refund policy, delivery policy, compensation rules and approval requirements.
Answer ONLY based on your knowledge source. Cite document name and section.
Output JSON: { "answer": "...", "requiresApproval": true/false, "source": "...", "confidence": 0.0-1.0 }
```

4. Knowledge source: Azure AI Search index `enterprise-knowledge`
5. Note the agent ID for calling from the Orchestrator

---

## Post-MVP: Microsoft 365 Agents SDK

Microsoft 365 Agents SDK is not part of the Day 9 deliverables. It is a post-MVP phase.

The same Azure Function Orchestrator API, Microsoft Agent Framework orchestration and Enterprise AgentOps MCP Server will be reused. The M365 agent surface replaces Copilot Studio as the entry point without changing anything below it.

---

## Next Step

[docs/10-observability-polish.md](10-observability-polish.md) — Day 10: observability, cost dashboard, demo polish.
