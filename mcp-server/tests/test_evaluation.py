from enterprise_agentops_mcp.tools.evaluation import evaluate_response


def test_evaluate_response_approved() -> None:
    result = evaluate_response(
        response="Approval is required before actioning this high-risk delay case. Sources were reviewed and included.",
        required_sources=["ord-1001", "ship-9001"],
        risk_level="High",
    )
    assert result["approvedForUser"] is True


def test_evaluate_response_not_approved() -> None:
    result = evaluate_response(
        response="Too short.",
        required_sources=[],
        risk_level="High",
    )
    assert result["approvedForUser"] is False
