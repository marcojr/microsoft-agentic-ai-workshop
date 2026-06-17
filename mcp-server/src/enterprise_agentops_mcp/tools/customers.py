from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def get_customer_by_email(email: str) -> dict:
    """Find a customer/contact by email address."""
    if DATA_MODE != "mock":
        raise NotImplementedError("Dataverse mode not yet implemented - see Stage 7")

    contacts = load("contacts.json")
    accounts = load("accounts.json")

    contact = next((item for item in contacts if item["email"].lower() == email.lower()), None)
    if contact is None:
        return {"error": f"Customer not found: {email}"}

    account = next((item for item in accounts if item["accountId"] == contact["accountId"]), {})
    return {
        **contact,
        "accountName": account.get("name", ""),
        "riskLevel": account.get("riskLevel", "Unknown"),
    }
