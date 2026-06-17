from enterprise_agentops_mcp.tools.orders import (
    get_latest_order,
    get_order_details,
    get_order_items,
)


def test_get_latest_order_returns_most_recent() -> None:
    result = get_latest_order("con-001")
    assert result["orderId"] == "ord-1001"


def test_get_order_details_found() -> None:
    result = get_order_details("ord-1001")
    assert result["orderNumber"] == "WEB-1001"


def test_get_order_items_found() -> None:
    result = get_order_items("ord-1001")
    assert result["orderId"] == "ord-1001"
    assert len(result["items"]) == 2
