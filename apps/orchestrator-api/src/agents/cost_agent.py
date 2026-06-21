from src.shared.mcp_client import MCPClient


class CostAgent:
    """Calculates LLM run cost through the governed MCP cost tool."""

    def __init__(self, mcp_client: MCPClient | None = None) -> None:
        # Step 1: Use MCP as the boundary for cost/pricing logic.
        self.mcp = mcp_client or MCPClient()

    def calculate_run_cost(
        self,
        *,
        vendor: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> dict:
        # Step 1: Delegate pricing calculation to the MCP cost tool.
        result = self.mcp.call(
            "calculate_agent_run_cost",
            {
                "vendor": vendor,
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            },
        )

        # Step 2: Preserve tool metadata for telemetry.
        return {
            **result,
            "toolsCalled": ["calculate_agent_run_cost"],
        }
