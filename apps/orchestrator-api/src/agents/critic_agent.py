from src.shared.mcp_client import MCPClient


class CriticAgent:
    """Evaluates generated responses through the governed MCP evaluation tool."""

    def __init__(self, mcp_client: MCPClient | None = None) -> None:
        # Step 1: Use MCP as the boundary for evaluation and scoring.
        self.mcp = mcp_client or MCPClient()

    def evaluate_order_support_summary(
        self,
        *,
        summary: str,
        order: dict,
        shipment: dict,
        risk: str,
    ) -> dict:
        # Step 1: Build source references used for groundedness checks.
        required_sources = [
            source_id
            for source_id in [order.get("orderId"), shipment.get("shipmentId")]
            if source_id
        ]

        # Step 2: Delegate scoring to the MCP evaluation tool.
        result = self.mcp.call(
            "evaluate_response",
            {
                "response": summary,
                "required_sources": required_sources,
                "risk_level": risk,
            },
        )

        # Step 3: Preserve tool metadata for telemetry.
        return {
            **result,
            "requiredSources": required_sources,
            "toolsCalled": ["evaluate_response"],
        }
