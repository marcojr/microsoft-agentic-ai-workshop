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

    if DATA_MODE == "dataverse":
        from enterprise_agentops_mcp.services.dataverse_service import dv_post

        dv_post(
            "cr_approvalrequests",
            {
                "cr_approvalkey": approval_id,
                "cr_relatedrecordid": related_record_id,
                "cr_relatedrecordtype": related_record_type,
                "cr_requestedby": requested_by,
                "cr_approvaltype": approval_type,
                "cr_status": "Pending",
                "cr_risklevel": risk_level,
                "cr_reason": reason,
                "cr_approvedby": None,
            },
        )
    elif DATA_MODE == "mock":
        approvals = load("approvals.json")
        approvals.append(approval)
        save("approvals.json", approvals)
    else:
        raise ValueError(f"Unsupported MCP_DATA_MODE: {DATA_MODE}")

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
