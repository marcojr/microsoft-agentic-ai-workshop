import uuid
from datetime import datetime, timezone

import httpx
from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE, POWER_AUTOMATE_APPROVAL_URL
from enterprise_agentops_mcp.services.mock_data_service import load, save

router = FastMCP()


@router.tool()
def create_approval_request(
    related_record_id: str,
    related_record_type: str,
    approval_type: str,
    reason: str,
    risk_level: str,
    requested_by: str = "agent",
) -> dict:
    """Create a human approval request for high-risk or sensitive actions."""
    approval_id = f"apr-{uuid.uuid4().hex[:8]}"
    created_on = datetime.now(timezone.utc).isoformat()
    approval = {
        "approvalId": approval_id,
        "relatedRecordId": related_record_id,
        "relatedRecordType": related_record_type,
        "requestedBy": requested_by,
        "approvalType": approval_type,
        "status": "Pending",
        "riskLevel": risk_level,
        "reason": reason,
        "createdOn": created_on,
        "approvedBy": None,
    }

    if DATA_MODE != "mock":
        raise NotImplementedError("Dataverse mode not yet implemented - see Stage 7")

    approvals = load("approvals.json")
    approvals.append(approval)
    save("approvals.json", approvals)

    if POWER_AUTOMATE_APPROVAL_URL:
        response = httpx.post(POWER_AUTOMATE_APPROVAL_URL, json=approval, timeout=5)
        response.raise_for_status()

    return {
        "approvalId": approval_id,
        "status": "Pending",
        "relatedRecordId": related_record_id,
        "riskLevel": risk_level,
        "createdOn": created_on,
    }


@router.tool()
def create_follow_up_task(
    related_record_id: str,
    related_record_type: str,
    subject: str,
    due_date: str,
    owner: str,
) -> dict:
    """Create a follow-up task linked to a record."""
    return {
        "taskId": f"task-{uuid.uuid4().hex[:8]}",
        "status": "Created",
        "subject": subject,
        "dueDate": due_date,
        "owner": owner,
        "relatedRecordId": related_record_id,
        "relatedRecordType": related_record_type,
    }
