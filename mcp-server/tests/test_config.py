from enterprise_agentops_mcp import config


def test_data_mode_setting_exists() -> None:
    assert hasattr(config, "DATA_MODE")


def test_dataverse_service_principal_settings_exist() -> None:
    assert hasattr(config, "DATAVERSE_SP_CLIENT_ID")
    assert hasattr(config, "DATAVERSE_SP_CLIENT_SECRET")
    assert hasattr(config, "DATAVERSE_SP_TENANT_ID")


def test_ai_provider_settings_exist() -> None:
    assert hasattr(config, "GEMINI_API_KEY")
    assert hasattr(config, "AI_PRIMARY_PROVIDER")
    assert hasattr(config, "AI_PRIMARY_MODEL")
    assert hasattr(config, "AI_SECONDARY_PROVIDER")
    assert hasattr(config, "AI_SECONDARY_MODEL")
    assert hasattr(config, "AZURE_OPENAI_ENDPOINT")
    assert hasattr(config, "AZURE_OPENAI_API_KEY")
    assert hasattr(config, "AZURE_OPENAI_DEPLOYMENT_NAME")
