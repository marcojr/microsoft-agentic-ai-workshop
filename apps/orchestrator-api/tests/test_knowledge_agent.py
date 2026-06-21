from src.agents.knowledge_agent import KnowledgeAgent


class _FakeMCPClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def call(self, tool_name: str, params: dict) -> dict:
        self.calls.append((tool_name, params))
        return {
            "query": params["query"],
            "results": [{"articleId": "ka-1", "title": "Delivery Delay Policy"}],
        }


def test_knowledge_agent_builds_contextual_order_support_query() -> None:
    client = _FakeMCPClient()

    result = KnowledgeAgent(client).search_order_support_knowledge(
        shipment={"status": "Delayed"},
        refunds={"refunds": [{"requiresApproval": True}]},
        returns={"returns": [{"returnId": "ret-1"}]},
        intake={"intent": "Investigate delayed order status"},
        risk="High",
    )

    query = client.calls[0][1]["query"]
    assert "delayed shipment" in query
    assert "refund" in query
    assert "approval" in query
    assert "return" in query
    assert "high" in query
    assert "Investigate delayed order status" in query
    assert result["toolsCalled"] == ["search_knowledge_articles"]
    assert result["results"][0]["articleId"] == "ka-1"


def test_knowledge_agent_uses_mcp_search_tool() -> None:
    client = _FakeMCPClient()

    KnowledgeAgent(client).search_order_support_knowledge(
        shipment={"status": "In Transit"},
        refunds={"refunds": []},
        returns={"returns": []},
        intake={},
        risk="Medium",
        max_results=5,
    )

    assert client.calls == [
        (
            "search_knowledge_articles",
            {
                "query": "delivery order support policy medium risk",
                "max_results": 5,
            },
        )
    ]
