from enterprise_agentops_mcp.tools.accounts import get_account_by_name


def test_get_account_by_name_found() -> None:
    result = get_account_by_name("Contoso")
    assert result["accountId"] == "acc-001"


def test_get_account_by_name_missing() -> None:
    result = get_account_by_name("Missing Corp")
    assert "error" in result
