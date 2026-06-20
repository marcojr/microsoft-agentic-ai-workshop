from enterprise_agentops_mcp.tools.cost import calculate_agent_run_cost


def test_calculate_agent_run_cost_found() -> None:
    result = calculate_agent_run_cost("Azure OpenAI", "gpt-5-mini", 1800, 450)
    assert result["estimatedCost"] > 0


def test_calculate_agent_run_cost_missing() -> None:
    result = calculate_agent_run_cost("Missing", "missing", 1, 1)
    assert "error" in result

