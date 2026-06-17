from enterprise_agentops_mcp.tools.cases import get_case_details, get_open_cases


def test_get_open_cases_found() -> None:
    result = get_open_cases("acc-001")
    assert len(result["openCases"]) == 1


def test_get_case_details_found() -> None:
    result = get_case_details("case-1001")
    assert result["caseId"] == "case-1001"
    assert len(result["activities"]) == 2
