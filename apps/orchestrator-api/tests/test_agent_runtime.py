import pytest

from src.shared.agent_runtime import AzureOpenAIAgentRuntime


def test_agent_runtime_requires_azure_openai_endpoint(monkeypatch) -> None:
    from enterprise_agentops_mcp import config

    monkeypatch.setattr(config, "AZURE_OPENAI_ENDPOINT", "")
    monkeypatch.setattr(config, "AZURE_OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(config, "AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini")

    with pytest.raises(ValueError, match="AZURE_OPENAI_ENDPOINT"):
        AzureOpenAIAgentRuntime()


def test_agent_runtime_builds_agent_framework_client(monkeypatch) -> None:
    from enterprise_agentops_mcp import config

    monkeypatch.setattr(config, "AZURE_OPENAI_ENDPOINT", "https://example.openai.azure.com")
    monkeypatch.setattr(config, "AZURE_OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(config, "AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini")

    runtime = AzureOpenAIAgentRuntime()
    client = runtime.build_agent_framework_client()

    assert client is not None
