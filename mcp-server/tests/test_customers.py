from enterprise_agentops_mcp.tools.customers import get_customer_by_email


def test_get_customer_by_email_found() -> None:
    result = get_customer_by_email("john.smith@contoso.com")
    assert result["contactId"] == "con-001"
    assert result["accountName"] == "Contoso Ltd"


def test_get_customer_by_email_missing() -> None:
    result = get_customer_by_email("nobody@example.com")
    assert "error" in result
