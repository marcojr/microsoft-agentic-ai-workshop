import json

from agent_framework import ChatAgent
from pydantic import BaseModel

from src.shared.agent_runtime import AzureOpenAIAgentRuntime


class DraftSummaryContract(BaseModel):
    summary: str
    approvalRequired: bool


class DraftAgent:
    """Generates grounded customer-support summaries with Microsoft Agent Framework."""

    def __init__(self) -> None:
        # Step 1: Create the shared Azure OpenAI runtime for Microsoft Agent Framework.
        runtime = AzureOpenAIAgentRuntime()
        self.client = runtime.build_agent_framework_client()

        # Step 2: Build the draft agent with a typed structured-output contract.
        self.agent = ChatAgent(
            chat_client=self.client,
            name="DraftAgent",
            instructions=self._build_instructions(),
            response_format=DraftSummaryContract,
        )

    @staticmethod
    def _build_instructions() -> str:
        return """
You are an enterprise order support agent.

Return ONLY valid JSON that matches the provided response schema.

The JSON must include:
- summary: a concise factual support summary
- approvalRequired: true when refunds or compensation require approval

Rules:
- Ground every field only in the provided data
- Mention approval needs when present
- Never promise compensation before approval is complete
""".strip()

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
        # Step 1: Build the grounded context passed to the model.
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

        # Step 2: Ask Microsoft Agent Framework to generate the structured summary.
        response = await self.agent.run(
            "Customer/order context:\n" + json.dumps(context, indent=2)
        )

        # Step 3: Read and validate the raw structured JSON returned by the model.
        content = response.text.strip()
        if not content:
            raise ValueError("Draft agent returned an empty summary.")

        contract = self._parse_contract(content)

        # Step 4: Extract metadata when the Agent Framework response exposes it.
        usage = getattr(response, "usage", None)
        return {
            "summary": contract.summary,
            "approvalRequired": contract.approvalRequired,
            "inputTokens": getattr(usage, "prompt_tokens", 0)
            or getattr(usage, "input_tokens", 0),
            "outputTokens": getattr(usage, "completion_tokens", 0)
            or getattr(usage, "output_tokens", 0),
            "model": getattr(response, "model", "gpt-5-mini"),
        }

    @staticmethod
    def _parse_contract(content: str) -> DraftSummaryContract:
        # Step 1: Parse the raw JSON text exactly as returned by the model.
        data = json.loads(content)

        # Step 2: Validate the contract so downstream code sees typed fields.
        return DraftSummaryContract.model_validate(data)
