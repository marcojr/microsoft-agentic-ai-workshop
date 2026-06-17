from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def get_shipment_status(shipment_id: str) -> dict:
    """Retrieve shipment status and tracking information."""
    if DATA_MODE != "mock":
        raise NotImplementedError("Dataverse mode not yet implemented - see Stage 7")

    shipments = load("shipments.json")
    shipment = next((item for item in shipments if item["shipmentId"] == shipment_id), None)
    if shipment is None:
        return {"error": f"Shipment not found: {shipment_id}"}

    return shipment
