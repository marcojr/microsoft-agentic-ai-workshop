from enterprise_agentops_mcp.services.mock_data_service import load


def test_load_existing_stub_returns_list() -> None:
    data = load("accounts.json")
    assert isinstance(data, list)


def test_load_missing_file_returns_empty_list() -> None:
    data = load("does-not-exist.json")
    assert data == []
