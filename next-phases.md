# Next Phases

Roadmap after the current Enterprise AgentOps Control Tower MVP.

The current MVP stays as the stable baseline:

- Azure Function Orchestrator API
- Microsoft Agent Framework pro-code agents
- Enterprise AgentOps MCP Server
- Dataverse business records
- Azure AI Search knowledge retrieval
- Copilot Studio agent with approval tools
- Power Apps approval console
- Power BI operations report
- Application Insights telemetry

The next phases modernize the experience without throwing away the working foundation.

---

## Phase 2: Copilot Studio Modernization

Goal: adapt the current Copilot Studio agent to the new Copilot Studio agent experience.

Why:

- Learn the new Copilot Studio model by comparison with the current working agent.
- Move more orchestration responsibility into Copilot Studio where it makes sense.
- Use more built-in tools and skills instead of only custom connectors.

What to use:

- New Copilot Studio agent experience
- Tools
- Skills
- Connected agents
- Knowledge
- Memory/state where available
- Activity map, evaluation and monitoring features

### Skills Strategy

In the modern Copilot Studio phase, skills are how we package reusable business capabilities for the agent. They should not replace every backend agent. They should wrap user-facing capabilities that Copilot can decide to invoke during conversation.

Use skills for:

- business tasks the user can ask for directly;
- reusable workflows that may call tools;
- guided decision flows;
- policy/question-answering capabilities;
- conversational orchestration around existing APIs.

Do not use skills for:

- hidden telemetry writes;
- raw Dataverse writes;
- cost calculation internals;
- final approval state transitions without controlled connector/API calls;
- logic that must also run identically from Microsoft 365 Agents SDK.

Planned skills:

| Skill | Purpose | Backing Capability | Migration Decision |
|---|---|---|---|
| `Review Pending Approvals` | Let a manager inspect pending approval requests conversationally | Custom connector `ListPendingApprovals` | New Copilot skill wrapping existing tool |
| `Submit Approval Decision` | Guide approve/reject decisions with comments | Custom connector `SubmitApprovalDecision` | New Copilot skill wrapping existing tool |
| `Explain Approval Risk` | Explain why an approval is high risk | Copilot reasoning + approval data + policy knowledge | Partially replaces simple Critic-style explanations, but not backend scoring |
| `Order Support Triage` | Ask for customer/order info and decide whether to call full orchestrator | Copilot orchestration + Orchestrator API | Partially migrates Intake behavior |
| `Policy Lookup` | Answer refund/shipment/compensation policy questions | Copilot knowledge and/or Azure AI Search tool | Partially migrates Knowledge Agent for FAQ use |
| `Escalation Recommendation` | Suggest next action for support manager | Approval data + policy knowledge + backend risk fields | Copilot-owned guidance, backend remains source of truth |

Skill design rules:

- A skill can decide what the user probably wants.
- A skill can ask clarification questions.
- A skill can call existing tools.
- A skill can summarize results for the user.
- A skill must not silently bypass approval controls.
- A skill must not become the only implementation of business-critical workflow logic.

### Tools vs Skills vs Orchestrator

| Need | Use |
|---|---|
| User asks “what approvals are pending?” | Skill wrapping `ListPendingApprovals` |
| User asks “approve this one” | Skill wrapping `SubmitApprovalDecision` |
| User asks “what is the refund policy?” | Copilot knowledge / `Policy Lookup` skill |
| User asks “what should I do with this delayed shipment?” | `Escalation Recommendation` skill |
| User asks “process this customer order issue end-to-end” | Orchestrator API |
| Backend needs to write Dataverse approval status | Orchestrator/API/tool only |
| Backend needs cost/telemetry/audit logging | Orchestrator/MCP only |

### Skill Implementation Plan

1. Create skills in the modern Copilot Studio agent, not in the current baseline agent.
2. Start with two skills:
   - `Review Pending Approvals`
   - `Submit Approval Decision`
