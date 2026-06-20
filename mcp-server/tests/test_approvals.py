from enterprise_agentops_mcp.tools.approvals import create_approval_request, create_follow_up_task
from enterprise_agentops_mcp.tools import approvals


def test_create_approval_request() -> None:
    result = create_approval_request(
        related_record_id="ord-1001",
        related_record_type="order",
        approval_type="Compensation",
        reason="Delayed shipment and requested refund compensation",
        risk_level="High",
    )
    assert result["status"] == "Pending"
    assert result["approvalId"].startswith("apr-")


def test_create_approval_request_dataverse_mode(monkeypatch) -> None:
    monkeypatch.setattr(approvals, "DATA_MODE", "dataverse")
    captured: dict = {}

    def fake_dv_post(entity_set: str, data: dict) -> dict:
        captured["entity_set"] = entity_set
        captured["data"] = data
        return {"status": "created"}

    monkeypatch.setattr(
        "enterprise_agentops_mcp.services.dataverse_service.dv_post",
        fake_dv_post,
    )

    result = create_approval_request(
        related_record_id="ord-1001",
        related_record_type="order",
        approval_type="Compensation",
        reason="Delayed shipment and requested refund compensation",
        risk_level="High",
        requested_by="agent",
    )

    assert result["status"] == "Pending"
    assert result["approvalId"].startswith("apr-")
    assert captured["entity_set"] == "cr_approvalrequests"
    assert captured["data"]["cr_relatedrecordid"] == "ord-1001"
    assert captured["data"]["cr_relatedrecordtype"] == "order"
    assert captured["data"]["cr_approvaltype"] == "Compensation"
    assert captured["data"]["cr_requestedby"] == "agent"
    assert captured["data"]["cr_status"] == "Pending"
    assert captured["data"]["cr_risklevel"] == "High"


def test_create_follow_up_task() -> None:
    result = create_follow_up_task(
        related_record_id="ord-1001",
        related_record_type="order",
        subject="Follow up with customer",
        due_date="2026-06-19",
        owner="Support Team A",
    )
    assert result["status"] == "Created"
    assert result["taskId"].startswith("task-")
