import uuid
from datetime import datetime, timezone
from typing import Any

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
    thread_id: str | None = None,
    customer_name: str | None = None,
    customer_email: str | None = None,
    order_number: str | None = None,
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
        "threadId": thread_id,
        "customerName": customer_name,
        "customerEmail": customer_email,
        "orderNumber": order_number,
        "decisionComment": None,
        "decidedOn": None,
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
                "cr_threadid": thread_id,
                "cr_customername": customer_name,
                "cr_customeremail": customer_email,
                "cr_ordernumber": order_number,
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
        "threadId": thread_id,
    }


def _map_approval_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "approvalId": row.get("approvalId") or row.get("cr_approvalkey"),
        "relatedRecordId": row.get("relatedRecordId") or row.get("cr_relatedrecordid"),
        "relatedRecordType": row.get("relatedRecordType") or row.get("cr_relatedrecordtype"),
        "requestedBy": row.get("requestedBy") or row.get("cr_requestedby"),
        "approvalType": row.get("approvalType") or row.get("cr_approvaltype"),
        "status": row.get("status") or row.get("cr_status"),
        "riskLevel": row.get("riskLevel") or row.get("cr_risklevel"),
        "reason": row.get("reason") or row.get("cr_reason"),
        "createdOn": row.get("createdOn") or row.get("createdon"),
        "approvedBy": row.get("approvedBy") or row.get("cr_approvedby"),
        "threadId": row.get("threadId") or row.get("cr_threadid"),
        "customerName": row.get("customerName") or row.get("cr_customername"),
        "customerEmail": row.get("customerEmail") or row.get("cr_customeremail"),
        "orderNumber": row.get("orderNumber") or row.get("cr_ordernumber"),
        "decisionComment": row.get("decisionComment") or row.get("cr_decisioncomment"),
        "decidedOn": row.get("decidedOn") or row.get("cr_decidedon"),
    }


@router.tool()
def list_pending_approval_requests(limit: int = 50) -> dict:
    """List pending human approval requests for approval console experiences."""
    if DATA_MODE == "dataverse":
        from enterprise_agentops_mcp.services.dataverse_service import dv_get

        rows = dv_get(
            "cr_approvalrequests",
            filter_query="cr_status eq 'Pending'",
            select=(
                "cr_approvalkey,cr_relatedrecordid,cr_relatedrecordtype,cr_requestedby,"
                "cr_approvaltype,cr_status,cr_risklevel,cr_reason,createdon,cr_approvedby,"
                "cr_threadid,cr_customername,cr_customeremail,cr_ordernumber,"
                "cr_decisioncomment,cr_decidedon"
            ),
            orderby="createdon desc",
            top=limit,
        )
        return {"approvals": [_map_approval_row(row) for row in rows]}
    if DATA_MODE == "mock":
        rows = [
            _map_approval_row(row)
            for row in load("approvals.json")
            if row.get("status") == "Pending"
        ]
        rows.sort(key=lambda row: row.get("createdOn") or "", reverse=True)
        return {"approvals": rows[:limit]}
    raise ValueError(f"Unsupported MCP_DATA_MODE: {DATA_MODE}")


@router.tool()
def decide_approval_request(
    approval_id: str,
    decision: str,
    approved_by: str,
    comment: str | None = None,
) -> dict:
    """Approve or reject a pending approval request."""
    if decision not in ("Approved", "Rejected"):
        raise ValueError("decision must be Approved or Rejected")

    decided_on = datetime.now(timezone.utc).isoformat()
    if DATA_MODE == "dataverse":
        from enterprise_agentops_mcp.services.dataverse_service import dv_get, dv_patch, escape_odata_string

        rows = dv_get(
            "cr_approvalrequests",
            filter_query=f"cr_approvalkey eq '{escape_odata_string(approval_id)}'",
            select=(
                "cr_approvalrequestid,cr_approvalkey,cr_relatedrecordid,cr_relatedrecordtype,"
                "cr_requestedby,cr_approvaltype,cr_status,cr_risklevel,cr_reason,createdon,"
                "cr_approvedby,cr_threadid,cr_customername,cr_customeremail,cr_ordernumber,"
                "cr_decisioncomment,cr_decidedon"
            ),
            top=1,
        )
        if not rows:
            return {"error": f"Approval not found: {approval_id}", "statusCode": 404}
        row = rows[0]
        dv_patch(
            "cr_approvalrequests",
            row["cr_approvalrequestid"],
            {
                "cr_status": decision,
                "cr_approvedby": approved_by,
                "cr_decisioncomment": comment,
                "cr_decidedon": decided_on,
            },
        )
        updated = _map_approval_row(row)
        updated.update(
            {
                "status": decision,
                "approvedBy": approved_by,
                "decisionComment": comment,
                "decidedOn": decided_on,
            }
        )
        return updated
    if DATA_MODE == "mock":
        approvals = load("approvals.json")
        for row in approvals:
            if row.get("approvalId") == approval_id:
                row["status"] = decision
                row["approvedBy"] = approved_by
                row["decisionComment"] = comment
                row["decidedOn"] = decided_on
                save("approvals.json", approvals)
                return _map_approval_row(row)
        return {"error": f"Approval not found: {approval_id}", "statusCode": 404}
    raise ValueError(f"Unsupported MCP_DATA_MODE: {DATA_MODE}")


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
