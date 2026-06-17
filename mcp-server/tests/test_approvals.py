from enterprise_agentops_mcp.tools.approvals import create_approval_request, create_follow_up_task


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
