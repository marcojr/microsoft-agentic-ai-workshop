# Change of Direction

## Summary

The project direction has expanded from a basic agent/tool orchestration demo into a more enterprise-shaped agent workflow architecture.

The new direction explicitly adopts:

- Human in the loop
- Thread-based state management
- Type safety
- A richer domain/workflow model

This does not replace the existing Microsoft Agentic AI architecture. It sharpens it.

## Why This Changed

The initial implementation proved the basic path:

```text
Request -> Orchestrator -> MCP tools -> Draft response -> Evaluation -> Logging
```

That was useful, but not enough for an enterprise agent architecture. Real enterprise workflows need continuation, auditability, approvals, typed contracts and explicit state.

The delayed-order scenario is naturally stateful:

- a user asks about an order
- the system retrieves data and policy
- compensation/refund may require manager approval
- the user may come back later asking about the same case
- the system must know whether approval is pending, approved or rejected

So the architecture now treats workflow state and human approval as first-class concepts.

## Decisions

## 1. Human in the Loop Is First-Class

Human approval is no longer treated as just a side-effect tool call.

The workflow now has an explicit approval outcome:

```text
approvalId
approvalStatus
humanInTheLoop
toolsCalled
```

High-risk actions such as compensation, exception refunds and escalation must create approval state and must not be communicated externally as completed while approval is pending.

Current code:

- `apps/orchestrator-api/src/agents/workflow_agent.py`
- `apps/orchestrator-api/src/agents/models.py`

Approval UX direction:

- Power Apps canvas app is the primary browser-based approval console.
- Dataverse stores `cr_approvalrequest` business/audit records.
- Orchestrator API exposes approval list and decision endpoints for Power Apps custom connectors.
- Azure Table Storage remains the technical thread-state store; Power Apps must not update it directly.

Current approval endpoints:

- `GET /api/approvals/pending`
- `POST /api/approvals/decision`

## 2. Thread-Based State Management

The orchestrator now supports thread-aware workflow state.

The caller can provide a `threadId`, or the system creates one. The thread state records:

- workflow name
- customer email
- intent
- order ID
- approval ID
- current step
- status
- context

Current implementation supports two explicit modes:

- `file`: local development/test only, stored under `apps/orchestrator-api/.state/thread_state.json`
- `table`: Azure Table Storage, the production-shaped direction for runtime thread state

The `.state/` directory is ignored by git.

Production direction: store runtime thread state in Azure Table Storage.

Dataverse remains the system of record for business/audit records such as approvals, agent runs, orders and refunds. Thread state is technical orchestration state, so Azure Table Storage is a better fit than storing conversational state in Dataverse.

Cosmos DB is not part of the current architecture. It remains a possible future option only if the project needs high-volume conversational memory or complex state queries beyond what Table Storage should handle.

## 3. Type Safety

The project now treats typed contracts as the standard for internal agent boundaries.

Current Pydantic contracts include:

- `IntakeClassificationContract`
- `DraftSummaryContract`
- `GovernanceDecision`
- `ApprovalOutcome`
- `ThreadState`

The rule going forward:

```text
MCP boundary may return shaped dictionaries.
Agent-to-agent orchestration should move toward Pydantic models.
```

This reduces fragile string-key coupling and makes the architecture easier to test.

## 4. Richer Domain Model

The project will continue expanding the typed model around:

- customer
- account
- order
- order item
- shipment
- return request
- refund
- knowledge result
- governance decision
- approval outcome
- run telemetry
- thread state

This should be done incrementally as each boundary stabilizes. The goal is not to create a giant model upfront; the goal is to type the workflow where it removes real ambiguity.

## 5. AutoGen Position

AutoGen is not being added as a runtime dependency.

It remains important historically and conceptually:

- multi-agent conversations
- user proxy / human approval patterns
- group chat style orchestration
- tool-using agents

But the active Microsoft direction for this project remains:

```text
Microsoft Agent Framework for new LLM agents
Deterministic MCP-backed agents for predictable business steps
Semantic Kernel only for the DraftAgent comparison track
```

## Current Agent Pipeline

The primary order-support flow now moves toward:

```text
IntakeAgent
  -> DataAgent
  -> GovernanceAgent
  -> KnowledgeAgent
  -> DraftAgent
  -> CriticAgent
  -> CostAgent
  -> WorkflowAgent
```

Agent roles:

- `IntakeAgent`: classifies request and extracts intent/email/tool hints.
- `DataAgent`: retrieves customer/order/shipment/refund data via MCP.
- `GovernanceAgent`: determines risk and approval requirement.
- `KnowledgeAgent`: retrieves policy knowledge via MCP/Azure AI Search.
- `DraftAgent`: generates the support summary using Semantic Kernel.
- `CriticAgent`: evaluates the summary via MCP.
- `CostAgent`: calculates model cost via MCP.
- `WorkflowAgent`: manages approvals, events, run logging and thread state.

## Why This Fits the Project

The project positioning is Microsoft Agentic AI Architect.

That positioning is stronger when the system demonstrates:

- governed tool access through MCP
- human approval gates
- auditable state
- typed contracts
- model cost visibility
- response evaluation
- business workflow continuation

These changes make the project less like a chatbot and more like a real enterprise agent workflow platform.

## Immediate Next Steps

1. Keep moving agent boundaries from loose dictionaries toward Pydantic models.
2. Build the Power Apps Approval Console over the approval endpoints.
3. Deploy/update the Dataverse approval schema columns used by the console.
4. Deploy the Azure Table Storage thread-state configuration and test continuation against it.
5. Expand tests around approval pending/resume behavior.
