import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MCP_SRC = ROOT / "mcp-server" / "src"
if str(MCP_SRC) not in sys.path:
    sys.path.insert(0, str(MCP_SRC))

from src.webshop_order_support import handle_webshop_order_support


def test_handle_webshop_order_support_success(monkeypatch) -> None:
    from enterprise_agentops_mcp.services import service_bus_service
    from enterprise_agentops_mcp import config
    import src.webshop_order_support as workflow

    published_events = []
    config.DATA_MODE = "mock"
    config.KNOWLEDGE_MODE = "mock"
    monkeypatch.setattr(
        workflow,
        "classify_order_support_request",
        lambda _message: {
            "intent": "SummariseLatestOrderDeliveryStatus",
            "businessDomain": "Logistics",
            "urgency": "High",
            "toolsRequired": [
                "get_customer_by_email",
                "get_latest_order",
                "get_shipment_status",
            ],
            "riskLevel": "High",
            "approvalLikelihood": "Medium",
            "contactEmail": "john.smith@contoso.com",
            "orderReference": None,
        },
    )
    monkeypatch.setattr(
        workflow,
        "generate_order_support_summary",
        lambda **_: {
            "summary": "John Smith's latest order is WEB-1001. Delivery is delayed and refund approval is required.",
            "inputTokens": 100,
            "outputTokens": 30,
            "model": "gpt-5-mini",
        },
    )
    monkeypatch.setattr(
        service_bus_service,
        "send_approval_request_event",
        lambda payload: published_events.append(("approval", payload)),
    )
    monkeypatch.setattr(
        service_bus_service,
        "send_agent_run_event",
        lambda payload: published_events.append(("agent-run", payload)),
    )

    result, status = handle_webshop_order_support(
        {"customerEmail": "john.smith@contoso.com", "userId": "user-001"}
    )
    assert status == 200
    assert result["customerName"] == "John Smith"
    assert result["orderNumber"] == "WEB-1001"
    assert result["approvalRequired"] is True
    assert result["intent"] == "SummariseLatestOrderDeliveryStatus"
    assert result["intake"]["toolsRequired"] == [
        "get_customer_by_email",
        "get_latest_order",
        "get_shipment_status",
    ]
    assert published_events[0][0] == "approval"
    assert published_events[1][0] == "agent-run"
    assert published_events[1][1]["intent"] == "SummariseLatestOrderDeliveryStatus"


def test_handle_webshop_order_support_uses_email_from_intake(monkeypatch) -> None:
    from enterprise_agentops_mcp.services import service_bus_service
    from enterprise_agentops_mcp import config
    import src.webshop_order_support as workflow

    config.DATA_MODE = "mock"
    config.KNOWLEDGE_MODE = "mock"
    monkeypatch.setattr(
        workflow,
        "classify_order_support_request",
        lambda _message: {
            "intent": "SummariseLatestOrderDeliveryStatus",
            "businessDomain": "Logistics",
            "urgency": "High",
            "toolsRequired": ["get_customer_by_email", "get_latest_order"],
            "riskLevel": "High",
            "approvalLikelihood": "Medium",
            "contactEmail": "john.smith@contoso.com",
            "orderReference": None,
        },
    )
    monkeypatch.setattr(
        workflow,
        "generate_order_support_summary",
        lambda **_: {
            "summary": "John Smith's latest order is WEB-1001.",
            "inputTokens": 100,
            "outputTokens": 30,
            "model": "gpt-5-mini",
        },
    )
    monkeypatch.setattr(service_bus_service, "send_approval_request_event", lambda _: None)
    monkeypatch.setattr(service_bus_service, "send_agent_run_event", lambda _: None)

    result, status = handle_webshop_order_support(
        {
            "message": "Can you check the delayed shipment for john.smith@contoso.com?"
        }
    )

    assert status == 200
    assert result["customerName"] == "John Smith"


def test_handle_webshop_order_support_requires_email_or_message() -> None:
    result, status = handle_webshop_order_support({})
    assert status == 400
    assert result["error"] == "customerEmail or message is required"
