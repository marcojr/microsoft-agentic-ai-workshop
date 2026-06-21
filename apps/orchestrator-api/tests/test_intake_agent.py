import asyncio

import pytest

from src.agents.intake_agent import IntakeAgent


class _FakeResponse:
    def __init__(self, text: str) -> None:
        self.text = text


class _FakeAgent:
    def __init__(self, text: str) -> None:
        self._text = text

    async def run(self, _message: str, **_kwargs) -> _FakeResponse:
        return _FakeResponse(self._text)


def test_intake_agent_parses_classification_json() -> None:
    agent = IntakeAgent.__new__(IntakeAgent)
    agent.allowed_tool_names = [
        "get_customer_by_email",
        "get_latest_order",
        "get_shipment_status",
    ]
    agent.agent = _FakeAgent(
        """
        {
          "intent": "SummariseLatestOrderDeliveryStatus",
          "businessDomain": "Logistics",
          "urgency": "High",
          "toolsRequired": ["get_customer_by_email", "get_latest_order", "get_shipment_status"],
          "riskLevel": "High",
          "approvalLikelihood": "Medium",
          "contactEmail": "john.smith@contoso.com",
          "orderReference": null
        }
        """
    )

    result = asyncio.run(
        agent.classify_request(
            "Check the delayed order for john.smith@contoso.com and tell me what is happening."
        )
    )

    assert result["intent"] == "SummariseLatestOrderDeliveryStatus"
    assert result["businessDomain"] == "Logistics"
    assert result["contactEmail"] == "john.smith@contoso.com"


def test_parse_contract_returns_typed_fields() -> None:
    contract = IntakeAgent._parse_contract(
        """
        {
          "intent": "SummariseLatestOrderDeliveryStatus",
          "businessDomain": "Logistics",
          "urgency": "High",
          "toolsRequired": ["get_customer_by_email", "get_latest_order", "get_shipment_status"],
          "riskLevel": "High",
          "approvalLikelihood": "Medium",
          "contactEmail": "john.smith@contoso.com",
          "orderReference": null
        }
        """
    )

    assert contract.intent == "SummariseLatestOrderDeliveryStatus"
    assert contract.toolsRequired == [
        "get_customer_by_email",
        "get_latest_order",
        "get_shipment_status",
    ]
    assert contract.contactEmail == "john.smith@contoso.com"


def test_build_instructions_includes_tool_registry_and_json_schema() -> None:
    instructions = IntakeAgent._build_instructions(
        ["get_customer_by_email", "get_latest_order"]
    )

    assert '"toolsRequired": ["exact registered MCP tool names only"]' in instructions
    assert "- get_customer_by_email" in instructions
    assert "- get_latest_order" in instructions


def test_parse_contract_rejects_unknown_tool_names() -> None:
    with pytest.raises(ValueError, match="Customer Database"):
        IntakeAgent._parse_contract(
            """
            {
              "intent": "SummariseLatestOrderDeliveryStatus",
              "businessDomain": "Logistics",
              "urgency": "High",
              "toolsRequired": ["Customer Database", "Shipment Tracking"],
              "riskLevel": "High",
              "approvalLikelihood": "Medium",
              "contactEmail": "john.smith@contoso.com",
              "orderReference": null
            }
            """,
            allowed_tool_names=[
                "get_customer_by_email",
                "get_latest_order",
                "get_shipment_status",
            ],
        )


def test_intake_agent_requires_message() -> None:
    agent = IntakeAgent.__new__(IntakeAgent)
    agent.agent = _FakeAgent("{}")

    try:
        asyncio.run(agent.classify_request("   "))
    except ValueError as exc:
        assert str(exc) == "user_message is required."
    else:
        raise AssertionError("Expected ValueError for empty user_message.")
