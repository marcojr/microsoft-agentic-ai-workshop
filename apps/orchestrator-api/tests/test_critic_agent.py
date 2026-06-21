from src.agents.critic_agent import CriticAgent


class _FakeMCPClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def call(self, tool_name: str, params: dict) -> dict:
        self.calls.append((tool_name, params))
        return {
            "qualityScore": 0.92,
            "groundednessScore": 0.88,
            "riskScore": 0.82,
            "issues": [],
            "approvedForUser": True,
        }


def test_critic_agent_evaluates_summary_with_required_sources() -> None:
    client = _FakeMCPClient()

    result = CriticAgent(client).evaluate_order_support_summary(
        summary="Approval is required before compensation is communicated.",
        order={"orderId": "ord-1"},
        shipment={"shipmentId": "ship-1"},
        risk="High",
    )

    assert result["qualityScore"] == 0.92
    assert result["requiredSources"] == ["ord-1", "ship-1"]
    assert result["toolsCalled"] == ["evaluate_response"]
    assert client.calls == [
        (
            "evaluate_response",
            {
                "response": "Approval is required before compensation is communicated.",
                "required_sources": ["ord-1", "ship-1"],
                "risk_level": "High",
            },
        )
    ]


def test_critic_agent_omits_missing_source_ids() -> None:
    client = _FakeMCPClient()

    result = CriticAgent(client).evaluate_order_support_summary(
        summary="Order is delivered.",
        order={},
        shipment={"shipmentId": "ship-1"},
        risk="Low",
    )

    assert result["requiredSources"] == ["ship-1"]
