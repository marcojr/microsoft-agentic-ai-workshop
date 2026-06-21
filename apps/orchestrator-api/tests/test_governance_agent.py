from src.agents.governance_agent import GovernanceAgent


def test_governance_agent_requires_approval_for_delay_with_approval_refund() -> None:
    result = GovernanceAgent().assess_order_support_risk(
        shipment={"status": "Delayed"},
        refunds={"refunds": [{"requiresApproval": True}]},
        returns={"returns": [{"returnId": "ret-1"}]},
        intake={"riskLevel": "Medium"},
    )

    assert result == {
        "risk": "High",
        "requiresApproval": True,
        "approvalType": "Compensation",
        "reason": "Delayed shipment with pending refund",
        "approvalTrigger": "DelayedShipmentWithRefundApproval",
    }


def test_governance_agent_uses_medium_risk_for_delay_without_refund_approval() -> None:
    result = GovernanceAgent().assess_order_support_risk(
        shipment={"status": "Delayed"},
        refunds={"refunds": [{"requiresApproval": False}]},
        returns={"returns": []},
        intake={"riskLevel": "Low"},
    )

    assert result["risk"] == "Medium"
    assert result["requiresApproval"] is False
    assert result["approvalType"] == "None"


def test_governance_agent_uses_low_risk_when_no_signals_exist() -> None:
    result = GovernanceAgent().assess_order_support_risk(
        shipment={"status": "Delivered"},
        refunds={"refunds": []},
        returns={"returns": []},
        intake={},
    )

    assert result["risk"] == "Low"
    assert result["requiresApproval"] is False
