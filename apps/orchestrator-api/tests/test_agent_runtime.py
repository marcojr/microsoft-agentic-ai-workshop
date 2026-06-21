import pytest

from src.shared.agent_runtime import AzureOpenAIAgentRuntime


def test_agent_runtime_requires_azure_openai_endpoint(monkeypatch) -> None:
    from enterprise_agentops_mcp import config

    monkeypatch.setattr(config, "AZURE_OPENAI_ENDPOINT", "")
    monkeypatch.setattr(config, "AZURE_OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(config, "AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini")

    with pytest.raises(ValueError, match="AZURE_OPENAI_ENDPOINT"):
        AzureOpenAIAgentRuntime()


def test_agent_runtime_builds_semantic_kernel_settings(monkeypatch) -> None:
    from enterprise_agentops_mcp import config

    monkeypatch.setattr(config, "AZURE_OPENAI_ENDPOINT", "https://example.openai.azure.com")
    monkeypatch.setattr(config, "AZURE_OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(config, "AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini")

    runtime = AzureOpenAIAgentRuntime()
    settings = runtime.build_semantic_kernel_settings(
        max_completion_tokens=123,
        reasoning_effort="low",
        structured_json_response=True,
    )

    assert settings.service_id == "azure-openai"
    assert settings.max_completion_tokens == 123
    assert settings.reasoning_effort == "low"
