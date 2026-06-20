import json

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.functions import KernelArguments


class DraftAgent:
    """Generates grounded customer-support summaries with Azure OpenAI."""

    def __init__(self) -> None:
        from enterprise_agentops_mcp import config

        # Step 1: Read Azure OpenAI settings from the project configuration.
        endpoint = config.AZURE_OPENAI_ENDPOINT.rstrip("/")
        api_key = config.AZURE_OPENAI_API_KEY
        deployment = config.AZURE_OPENAI_DEPLOYMENT_NAME

        # Step 2: Fail fast when required configuration is missing.
        if not endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT is required.")
        if not api_key:
            raise ValueError("AZURE_OPENAI_API_KEY is required.")
        if not deployment:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME is required.")

        # Step 3: Create the Semantic Kernel instance used only by this comparison agent.
        self.kernel = Kernel()

        # Step 4: Register Azure OpenAI as the chat completion service.
        self.kernel.add_service(
            AzureChatCompletion(
                service_id="azure-openai",
                deployment_name=deployment,
                endpoint=endpoint,
                api_key=api_key,
                api_version="2024-10-21",
            )
        )

        # Step 5: Configure GPT-5-compatible execution settings.
        self.settings = AzureChatPromptExecutionSettings(
            service_id="azure-openai",
            max_completion_tokens=1600,
            reasoning_effort="low",
        )

    async def generate_summary(
        self,
        *,
        customer: dict,
        order: dict,
        shipment: dict,
        refunds: list[dict],
        returns: list[dict],
        knowledge: list[dict],
        risk: str,
    ) -> dict:
        # Step 1: Define the model instructions for a safe, grounded support summary.
        prompt = """
You are an enterprise order support agent.

Write a concise, factual support summary grounded only in the provided data.
Mention approval needs when present.
Never promise compensation before approval is complete.

Customer/order context:
{{$context_json}}
"""

        # Step 2: Build the grounded context passed to the model.
        # The model should only reason over this prepared business data.
        context = {
            "customer": {
                "name": customer["fullName"],
                "email": customer["email"],
            },
            "order": {
                "number": order["orderNumber"],
                "deliveryStatus": order["deliveryStatus"],
                "status": order["status"],
            },
            "shipment": shipment,
            "refunds": refunds,
            "returns": returns,
            "knowledge": knowledge,
            "risk": risk,
        }

        # Step 3: Invoke Semantic Kernel with the prompt, context and Azure OpenAI settings.
        result = await self.kernel.invoke_prompt(
            prompt,
            arguments=KernelArguments(
                context_json=json.dumps(context, indent=2),
                settings=self.settings,
            ),
        )

        # Step 4: Fail fast if Semantic Kernel returned nothing.
        if result is None:
            raise ValueError("Semantic Kernel returned no result.")

        # Step 5: Convert the model result into the support summary text.
        content = str(result).strip()
        if not content:
            raise ValueError("Semantic Kernel returned an empty summary.")

        # Step 6: Extract token usage and model metadata for AgentOps telemetry.
        inner = result.get_inner_content()
        usage = getattr(inner, "usage", None)
        return {
            "summary": content,
            "inputTokens": getattr(usage, "prompt_tokens", 0),
            "outputTokens": getattr(usage, "completion_tokens", 0),
            "model": getattr(inner, "model", "gpt-5-mini"),
        }
