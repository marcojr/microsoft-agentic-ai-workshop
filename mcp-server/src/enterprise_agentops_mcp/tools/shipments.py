from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def get_shipment_status(shipment_id: str) -> dict:
    """Retrieve shipment status and tracking information."""
    if DATA_MODE == "dataverse":
        from enterprise_agentops_mcp.services.dataverse_service import (
            dv_get,
            escape_odata_string,
        )

        rows = dv_get(
            "cr_shipments",
            filter_query=f"cr_shipmentkey eq '{escape_odata_string(shipment_id)}'",
            select="cr_shipmentkey,cr_orderkeyref,cr_carrier,cr_trackingnumber,cr_status,cr_estimateddeliverydate,cr_delivereddate,cr_delayreason,cr_originpostcode,cr_destinationpostcode,cr_routedistancekm",
            top=1,
        )
        if not rows:
            return {"error": f"Shipment not found: {shipment_id}"}

        shipment = rows[0]
        return {
            "shipmentId": shipment.get("cr_shipmentkey", ""),
            "orderId": shipment.get("cr_orderkeyref", ""),
            "carrier": shipment.get("cr_carrier", ""),
            "trackingNumber": shipment.get("cr_trackingnumber", ""),
            "status": shipment.get("cr_status", ""),
            "estimatedDeliveryDate": shipment.get("cr_estimateddeliverydate"),
            "deliveredDate": shipment.get("cr_delivereddate"),
            "delayReason": shipment.get("cr_delayreason"),
            "originPostcode": shipment.get("cr_originpostcode", ""),
            "destinationPostcode": shipment.get("cr_destinationpostcode", ""),
            "routeDistanceKm": shipment.get("cr_routedistancekm"),
        }
    if DATA_MODE != "mock":
        raise ValueError(f"Unsupported MCP_DATA_MODE: {DATA_MODE}")

    shipments = load("shipments.json")
    shipment = next((item for item in shipments if item["shipmentId"] == shipment_id), None)
    if shipment is None:
        return {"error": f"Shipment not found: {shipment_id}"}

    return shipment
