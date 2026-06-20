from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def get_latest_order(contact_id: str) -> dict:
    """Retrieve the most recent order for a contact."""
    if DATA_MODE == "dataverse":
        from enterprise_agentops_mcp.services.dataverse_service import dv_get

        orders = dv_get(
            "cr_orders",
            filter_query=f"cr_contactid eq '{contact_id}'",
            select="cr_orderkey,cr_ordernumber,cr_accountid,cr_contactid,cr_orderdate,cr_status,cr_totalamount,cr_paymentstatus,cr_deliverystatus,cr_shipmentkeyref,cr_risklevel,cr_deliveryaddress,cr_deliverypostcode",
            orderby="cr_orderdate desc",
            top=1,
        )
        if not orders:
            return {"error": f"No orders found for contact: {contact_id}"}

        return _map_order_row(orders[0])
    if DATA_MODE != "mock":
        raise ValueError(f"Unsupported MCP_DATA_MODE: {DATA_MODE}")

    orders = load("orders.json")
    contact_orders = [item for item in orders if item["contactId"] == contact_id]
    if not contact_orders:
        return {"error": f"No orders found for contact: {contact_id}"}

    return sorted(contact_orders, key=lambda item: item["orderDate"], reverse=True)[0]


@router.tool()
def get_order_details(order_id: str) -> dict:
    """Retrieve order header and key metadata."""
    if DATA_MODE == "dataverse":
        from enterprise_agentops_mcp.services.dataverse_service import dv_get

        orders = dv_get(
            "cr_orders",
            filter_query=f"cr_orderkey eq '{order_id}'",
            select="cr_orderkey,cr_ordernumber,cr_accountid,cr_contactid,cr_orderdate,cr_status,cr_totalamount,cr_paymentstatus,cr_deliverystatus,cr_shipmentkeyref,cr_risklevel,cr_deliveryaddress,cr_deliverypostcode",
            top=1,
        )
        if not orders:
            return {"error": f"Order not found: {order_id}"}

        return _map_order_row(orders[0])
    if DATA_MODE != "mock":
        raise ValueError(f"Unsupported MCP_DATA_MODE: {DATA_MODE}")

    orders = load("orders.json")
    order = next((item for item in orders if item["orderId"] == order_id), None)
    if order is None:
        return {"error": f"Order not found: {order_id}"}

    return order


@router.tool()
def get_order_items(order_id: str) -> dict:
    """Retrieve all line items for an order."""
    if DATA_MODE == "dataverse":
        from enterprise_agentops_mcp.services.dataverse_service import dv_get

        rows = dv_get(
            "cr_orderitems",
            filter_query=f"cr_orderkeyref eq '{order_id}'",
            select="cr_orderitemkey,cr_orderkeyref,cr_productname,cr_sku,cr_quantity,cr_unitprice,cr_totalprice",
            orderby="createdon asc",
        )
        return {
            "orderId": order_id,
            "items": [
                {
                    "orderItemId": item.get("cr_orderitemkey", ""),
                    "productName": item.get("cr_productname", ""),
                    "sku": item.get("cr_sku", ""),
                    "quantity": item.get("cr_quantity", 0),
                    "unitPrice": item.get("cr_unitprice", 0),
                    "totalPrice": item.get("cr_totalprice", 0),
                }
                for item in rows
            ],
        }
    if DATA_MODE != "mock":
        raise ValueError(f"Unsupported MCP_DATA_MODE: {DATA_MODE}")

    items = load("order_items.json")
    return {"orderId": order_id, "items": [item for item in items if item["orderId"] == order_id]}


def _map_order_row(row: dict) -> dict:
    return {
        "orderId": row.get("cr_orderkey", ""),
        "orderNumber": row.get("cr_ordernumber", ""),
        "accountId": row.get("cr_accountid", ""),
        "contactId": row.get("cr_contactid", ""),
        "orderDate": row.get("cr_orderdate"),
        "status": row.get("cr_status"),
        "totalAmount": row.get("cr_totalamount"),
        "paymentStatus": row.get("cr_paymentstatus"),
        "deliveryStatus": row.get("cr_deliverystatus"),
        "shipmentId": row.get("cr_shipmentkeyref", ""),
        "riskLevel": row.get("cr_risklevel"),
        "deliveryAddress": row.get("cr_deliveryaddress", ""),
        "deliveryPostcode": row.get("cr_deliverypostcode", ""),
    }
