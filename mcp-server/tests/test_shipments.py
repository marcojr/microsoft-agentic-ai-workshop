from enterprise_agentops_mcp.tools.shipments import get_shipment_status


def test_get_shipment_status_found() -> None:
    result = get_shipment_status("ship-9001")
    assert result["status"] == "Delayed"


def test_get_shipment_status_missing() -> None:
    result = get_shipment_status("ship-9999")
    assert "error" in result
