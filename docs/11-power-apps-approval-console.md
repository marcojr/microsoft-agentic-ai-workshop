# Stage 11: Power Apps Approval Console

Build the human-in-the-loop approval surface as a Power Apps canvas app running in the browser.

This is the active approval UX direction: Power Apps is the approver console, Dataverse stores approval records, and the Orchestrator API remains responsible for workflow state changes.

There is also a local HTML console for learning and fast smoke tests:

```text
GET /api/approval-console
```

The HTML console is not the enterprise target surface. It exists so the approval pattern can be felt in the browser before building the Power Apps canvas app.

## Target Flow

```text
Orchestrator API
  -> GovernanceAgent requires approval
  -> WorkflowAgent creates ApprovalRequest through MCP
  -> Dataverse stores cr_approvalrequest
  -> ThreadState moves to WaitingForApproval

Power Apps Approval Console
  -> lists pending approvals
  -> approver reviews risk, reason, customer, order
  -> approver selects Approve or Reject

Orchestrator API
  -> records decision through MCP
  -> updates Dataverse approval status
  -> updates ThreadState to Completed or Blocked
```

The LLM does not approve business action. It prepares context. A human approves or rejects.

## Backend Endpoints

Power Apps should call the Orchestrator through a custom connector.

Versioned connector assets:

- OpenAPI: [power-platform/custom-connectors/agentops-approval-console.openapi.json](../power-platform/custom-connectors/agentops-approval-console.openapi.json)
- Connector notes: [power-platform/custom-connectors/README.md](../power-platform/custom-connectors/README.md)
- Canvas formulas: [power-platform/power-apps/approval-console-formulas.md](../power-platform/power-apps/approval-console-formulas.md)

### List Pending Approvals

```http
GET /api/approvals/pending
```

### Decide Approval

```http
POST /api/approvals/decision
```

Request:

```json
{
  "approvalId": "apr-123",
  "threadId": "thread-123",
  "decision": "Approved",
  "approvedBy": "manager@contoso.com",
  "comment": "Approved under team lead threshold."
}
```

Allowed decisions:

- `Approved`
- `Rejected`

## Dataverse Contract

Power Apps reads from `cr_approvalrequests`.

Required approval-console columns:

| Display | Logical Name |
|---|---|
| Thread ID | `cr_threadid` |
| Customer Name | `cr_customername` |
| Customer Email | `cr_customeremail` |
| Order Number | `cr_ordernumber` |
| Decision Comment | `cr_decisioncomment` |
| Decided On | `cr_decidedon` |

Deploy or update the schema:

```powershell
powershell -ExecutionPolicy Bypass -File .\power-platform\scripts\Deploy-AgentOpsDataverseSchema.ps1
```

The schema deploy script adds missing columns to existing tables, so it can be rerun after this change.

## Canvas App Design

Create a canvas app named `AgentOps Approval Console`.

Recommended layout:

- Header: app name, refresh button, signed-in approver.
- Left gallery: pending approval requests.
- Right details panel: customer, order, risk, reason, thread ID, created date.
- Bottom command bar: approve, reject, comment input.

Suggested gallery fields:

- `orderNumber`
- `customerName`
- `riskLevel`
- `approvalType`
- `createdOn`

Preferred data approach:

1. Create a custom connector over the Orchestrator API.
2. Import `power-platform/custom-connectors/agentops-approval-console.openapi.json`.
3. Use `ListPendingApprovals` for the gallery.
4. Use `SubmitApprovalDecision` for approve/reject.

This keeps thread-state mutation inside the Orchestrator and avoids teaching Power Apps how to update Azure Table Storage.

Power Apps may expose the `SubmitApprovalDecision` OpenAPI body as required parameters plus an optional record:

```powerfx
AgentOpsApprovalConsole.SubmitApprovalDecision(
    varSelectedApproval.approvalId,
    "Approved",
    User().Email,
    {comment: txtDecisionComment.Text}
)
```

Use the formulas in [power-platform/power-apps/approval-console-formulas.md](../power-platform/power-apps/approval-console-formulas.md) as the current source of truth for the Canvas App.

## Local Test

Start the Function app:

```bash
cd apps/orchestrator-api
source .venv/bin/activate
func start --python
```

List pending approvals:

```bash
curl -s "http://localhost:7071/api/approvals/pending" | jq
```

Open the local HTML console:

```text
http://localhost:7071/api/approval-console
```

Approve an item:

```bash
curl -s -X POST "http://localhost:7071/api/approvals/decision" \
  -H "Content-Type: application/json" \
  -d '{
    "approvalId": "apr-123",
    "threadId": "thread-123",
    "decision": "Approved",
    "approvedBy": "manager@contoso.com",
    "comment": "Approved under team lead threshold."
  }' | jq
```
