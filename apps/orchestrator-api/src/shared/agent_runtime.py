from typing import Any

from agent_framework.openai import OpenAIChatCompletionClient
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureChatPromptExecutionSettings,
)


class AzureOpenAIAgentRuntime:
    """Builds Azure OpenAI runtime objects for the supported agent frameworks."""

    def __init__(self) -> None:
        from enterprise_agentops_mcp import config

        # Step 1: Read the shared Azure OpenAI configuration once.
        self.endpoint = config.AZURE_OPENAI_ENDPOINT.rstrip("/")
        self.api_key = config.AZURE_OPENAI_API_KEY
        self.deployment = config.AZURE_OPENAI_DEPLOYMENT_NAME
        self.api_version = "2024-10-21"
        self.service_id = "azure-openai"

        # Step 2: Fail fast so agents do not hide broken runtime configuration.
        if not self.endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT is required.")
        if not self.api_key:
            raise ValueError("AZURE_OPENAI_API_KEY is required.")
        if not self.deployment:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME is required.")

    def build_agent_framework_client(self) -> OpenAIChatCompletionClient:
        # Step 3: Build the Microsoft Agent Framework client.
        return OpenAIChatCompletionClient(
            model=self.deployment,
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=self.api_version,
        )

    def build_semantic_kernel(self) -> Kernel:
        # Step 3: Build the Semantic Kernel runtime used by the comparison agent.
        kernel = Kernel()
        kernel.add_service(
            AzureChatCompletion(
                service_id=self.service_id,
                deployment_name=self.deployment,
                endpoint=self.endpoint,
                api_key=self.api_key,
                api_version=self.api_version,
            )
        )
        return kernel

    def build_semantic_kernel_settings(
        self,
        *,
        response_format: type[Any] | None = None,
        max_completion_tokens: int = 1600,
        reasoning_effort: str = "low",
        structured_json_response: bool = False,
    ) -> AzureChatPromptExecutionSettings:
        # Step 4: Build GPT-5-compatible Semantic Kernel execution settings.
        return AzureChatPromptExecutionSettings(
            service_id=self.service_id,
            max_completion_tokens=max_completion_tokens,
            reasoning_effort=reasoning_effort,
            response_format=response_format,
            structured_json_response=structured_json_response,
        )
