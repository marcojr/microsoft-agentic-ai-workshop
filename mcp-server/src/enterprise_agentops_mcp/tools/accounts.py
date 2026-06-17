from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def get_account_by_name(account_name: str) -> dict:
    """Find an account by name."""
    if DATA_MODE != "mock":
        raise NotImplementedError("Dataverse mode not yet implemented - see Stage 7")

    accounts = load("accounts.json")
    account = next(
        (item for item in accounts if account_name.lower() in item["name"].lower()),
        None,
    )
    if account is None:
        return {"error": f"Account not found: {account_name}"}

    return account
