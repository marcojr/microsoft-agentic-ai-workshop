import json

from pydantic import BaseModel
from semantic_kernel.functions import KernelArguments

from src.shared.agent_runtime import AzureOpenAIAgentRuntime


class DraftSummaryContract(BaseModel):
    summary: str
    approvalRequired: bool


class DraftAgent:
    """Generates grounded customer-support summaries with Azure OpenAI."""

    def __init__(self) -> None:
        # Step 1: Create the shared Azure OpenAI runtime for Semantic Kernel.
        runtime = AzureOpenAIAgentRuntime()

        # Step 2: Build the Semantic Kernel comparison-agent runtime.
        self.kernel = runtime.build_semantic_kernel()

        # Step 3: Configure GPT-5-compatible structured output settings.
        self.settings = runtime.build_semantic_kernel_settings(
            response_format=DraftSummaryContract,
            structured_json_response=True,
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
        # Step 1: Define the model instructions for a safe, grounded structured response.
        prompt = """
You are an enterprise order support agent.

Return ONLY valid JSON that matches the provided response schema.

The JSON must include:
- summary: a concise factual support summary
- approvalRequired: true when refunds or compensation require approval

Rules:
- Ground every field only in the provided data
- Mention approval needs when present
- Never promise compensation before approval is complete

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
                "id": order.get("orderId"),
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

        # Step 5: Read the raw structured JSON returned by the model.
        content = str(result).strip()
        if not content:
            raise ValueError("Semantic Kernel returned an empty summary.")

        # Step 6: Validate the response against the didactic output contract.
        contract = self._parse_contract(content)

        # Step 7: Extract token usage and model metadata for AgentOps telemetry.
        inner = result.get_inner_content()
        usage = getattr(inner, "usage", None)
        return {
            "summary": contract.summary,
            "approvalRequired": contract.approvalRequired,
            "inputTokens": getattr(usage, "prompt_tokens", 0),
            "outputTokens": getattr(usage, "completion_tokens", 0),
            "model": getattr(inner, "model", "gpt-5-mini"),
        }

    @staticmethod
    def _parse_contract(content: str) -> DraftSummaryContract:
        # Step 1: Parse the raw JSON text exactly as returned by the model.
        data = json.loads(content)

        # Step 2: Validate the contract so downstream code sees typed fields.
        return DraftSummaryContract.model_validate(data)
