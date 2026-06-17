import uuid
from datetime import datetime, timezone

from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load, save
from enterprise_agentops_mcp.tools.cost import calculate_agent_run_cost

router = FastMCP()


@router.tool()
def log_agent_run(
    workflow_name: str,
    intent: str,
    model_used: str,
    vendor: str,
    input_tokens: int,
    output_tokens: int,
    latency_ms: int,
    tools_called: list[str],
    requires_approval: bool = False,
    risk_score: float = 0.0,
    quality_score: float = 0.0,
    groundedness_score: float = 0.0,
) -> dict:
    """Log agent execution telemetry for observability and cost tracking."""
    if DATA_MODE != "mock":
        raise NotImplementedError("Dataverse mode not yet implemented - see Stage 7")

    cost_result = calculate_agent_run_cost(vendor, model_used, input_tokens, output_tokens)
    if "error" in cost_result:
        raise ValueError(cost_result["error"])

    run_id = f"run-{uuid.uuid4().hex[:8]}"
    run = {
        "runId": run_id,
        "workflowName": workflow_name,
        "intent": intent,
        "modelUsed": model_used,
        "vendorUsed": vendor,
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "status": "Completed",
        "inputTokens": input_tokens,
        "outputTokens": output_tokens,
        "estimatedCost": cost_result["estimatedCost"],
        "latencyMs": latency_ms,
        "toolsCalled": tools_called,
        "requiresApproval": requires_approval,
        "riskScore": risk_score,
        "qualityScore": quality_score,
        "groundednessScore": groundedness_score,
    }

    runs = load("agent_runs.json")
    runs.append(run)
    save("agent_runs.json", runs)

    return {
        "logged": True,
        "runId": run_id,
        "estimatedCost": cost_result["estimatedCost"],
    }