3. Bind those skills to the existing custom connector tools.
4. Add descriptions that explain when Copilot should use each skill.
5. Add `Policy Lookup` using knowledge sources.
6. Add `Order Support Triage` only after the approval skills work.
7. Add `Escalation Recommendation` last, because it mixes approval data and policy reasoning.

### Skill Validation Prompts

Review:

```text
Show me the pending approvals and tell me which ones are risky.
```

Decision:

```text
Approve approval apr-123 because the refund is within policy and the customer has a confirmed delay.
```

Policy:

```text
When does delayed shipment compensation require approval?
```

Triage:

```text
Customer john.smith@contoso.com says the shipment is late. What should we do?
```

Escalation:

```text
Should I approve this high-risk compensation request?
```

Expected result:

- Copilot chooses the right skill.
- The skill calls the right tool when needed.
- The skill asks for missing approval/customer/order data.
- The backend still owns final writes, telemetry and audit records.

Modernization principle:

The current Copilot Studio agent is mostly a conversational front door. It calls tools, but the real agentic pipeline lives in the Azure Function Orchestrator:

```text
Copilot Studio -> Custom Connector / REST -> Orchestrator API -> Microsoft Agent Framework agents -> MCP tools -> Dataverse/Search/Telemetry
```

The modernized version should not blindly replace the backend. It should move only the parts that are natural for Copilot Studio:

- conversation planning
- clarification questions
- tool selection
- knowledge Q&A
- lightweight approval review
- user-facing state

The backend should keep the parts that must remain deterministic, auditable or reusable across channels.

### Agent Migration Matrix

| Current Component | Current Role | Modern Copilot Decision | Reason |
|---|---|---|---|
| Copilot Studio agent | Thin chat interface calling connector tools | Replace with modern Copilot Studio agent | This is the main modernization target |
| Intake Agent | Classifies intent and extracts customer/order info | Partially migrate | Copilot can handle basic intent and clarification; backend should still validate structured inputs |
| Data Agent | Calls MCP tools for customer/order/shipment/refund data | Keep in backend | Data retrieval must stay governed and reusable |
| Knowledge Agent | Calls Azure AI Search through MCP | Partially migrate | Copilot can use native knowledge for simple FAQ; backend RAG remains for governed workflow grounding |
| Governance Agent | Decides approval requirement | Keep in backend | Approval logic must be deterministic, auditable and tested |
| Draft Agent | Generates grounded summary | Keep in backend for workflow summaries | Copilot can summarize conversationally, but official workflow output should stay in MAF |
| Critic / Evaluator | Scores quality, groundedness and risk | Keep in backend | Evaluation must be logged and repeatable |
| Cost Agent | Calculates model/token cost | Keep in backend | Cost telemetry belongs to the controlled runtime |
| Workflow Agent | Creates approvals, thread state, events and run logs | Keep in backend | This is system-of-record orchestration |
| Power Apps Approval Console | Human approval UI | Keep | It is deterministic and manager-friendly |
| Power BI report | Operations dashboard | Keep | It remains the reporting layer |

### What Copilot Studio Should Own After Modernization

Copilot Studio should become smarter than the current thin interface:

- decide when to call approval tools;
- ask for missing customer email/order ID;
- answer policy questions from knowledge;
- summarize pending approvals conversationally;
- use built-in Power Platform/Microsoft 365 tools where useful;
- maintain conversational state for the operator;
- route between approval review, policy Q&A and order-support workflows.

### What Copilot Studio Must Not Own

These stay in backend/MCP:

- final approval state changes;
- Dataverse writes;
- cost and telemetry logging;
- compliance/governance decisions;
- official workflow summaries;
- direct business data joins;
- anything that must work again later from Microsoft 365 Agents SDK.

### Target Modern Flow

```text
User
  -> Modern Copilot Studio Agent
     -> Built-in knowledge/tools for simple questions
     -> Custom connector tools for approval review
     -> Orchestrator API for full governed workflow
        -> Microsoft Agent Framework agents
        -> MCP Server
        -> Dataverse / Azure AI Search / App Insights / Service Bus
```

