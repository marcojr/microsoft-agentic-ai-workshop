from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def get_returns_for_order(order_id: str) -> dict:
    """Retrieve return requests linked to an order."""
    if DATA_MODE != "mock":
        raise NotImplementedError("Dataverse mode not yet implemented - see Stage 7")

    returns = load("returns.json")
    return {"orderId": order_id, "returns": [item for item in returns if item["orderId"] == order_id]}


@router.tool()
def get_refunds_for_order(order_id: str) -> dict:
    """Retrieve refund records linked to an order."""
    if DATA_MODE != "mock":
        raise NotImplementedError("Dataverse mode not yet implemented - see Stage 7")

    refunds = load("refunds.json")
    return {"orderId": order_id, "refunds": [item for item in refunds if item["orderId"] == order_id]}
