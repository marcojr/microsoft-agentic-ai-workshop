from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def get_returns_for_order(order_id: str) -> dict:
    """Retrieve return requests linked to an order."""
    if DATA_MODE == "dataverse":
        from enterprise_agentops_mcp.services.dataverse_service import dv_get

        rows = dv_get(
            "cr_returnrequests",
            filter_query=f"cr_orderkeyref eq '{order_id}'",
            select="cr_returnkey,cr_orderkeyref,cr_orderitemkeyref,cr_reason,cr_status,cr_requesteddate,cr_refundrequired",
            orderby="cr_requesteddate desc",
        )
        return {
            "orderId": order_id,
            "returns": [
                {
                    "returnId": item.get("cr_returnkey", ""),
                    "orderId": item.get("cr_orderkeyref", ""),
                    "orderItemId": item.get("cr_orderitemkeyref", ""),
                    "reason": item.get("cr_reason", ""),
                    "status": item.get("cr_status", ""),
                    "requestedDate": item.get("cr_requesteddate"),
                    "refundRequired": item.get("cr_refundrequired", False),
                }
                for item in rows
            ],
        }
    if DATA_MODE != "mock":
        raise ValueError(f"Unsupported MCP_DATA_MODE: {DATA_MODE}")

    returns = load("returns.json")
    return {"orderId": order_id, "returns": [item for item in returns if item["orderId"] == order_id]}


@router.tool()
def get_refunds_for_order(order_id: str) -> dict:
    """Retrieve refund records linked to an order."""
    if DATA_MODE == "dataverse":
        from enterprise_agentops_mcp.services.dataverse_service import dv_get

        rows = dv_get(
            "cr_refunds",
            filter_query=f"cr_orderkeyref eq '{order_id}'",
            select="cr_refundkey,cr_orderkeyref,cr_returnkeyref,cr_amount,cr_status,cr_reason,cr_requiresapproval,cr_approvedby",
        )
        return {
            "orderId": order_id,
            "refunds": [
                {
                    "refundId": item.get("cr_refundkey", ""),
                    "orderId": item.get("cr_orderkeyref", ""),
                    "returnId": item.get("cr_returnkeyref", ""),
                    "amount": item.get("cr_amount", 0),
                    "status": item.get("cr_status", ""),
                    "reason": item.get("cr_reason", ""),
                    "requiresApproval": item.get("cr_requiresapproval", False),
                    "approvedBy": item.get("cr_approvedby"),
                }
                for item in rows
            ],
        }
    if DATA_MODE != "mock":
        raise ValueError(f"Unsupported MCP_DATA_MODE: {DATA_MODE}")

    refunds = load("refunds.json")
    return {"orderId": order_id, "refunds": [item for item in refunds if item["orderId"] == order_id]}
