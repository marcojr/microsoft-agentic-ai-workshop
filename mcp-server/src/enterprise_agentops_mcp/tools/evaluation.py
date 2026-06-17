from fastmcp import FastMCP

router = FastMCP()


@router.tool()
def evaluate_response(response: str, required_sources: list[str], risk_level: str = "Medium") -> dict:
    """Evaluate a generated response for quality, groundedness and policy compliance."""
    issues = []
    if len(response.strip()) < 50:
        issues.append("Response is too short to be useful.")
    if risk_level == "High" and "approval" not in response.lower():
        issues.append("High-risk response must mention that approval is required before actioning.")
    if not required_sources:
        issues.append("No source references provided - groundedness cannot be confirmed.")

    return {
        "qualityScore": round(max(0.3, 0.92 - len(issues) * 0.12), 2),
        "groundednessScore": 0.88 if required_sources else 0.55,
        "riskScore": {"Low": 0.2, "Medium": 0.5, "High": 0.82}.get(risk_level, 0.5),
        "issues": issues,
        "approvedForUser": len(issues) == 0,
    }