### Concrete Modernization Work Items

1. Create `AgentOps Support Agent - Modern`.
2. Recreate current instructions in the new experience.
3. Add existing approval connector tools.
4. Add native knowledge for policies if available.
5. Add at least one out-of-the-box Microsoft tool, preferably Dataverse read or SharePoint knowledge.
6. Configure orchestration so Copilot decides between:
   - approval review;
   - policy question;
   - full order-support workflow.
7. Test whether Copilot can replace the backend Intake Agent for basic clarification only.
8. Keep backend validation even if Copilot does the first pass.
9. Document what was replaced, partially migrated or kept.

Official docs:

- New agent experience: https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/overview
- Classic vs new experience: https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/classic-vs-new
- Generative orchestration: https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions
- Skills: https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-add-skills
- Connected agents: https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents
- Knowledge: https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio

Steps:

1. Keep the existing Copilot Studio agent as the baseline.
2. Create a new modern Copilot Studio agent named `AgentOps Support Agent - Modern`.
3. Reuse the same business instructions from the current agent.
4. Add the existing `AgentOps Approval Console` connector tools:
   - `ListPendingApprovals`
   - `SubmitApprovalDecision`
5. Add native/out-of-the-box tools where useful:
   - Dataverse
   - SharePoint or OneDrive knowledge
   - Teams/Outlook/Planner if the scenario benefits from them
6. Add knowledge sources for policy questions:
   - refund policy
   - delivery delay policy
   - approval policy
7. Test whether the modern agent can replace some backend-only agent behavior:
   - simple approval listing
   - policy lookup
   - routing between tools
   - clarification questions
8. Keep the Azure Function Orchestrator for governed workflow execution.
9. Document what moved into Copilot Studio and what stayed in the backend.

Validation:

- Ask it to list pending approvals.
- Ask it to explain why an approval is high risk.
- Ask it to approve/reject an approval with a comment.
- Ask a policy question and verify it uses knowledge.
- Confirm Dataverse state changes after approval/rejection.

Deliverables:

- Modern Copilot Studio agent
- Comparison notes: classic/current vs modern
- Screenshots of tools, skills, knowledge and test results
- Updated architecture diagram if orchestration responsibility changes

---

## Phase 3: Microsoft 365 Agents SDK

Goal: create a custom-engine Microsoft 365 agent that reuses the same backend.

Why:

- This is the developer-first/custom-agent path.
- It proves the architecture is not locked to Copilot Studio.
- It demonstrates how the same orchestrator and MCP layer can serve multiple agent surfaces.

What to use:

- Microsoft 365 Agents SDK
- Microsoft 365 Agents Playground
- Existing Azure Function Orchestrator API
- Existing MCP Server
- Existing Dataverse and telemetry

Steps:

1. Review the current `apps/m365-agent/` placeholder.
2. Create the Microsoft 365 agent project.
3. Configure local dev environment and app registration if required.
4. Implement a simple chat route:
   - user asks about latest order
   - agent calls Orchestrator API
   - agent returns summary and approval status
5. Add an approval review path:
   - list pending approvals
   - submit approval/rejection
6. Test in Microsoft 365 Agents Playground.
7. Decide whether Teams deployment is needed or if Playground is enough for the demo.

Validation:

- Same customer/order scenario works through the M365 agent.
- Same approval request appears in Dataverse.
- Same telemetry appears in Dataverse/App Insights/Power BI.

Deliverables:

- Working M365 agent project
- Playground screenshots
- Short comparison: Copilot Studio vs Microsoft 365 Agents SDK
- Updated final walkthrough section

---

## Phase 4: RAG / Knowledge Expansion

Goal: make Azure AI Search knowledge retrieval more realistic and useful.

Why:

- The MVP proves that RAG works.
- This phase makes the knowledge layer strong enough for real policy reasoning.
- It improves groundedness and explainability.

