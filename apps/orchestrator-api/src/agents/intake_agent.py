import json

from agent_framework import Agent
from pydantic import BaseModel

from src.shared.mcp_client import MCPClient
from src.shared.agent_runtime import AzureOpenAIAgentRuntime


class IntakeClassificationContract(BaseModel):
    intent: str
    businessDomain: str
    urgency: str
    toolsRequired: list[str]
    riskLevel: str
    approvalLikelihood: str
    contactEmail: str | None
    orderReference: str | None


class IntakeAgent:
    """Classifies incoming support requests with Microsoft Agent Framework."""

    def __init__(self) -> None:
        mcp_client = MCPClient()

        # Step 1: Load the registered MCP tool names so the model cannot invent systems.
        self.allowed_tool_names = mcp_client.list_tool_names()

        # Step 2: Create the shared Azure OpenAI runtime for Agent Framework.
        runtime = AzureOpenAIAgentRuntime()
        self.client = runtime.build_agent_framework_client()

        # Step 3: Build the intake agent with strict JSON-only instructions.
        self.agent = Agent(
            client=self.client,
            name="IntakeAgent",
            instructions=self._build_instructions(self.allowed_tool_names),
        )

    @staticmethod
    def _build_instructions(allowed_tool_names: list[str]) -> str:
        allowed_tools_text = "\n".join(f"- {name}" for name in allowed_tool_names)
        return f"""
You are an enterprise AI intake agent.
Classify incoming support requests and output ONLY valid JSON that matches the response schema.

Return this schema exactly:
{{
  "intent": "what the user wants to achieve",
  "businessDomain": "CustomerService | Logistics | Finance | HR | Legal",
  "urgency": "Low | Medium | High",
  "toolsRequired": ["exact registered MCP tool names only"],
  "riskLevel": "Low | Medium | High",
  "approvalLikelihood": "Low | Medium | High",
  "contactEmail": "email if provided or null",
  "orderReference": "order ref if mentioned or null"
}}

For toolsRequired, choose only exact tool names from this registered MCP tool list:
{allowed_tools_text}

Do not return business system names, categories, descriptions, or paraphrases.
""".strip()

    async def classify_request(self, user_message: str) -> dict:
        # Step 1: Require a real user message before spending an LLM call.
        if not user_message.strip():
            raise ValueError("user_message is required.")

        # Step 2: Run the Microsoft Agent Framework agent with a typed output contract.
        response = await self.agent.run(
            user_message,
            options={"response_format": IntakeClassificationContract},
        )

        # Step 3: Extract the text payload returned by the agent runtime.
        content = response.text.strip()
        if not content:
            raise ValueError("Intake agent returned an empty response.")

        # Step 4: Validate the structured JSON contract returned by the model.
        result = self._parse_contract(
            content,
            allowed_tool_names=getattr(self, "allowed_tool_names", None),
        )

        # Step 5: Return a plain dict so the orchestrator can consume the result easily.
        return result.model_dump()

    @staticmethod
    def _parse_contract(
        content: str,
        allowed_tool_names: list[str] | None = None,
    ) -> IntakeClassificationContract:
        # Step 1: Parse the raw JSON text returned by the model.
        data = json.loads(content)

        # Step 2: Validate the payload against the intake classification schema.
        contract = IntakeClassificationContract.model_validate(data)

        # Step 3: Reject hallucinated tool names when a registry is available.
        if allowed_tool_names is not None:
            allowed = set(allowed_tool_names)
            unknown_tools = [
                tool_name
                for tool_name in contract.toolsRequired
                if tool_name not in allowed
            ]
            if unknown_tools:
                raise ValueError(
                    "Intake agent returned unknown MCP tools: "
                    + ", ".join(sorted(unknown_tools))
                )

        return contract
