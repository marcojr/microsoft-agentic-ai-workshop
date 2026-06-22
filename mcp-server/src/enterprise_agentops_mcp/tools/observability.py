import uuid
from datetime import datetime, timezone
import json

from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load, save
from enterprise_agentops_mcp.services.telemetry import flush_telemetry, get_tracer
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
    """Log one completed agent run for dashboards, audit, and Azure telemetry."""
    # Step 1: create an OpenTelemetry span. In Application Insights this appears
    # as the custom dependency named mcp.log_agent_run.
    tracer = get_tracer()
    with tracer.start_as_current_span("mcp.log_agent_run") as span:
        # Step 2: attach the business and operational dimensions that make the
        # run searchable in Azure Monitor Logs.
        span.set_attribute("agentops.workflow_name", workflow_name)
        span.set_attribute("agentops.intent", intent)
        span.set_attribute("agentops.model_used", model_used)
        span.set_attribute("agentops.vendor", vendor)
        span.set_attribute("agentops.input_tokens", input_tokens)
        span.set_attribute("agentops.output_tokens", output_tokens)
        span.set_attribute("agentops.latency_ms", latency_ms)
        span.set_attribute("agentops.requires_approval", requires_approval)
        span.set_attribute("agentops.risk_score", risk_score)
        span.set_attribute("agentops.quality_score", quality_score)
        span.set_attribute("agentops.groundedness_score", groundedness_score)
        span.set_attribute("agentops.tools_called", ",".join(tools_called))

        # Step 3: calculate cost from the same token counts we store for
        # reporting. Unknown vendor/model combinations should fail loudly.
        cost_result = calculate_agent_run_cost(
            vendor,
            model_used,
            input_tokens,
            output_tokens,
        )
        if "error" in cost_result:
            raise ValueError(cost_result["error"])

        run_id = f"run-{uuid.uuid4().hex[:8]}"
        span.set_attribute("agentops.run_id", run_id)
        span.set_attribute("agentops.estimated_cost", cost_result["estimatedCost"])

        # Step 4: build a normalized run record. This structure is used by mock
        # mode and mirrors the fields persisted in Dataverse for Power BI.
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

        # Step 5: persist the run in the active data mode. Dataverse is the real
        # workshop path; mock mode keeps local development quick and inspectable.
        if DATA_MODE == "dataverse":
            from enterprise_agentops_mcp.services.dataverse_service import dv_post

            dv_post(
                "cr_agentruns",
                {
                    "cr_runkey": run["runId"],
                    "cr_workflowname": workflow_name,
                    "cr_intent": intent,
                    "cr_modelused": model_used,
                    "cr_vendorused": vendor,
                    "cr_startedat": run["startedAt"],
                    "cr_status": run["status"],
                    "cr_inputtokens": input_tokens,
                    "cr_outputtokens": output_tokens,
                    "cr_estimatedcost": cost_result["estimatedCost"],
                    "cr_latencyms": latency_ms,
                    "cr_toolscalled": json.dumps(tools_called),
                    "cr_requiresapproval": requires_approval,
                    "cr_riskscore": risk_score,
                    "cr_qualityscore": quality_score,
                    "cr_groundednessscore": groundedness_score,
                },
            )
        elif DATA_MODE == "mock":
            runs = load("agent_runs.json")
            runs.append(run)
            save("agent_runs.json", runs)
        else:
            raise ValueError(f"Unsupported MCP_DATA_MODE: {DATA_MODE}")

        result = {
            "logged": True,
            "runId": run_id,
            "estimatedCost": cost_result["estimatedCost"],
        }
    # Step 6: push telemetry before returning so short Function executions still
    # show up quickly in Application Insights.
    flush_telemetry()
    return result