What to expand:

- Refund policy documents
- Delivery delay policy documents
- Compensation approval rules
- Escalation policy
- Responsible AI / governance policy
- Internal support playbooks

Steps:

1. Add more policy documents under `data/knowledge/`.
2. Index them into Azure AI Search.
3. Improve metadata:
   - category
   - policy type
   - effective date
   - risk level
   - approval requirement
4. Add or improve search test prompts:
   - “When does compensation require approval?”
   - “What should we do for delayed shipments?”
   - “Can we refund before approval?”
5. Improve groundedness evaluation.
6. Consider exposing a direct search tool to Copilot Studio if useful.

Validation:

- Search returns the right policy for known questions.
- Draft summaries cite the right policy source.
- Critic/evaluation catches unsupported claims.

Deliverables:

- Expanded knowledge corpus
- Search test set
- Updated RAG documentation
- Updated demo prompts

---

## Phase 5: Power Platform / Tool Ecosystem Expansion

Goal: use more Microsoft-native tools and connectors, not only our custom tools.

Why:

- Demonstrates the real Power Platform/Copilot Studio ecosystem.
- Shows when native tools are enough and when custom MCP/custom connectors are justified.
- Makes the demo feel more like an enterprise Microsoft solution.

Candidate tools/connectors:

- Dataverse native connector
- SharePoint knowledge
- OneDrive knowledge
- Teams actions
- Outlook actions
- Planner tasks
- Power Automate flows
- Existing custom connector for approval console

Steps:

1. Inventory useful built-in tools in the modern Copilot Studio agent.
2. Pick two or three that strengthen the demo.
3. Add SharePoint/OneDrive knowledge if documents are available.
4. Add a native Dataverse read action if it can safely expose approval/order data.
5. Add a Teams or Outlook action only if it fits the support workflow.
6. Compare:
   - native tool
   - custom connector
   - MCP-backed backend call

Validation:

- Native tools work without breaking governance.
- Sensitive writes still go through controlled approval paths.
- The agent does not bypass Dataverse approval rules.

Deliverables:

- Tool inventory
- Native tool screenshots
- Updated architecture notes
- Recommendation table: native tool vs custom connector vs MCP

---

## Phase 6: Microsoft Purview Governance

Goal: add enterprise governance and compliance after the agentic workflow is already working.

Why this is last:

- Purview is a governance layer, not the core agentic runtime.
- It may require trial/licensing or pay-as-you-go setup.
- It is strongest as the final enterprise maturity layer.

What to evaluate:

- Microsoft Purview trial
- Sensitivity labels
- Data classification
- Compliance posture
- Governance over Dataverse, Power BI and knowledge documents
- AI/data access policies where available

Official docs:

- Purview trial: https://learn.microsoft.com/en-us/purview/purview-trial
- Purview billing models: https://learn.microsoft.com/en-us/purview/purview-billing-models
- Purview pricing: https://www.microsoft.com/en-us/security/microsoft-purview-pricing

Steps:

1. Check tenant eligibility for the 90-day Purview trial.
2. Confirm whether the trial is enough for the demo.
3. Avoid pay-as-you-go features unless explicitly needed.
4. Classify key data sources:
   - Dataverse approval records
   - customer/order data
   - Power BI report
   - policy documents
5. Apply labels or governance controls where available.
6. Document how governed data affects the agent workflow.

Validation:

- Show which data sources are governed.
- Show labels/classification where available.
- Explain how approval and audit trails support compliance.

Deliverables:

- Purview setup notes
- Governance screenshots
- Updated architecture diagram
- Enterprise governance talk track

---

## Recommended Execution Order

1. Copilot Studio Modernization
2. Microsoft 365 Agents SDK
3. RAG / Knowledge Expansion
4. Power Platform / Tool Ecosystem Expansion
5. Microsoft Purview Governance

This order keeps the next work focused on agent capability first, then knowledge depth, then ecosystem breadth, then enterprise governance.
