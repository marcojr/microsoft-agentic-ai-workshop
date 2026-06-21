from pydantic import ValidationError

from src.agents.models import ApprovalDecisionRequest
from src.shared.mcp_client import MCPClient
from src.shared.thread_state_store import ThreadStateStore


def list_pending_approvals() -> tuple[dict, int]:
    client = MCPClient()
    result = client.call("list_pending_approval_requests", {"limit": 100})
    if "error" in result:
        return result, result.get("statusCode", 500)
    return result, 200


def decide_approval(body: dict) -> tuple[dict, int]:
    try:
        request = ApprovalDecisionRequest.model_validate(body)
    except ValidationError as exc:
        return {"error": "Invalid approval decision request", "details": exc.errors()}, 400

    client = MCPClient()
    result = client.call(
        "decide_approval_request",
        {
            "approval_id": request.approvalId,
            "decision": request.decision,
            "approved_by": request.approvedBy,
            "comment": request.comment,
        },
    )
    if "error" in result:
        return result, result.get("statusCode", 500)

    # Step 1: Resolve the workflow thread from the decision body or approval record.
    thread_id = request.threadId or result.get("threadId")
    if thread_id:
        store = ThreadStateStore()
        state = store.get_or_create(
            thread_id=thread_id,
            workflow_name="WebshopOrderSupport",
            customer_email=result.get("customerEmail"),
            intent=None,
        )
        # Step 2: Capture the human decision in thread state for follow-up turns.
        state.status = "Completed" if request.decision == "Approved" else "Blocked"
        state.currentStep = (
            "human_approval_approved"
            if request.decision == "Approved"
            else "human_approval_rejected"
        )
        state.approvalId = request.approvalId
        state.context.update(
            {
                "approvalDecision": request.decision,
                "approvalDecidedBy": request.approvedBy,
                "approvalDecisionComment": request.comment,
                "approvalDecidedOn": result.get("decidedOn"),
            }
        )
        store.save(state)
        result["threadStatus"] = state.status
        result["threadCurrentStep"] = state.currentStep

    return result, 200
