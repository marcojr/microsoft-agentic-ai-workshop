from src.agents.cost_agent import CostAgent


class _FakeMCPClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def call(self, tool_name: str, params: dict) -> dict:
        self.calls.append((tool_name, params))
        return {
            "vendor": params["vendor"],
            "model": params["model"],
            "inputTokens": params["input_tokens"],
            "outputTokens": params["output_tokens"],
            "estimatedCost": 0.000123,
            "currency": "USD",
        }


def test_cost_agent_calculates_run_cost_through_mcp() -> None:
    client = _FakeMCPClient()

    result = CostAgent(client).calculate_run_cost(
        vendor="Azure OpenAI",
        model="gpt-5-mini",
        input_tokens=100,
        output_tokens=30,
    )

    assert result["estimatedCost"] == 0.000123
    assert result["toolsCalled"] == ["calculate_agent_run_cost"]
    assert client.calls == [
        (
            "calculate_agent_run_cost",
            {
                "vendor": "Azure OpenAI",
                "model": "gpt-5-mini",
                "input_tokens": 100,
                "output_tokens": 30,
            },
        )
    ]
