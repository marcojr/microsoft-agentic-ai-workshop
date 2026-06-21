from src.shared.mcp_client import MCPClient


class DataAgent:
    """Retrieves deterministic order-support data through MCP tools."""

    def __init__(self, mcp_client: MCPClient | None = None) -> None:
        # Step 1: Use the governed MCP client as the only business-data boundary.
        self.mcp = mcp_client or MCPClient()

    def fetch_order_support_data(self, customer_email: str) -> dict:
        # Step 1: Resolve the customer record from the provided email.
        customer = self.mcp.call("get_customer_by_email", {"email": customer_email})
        tools_called = ["get_customer_by_email"]
        if "error" in customer:
            return {"error": customer["error"], "statusCode": 404, "toolsCalled": tools_called}

        # Step 2: Retrieve the latest order for the resolved customer.
        order = self.mcp.call("get_latest_order", {"contact_id": customer["contactId"]})
        tools_called.append("get_latest_order")
        if "error" in order:
            return {"error": order["error"], "statusCode": 404, "toolsCalled": tools_called}

        # Step 3: Gather all deterministic order context needed by later agents.
        order_items = self.mcp.call("get_order_items", {"order_id": order["orderId"]})
        shipment = self.mcp.call("get_shipment_status", {"shipment_id": order["shipmentId"]})
        returns = self.mcp.call("get_returns_for_order", {"order_id": order["orderId"]})
        refunds = self.mcp.call("get_refunds_for_order", {"order_id": order["orderId"]})
        tools_called.extend(
            [
                "get_order_items",
                "get_shipment_status",
                "get_returns_for_order",
                "get_refunds_for_order",
            ]
        )

        # Step 4: Return shaped data so the orchestrator can compose later agents.
        return {
            "customer": customer,
            "order": order,
            "orderItems": order_items,
            "shipment": shipment,
            "returns": returns,
            "refunds": refunds,
            "toolsCalled": tools_called,
        }
