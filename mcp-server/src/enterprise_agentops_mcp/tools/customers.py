from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def get_customer_by_email(email: str) -> dict:
    """Find a customer/contact by email address."""
    if DATA_MODE == "dataverse":
        from enterprise_agentops_mcp.services.dataverse_service import (
            dv_get,
            escape_odata_string,
        )

        contacts = dv_get(
            "contacts",
            filter_query=f"emailaddress1 eq '{escape_odata_string(email)}'",
            select="contactid,fullname,emailaddress1,jobtitle,telephone1,_parentcustomerid_value,address1_line1,address1_postalcode",
            top=1,
        )
        if not contacts:
            return {"error": f"Customer not found: {email}"}

        contact = contacts[0]
        account_id = contact.get("_parentcustomerid_value", "")
        account = {}
        if account_id:
            accounts = dv_get(
                "accounts",
                filter_query=f"accountid eq {account_id}",
                select="accountid,name,address1_line1,address1_postalcode",
                top=1,
            )
            if accounts:
                account = accounts[0]

        return {
            "contactId": contact["contactid"],
            "accountId": account_id,
            "fullName": contact.get("fullname", ""),
            "email": contact.get("emailaddress1", ""),
            "role": contact.get("jobtitle", ""),
            "phone": contact.get("telephone1", ""),
            "deliveryAddress": contact.get("address1_line1", ""),
            "deliveryPostcode": contact.get("address1_postalcode", ""),
            "accountName": account.get("name", ""),
            "riskLevel": "Unknown",
        }
    if DATA_MODE != "mock":
        raise ValueError(f"Unsupported MCP_DATA_MODE: {DATA_MODE}")

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
