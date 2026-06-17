from enterprise_agentops_mcp.tools.observability import log_agent_run


def test_log_agent_run() -> None:
    result = log_agent_run(
        workflow_name="WebshopOrderSupport",
        intent="SummariseLatestOrderIssue",
        model_used="gpt-4.1-mini",
        vendor="OpenAI",
        input_tokens=1800,
        output_tokens=450,
        latency_ms=3200,
        tools_called=["get_customer_by_email", "get_latest_order"],
        requires_approval=True,
        risk_score=0.82,
        quality_score=0.88,
        groundedness_score=0.91,
    )
    assert result["logged"] is True
    assert result["runId"].startswith("run-")
