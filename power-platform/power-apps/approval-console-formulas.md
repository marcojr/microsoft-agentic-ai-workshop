# AgentOps Approval Console Canvas App Formulas

Canvas app name:

```text
AgentOps Approval Console
```

Custom connector:

```text
AgentOpsApprovalConsole
```

Connector operations:

- `ListPendingApprovals`
- `SubmitApprovalDecision`

## App.OnStart

```powerfx
Set(varApproverEmail, User().Email);
RefreshApprovals()
```

## Screen.OnVisible

```powerfx
RefreshApprovals()
```

## Refresh Button.OnSelect

```powerfx
RefreshApprovals()
```

## RefreshApprovals Named Formula / Reusable Pattern

If using a button-only implementation, put this block in `RefreshButton.OnSelect` and `Screen.OnVisible`:

```powerfx
ClearCollect(
    colPendingApprovals,
    AgentOpsApprovalConsole.ListPendingApprovals().approvals
);
Set(varSelectedApproval, First(colPendingApprovals))
```

## Gallery.Items

```powerfx
SortByColumns(
    colPendingApprovals,
    "createdOn",
    SortOrder.Descending
)
```

## Gallery.OnSelect

```powerfx
Set(varSelectedApproval, ThisItem);
Reset(txtDecisionComment)
```

## Detail Labels

Customer:

```powerfx
varSelectedApproval.customerName
```

Order:

```powerfx
varSelectedApproval.orderNumber
```

Risk:

```powerfx
varSelectedApproval.riskLevel
```

Reason:

```powerfx
varSelectedApproval.reason
```

Thread:

```powerfx
varSelectedApproval.threadId
```

## Approve Button.DisplayMode

```powerfx
If(
    IsBlank(varSelectedApproval.approvalId),
    DisplayMode.Disabled,
    DisplayMode.Edit
)
```

## Approve Button.OnSelect

Power Apps expands the OpenAPI body schema into required parameters plus an optional record.
Use this connector signature:

```powerfx
SubmitApprovalDecision(approvalId, decision, approvedBy, {comment: commentText})
```

```powerfx
Set(
    varDecisionResult,
    AgentOpsApprovalConsole.SubmitApprovalDecision(
        varSelectedApproval.approvalId,
        "Approved",
        varApproverEmail,
        {comment: txtDecisionComment.Text}
    )
);
Notify(
    "Approval " & varSelectedApproval.approvalId & " approved.",
    NotificationType.Success
);
ClearCollect(
    colPendingApprovals,
    AgentOpsApprovalConsole.ListPendingApprovals().approvals
);
Reset(txtDecisionComment);
Set(varSelectedApproval, Blank())
```

## Reject Button.OnSelect

```powerfx
Set(
    varDecisionResult,
    AgentOpsApprovalConsole.SubmitApprovalDecision(
        varSelectedApproval.approvalId,
        "Rejected",
        varApproverEmail,
        {comment: txtDecisionComment.Text}
    )
);
Notify(
    "Approval " & varSelectedApproval.approvalId & " rejected.",
    NotificationType.Warning
);
ClearCollect(
    colPendingApprovals,
    AgentOpsApprovalConsole.ListPendingApprovals().approvals
);
Reset(txtDecisionComment);
Set(varSelectedApproval, Blank())
```

## Visual Structure

- Header: title, approver email, refresh button.
- Left gallery: `colPendingApprovals`.
- Right detail pane: `varSelectedApproval`.
- Bottom actions: comment input, approve, reject.

The Canvas App is the final approval UX. The local HTML page is only a same-origin development smoke test for the same backend contract.
