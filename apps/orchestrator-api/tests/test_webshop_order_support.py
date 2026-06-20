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
    assert published_events[0][0] == "approval"
    assert published_events[1][0] == "agent-run"


def test_handle_webshop_order_support_requires_email() -> None:
    result, status = handle_webshop_order_support({})
    assert status == 400
    assert result["error"] == "customerEmail is required"
