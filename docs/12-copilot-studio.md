# Stage 12: Copilot Studio Agent

Create the business-facing Copilot Studio agent that uses Power Platform connector tools.

---

## Current Agent

Name:

```text
AgentOps Support Agent
```

Purpose:

- list pending human approvals
- summarize approval risk
- submit approve/reject decisions

---

## Create the Agent

Go to:

```text
https://copilotstudio.microsoft.com
```

Use the environment:

```text
Marco Jr Digital Ventures LTD (default)
```

Create:

```text
Agents -> New agent
```

Description:

```text
Enterprise support operations agent for approval review, policy lookup and agentic workflow coordination.
```

Instructions:

```text
You are an enterprise support operations agent. Help users review pending approval requests,
understand customer/order risk context, and decide whether approvals should be accepted or
rejected. Use available tools when approval data is needed. Be concise and ask for
clarification when required.
```

---

## Add Approval Tools

Path:

```text
Agent -> Tools -> Add a tool -> Connector
```

Search for:

```text
AgentOps Approval Console
```

Add:

```text
ListPendingApprovals
SubmitApprovalDecision
```

`ListPendingApprovals` reads pending approval records through:

```text
Copilot Studio -> Custom Connector -> Azure Function -> Dataverse
```

`SubmitApprovalDecision` updates the approval decision through:

```text
Copilot Studio -> Custom Connector -> Azure Function -> Dataverse + Azure Table thread state
```

For `SubmitApprovalDecision`, use these input descriptions:

```text
approvalId: The approval request ID to approve or reject. Example: apr-4874e82a.
decision: The decision to apply. Must be exactly Approved or Rejected.
approvedBy: Email address of the human approver. Use the current user's email when available.
comment: Short explanation for the approval or rejection decision.
threadId: Workflow thread ID linked to the approval. If unknown, use the threadId from the approval request.
```

For the workshop version, keep the inputs filled by AI.

---

## Verified Approval Flow

Prompt:

```text
List the current pending approvals and summarize the risk.
```

Verified response included:

```text
approvalId: apr-4874e82a
customer: John Smith
order: WEB-1001
riskLevel: High
status: Pending
```

Decision prompt:

```text
Approve approval apr-4874e82a because the delayed shipment compensation is valid and the refund amount is within policy.
```

After approval, this prompt returned no pending approvals:

```text
List the current pending approvals.
```

---

## Architecture Proven

```text
Copilot Studio Agent
  -> Tool
  -> Power Platform Custom Connector
  -> Azure Function App
  -> MCP/orchestrator logic
  -> Dataverse
  -> Azure Table thread state
```

---

## Next Steps

- Finish the Power Apps Approval Console approve/reject buttons.
- Publish the Canvas App.
- Add observability and cost dashboard polish.
- Add Microsoft Purview as a governance/compliance phase after the core workflow is stable.
