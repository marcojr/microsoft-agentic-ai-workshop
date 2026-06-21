from src.agents.data_agent import DataAgent


class _FakeMCPClient:
    def __init__(self, responses: dict[str, dict]) -> None:
        self.responses = responses
        self.calls: list[tuple[str, dict]] = []

    def call(self, tool_name: str, params: dict) -> dict:
        self.calls.append((tool_name, params))
        return self.responses[tool_name]


def test_data_agent_fetches_order_support_data_in_sequence() -> None:
    client = _FakeMCPClient(
        {
            "get_customer_by_email": {"contactId": "contact-1", "fullName": "John Smith"},
            "get_latest_order": {"orderId": "ord-1", "shipmentId": "ship-1"},
            "get_order_items": {"items": [{"orderItemId": "oi-1"}]},
            "get_shipment_status": {"shipmentId": "ship-1", "status": "Delayed"},
            "get_returns_for_order": {"returns": []},
            "get_refunds_for_order": {"refunds": []},
        }
    )

    result = DataAgent(client).fetch_order_support_data("john.smith@contoso.com")

    assert result["customer"]["contactId"] == "contact-1"
    assert result["order"]["orderId"] == "ord-1"
    assert result["shipment"]["status"] == "Delayed"
    assert result["toolsCalled"] == [
        "get_customer_by_email",
        "get_latest_order",
        "get_order_items",
        "get_shipment_status",
        "get_returns_for_order",
        "get_refunds_for_order",
    ]
    assert client.calls == [
        ("get_customer_by_email", {"email": "john.smith@contoso.com"}),
        ("get_latest_order", {"contact_id": "contact-1"}),
        ("get_order_items", {"order_id": "ord-1"}),
        ("get_shipment_status", {"shipment_id": "ship-1"}),
        ("get_returns_for_order", {"order_id": "ord-1"}),
        ("get_refunds_for_order", {"order_id": "ord-1"}),
    ]


def test_data_agent_stops_when_customer_is_missing() -> None:
    client = _FakeMCPClient(
        {
            "get_customer_by_email": {
                "error": "Customer not found: missing@example.com"
            }
        }
    )

    result = DataAgent(client).fetch_order_support_data("missing@example.com")

    assert result == {
        "error": "Customer not found: missing@example.com",
        "statusCode": 404,
        "toolsCalled": ["get_customer_by_email"],
    }
    assert client.calls == [("get_customer_by_email", {"email": "missing@example.com"})]
