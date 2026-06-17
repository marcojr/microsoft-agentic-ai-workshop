from enterprise_agentops_mcp.tools.returns import get_refunds_for_order, get_returns_for_order


def test_get_returns_for_order_found() -> None:
    result = get_returns_for_order("ord-1001")
    assert len(result["returns"]) == 1


def test_get_refunds_for_order_found() -> None:
    result = get_refunds_for_order("ord-1001")
    assert len(result["refunds"]) == 1
