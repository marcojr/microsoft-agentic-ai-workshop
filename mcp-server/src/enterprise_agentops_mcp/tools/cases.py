from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def get_open_cases(account_id: str) -> dict:
    """Retrieve all open support cases for an account."""
    if DATA_MODE != "mock":
        raise NotImplementedError("Dataverse mode not yet implemented - see Stage 7")

    cases = load("cases.json")
    open_cases = [
        item for item in cases if item["accountId"] == account_id and item["status"] == "Open"
    ]
    return {"accountId": account_id, "openCases": open_cases}


@router.tool()
def get_case_details(case_id: str) -> dict:
    """Retrieve full support case details including activities."""
    if DATA_MODE != "mock":
        raise NotImplementedError("Dataverse mode not yet implemented - see Stage 7")

    cases = load("cases.json")
    activities = load("activities.json")
    support_case = next((item for item in cases if item["caseId"] == case_id), None)
    if support_case is None:
        return {"error": f"Case not found: {case_id}"}

    return {
        **support_case,
        "activities": [item for item in activities if item["regardingId"] == case_id],
    }
