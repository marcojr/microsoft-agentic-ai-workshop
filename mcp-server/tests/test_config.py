from enterprise_agentops_mcp import config


def test_default_data_mode_is_mock() -> None:
    assert config.DATA_MODE == "mock"


def test_dataverse_service_principal_settings_exist() -> None:
    assert hasattr(config, "DATAVERSE_SP_CLIENT_ID")
    assert hasattr(config, "DATAVERSE_SP_CLIENT_SECRET")
    assert hasattr(config, "DATAVERSE_SP_TENANT_ID")
