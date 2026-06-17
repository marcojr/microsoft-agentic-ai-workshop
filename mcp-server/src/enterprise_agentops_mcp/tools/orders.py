from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def get_latest_order(contact_id: str) -> dict:
    """Retrieve the most recent order for a contact."""
    if DATA_MODE != "mock":
        raise NotImplementedError("Dataverse mode not yet implemented - see Stage 7")

    orders = load("orders.json")
    contact_orders = [item for item in orders if item["contactId"] == contact_id]
    if not contact_orders:
        return {"error": f"No orders found for contact: {contact_id}"}

    return sorted(contact_orders, key=lambda item: item["orderDate"], reverse=True)[0]


@router.tool()
def get_order_details(order_id: str) -> dict:
    """Retrieve order header and key metadata."""
    if DATA_MODE != "mock":
        raise NotImplementedError("Dataverse mode not yet implemented - see Stage 7")

    orders = load("orders.json")
    order = next((item for item in orders if item["orderId"] == order_id), None)
    if order is None:
        return {"error": f"Order not found: {order_id}"}

    return order


@router.tool()
def get_order_items(order_id: str) -> dict:
    """Retrieve all line items for an order."""
    if DATA_MODE != "mock":
        raise NotImplementedError("Dataverse mode not yet implemented - see Stage 7")

    items = load("order_items.json")
    return {"orderId": order_id, "items": [item for item in items if item["orderId"] == order_id]}
