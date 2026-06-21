from src.shared.mcp_client import MCPClient


class KnowledgeAgent:
    """Retrieves policy knowledge for order-support workflows through MCP."""

    def __init__(self, mcp_client: MCPClient | None = None) -> None:
        # Step 1: Use MCP as the governed boundary for knowledge retrieval.
        self.mcp = mcp_client or MCPClient()

    def search_order_support_knowledge(
        self,
        *,
        shipment: dict,
        refunds: dict,
        returns: dict,
        intake: dict,
        risk: str,
        max_results: int = 3,
    ) -> dict:
        # Step 1: Build a grounded search query from the case context.
        query = self._build_order_support_query(
            shipment=shipment,
            refunds=refunds,
            returns=returns,
            intake=intake,
            risk=risk,
        )

        # Step 2: Retrieve matching policy knowledge through the MCP tool layer.
        result = self.mcp.call(
            "search_knowledge_articles",
            {"query": query, "max_results": max_results},
        )

        # Step 3: Preserve query/tool metadata for telemetry and debugging.
        return {
            **result,
            "query": result.get("query", query),
            "toolsCalled": ["search_knowledge_articles"],
        }

    @staticmethod
    def _build_order_support_query(
        *,
        shipment: dict,
        refunds: dict,
        returns: dict,
        intake: dict,
        risk: str,
    ) -> str:
        terms = ["delivery", "order", "support", "policy"]

        if shipment.get("status") == "Delayed":
            terms.extend(["delay", "delayed shipment", "escalation"])

        refund_rows = refunds.get("refunds", [])
        if any(item.get("requiresApproval") for item in refund_rows):
            terms.extend(["refund", "approval", "compensation"])

        return_rows = returns.get("returns", [])
        if return_rows:
            terms.extend(["return", "non delivery"])

        if risk:
            terms.extend([risk.lower(), "risk"])

        intent = intake.get("intent")
        if intent:
            terms.append(intent)

        return " ".join(dict.fromkeys(term for term in terms if term))
