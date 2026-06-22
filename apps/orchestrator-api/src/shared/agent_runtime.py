from agent_framework.azure import AzureOpenAIChatClient


class AzureOpenAIAgentRuntime:
    """Builds Azure OpenAI runtime objects for Microsoft Agent Framework agents."""

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

    def build_agent_framework_client(self) -> AzureOpenAIChatClient:
        # Step 3: Build the Microsoft Agent Framework client.
        return AzureOpenAIChatClient(
            deployment_name=self.deployment,
            api_key=self.api_key,
            endpoint=self.endpoint,
            api_version=self.api_version,
        )
