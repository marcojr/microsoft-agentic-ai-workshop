from src.shared.mcp_client import MCPClient


def test_mcp_client_lists_registered_tool_names() -> None:
    tool_names = MCPClient().list_tool_names()

    assert "get_customer_by_email" in tool_names
    assert "get_latest_order" in tool_names
    assert "get_shipment_status" in tool_names
    assert "list_pending_approval_requests" in tool_names
    assert "decide_approval_request" in tool_names
