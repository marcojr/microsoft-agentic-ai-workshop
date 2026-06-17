from fastmcp import FastMCP

from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def calculate_agent_run_cost(vendor: str, model: str, input_tokens: int, output_tokens: int) -> dict:
    """Calculate estimated LLM cost from token usage and model pricing."""
    pricing = load("pricing.json")
    rate = next(
        (item for item in pricing if item["vendor"] == vendor and item["model"] == model),
        None,
    )
    if rate is None:
        return {"error": f"No pricing data found for {vendor}/{model}"}

    total = round(
        (input_tokens / 1_000_000) * rate["inputTokenPricePer1M"]
        + (output_tokens / 1_000_000) * rate["outputTokenPricePer1M"],
        6,
    )
    return {
        "vendor": vendor,
        "model": model,
        "inputTokens": input_tokens,
        "outputTokens": output_tokens,
        "estimatedCost": total,
        "currency": rate["currency"],
    }
