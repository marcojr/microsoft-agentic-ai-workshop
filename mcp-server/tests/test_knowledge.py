from enterprise_agentops_mcp.tools.knowledge import search_knowledge_articles
from enterprise_agentops_mcp.tools import knowledge


def test_search_knowledge_articles_found() -> None:
    knowledge.KNOWLEDGE_MODE = "mock"
    result = search_knowledge_articles("delivery delay compensation", max_results=3)
    assert len(result["results"]) >= 1


def test_search_knowledge_articles_empty() -> None:
    knowledge.KNOWLEDGE_MODE = "mock"
    result = search_knowledge_articles("unfindable phrase", max_results=3)
    assert result["results"] == []


def test_search_knowledge_articles_search_mode(monkeypatch) -> None:
    monkeypatch.setattr(knowledge, "KNOWLEDGE_MODE", "search")

    monkeypatch.setattr(
        "enterprise_agentops_mcp.services.azure_search_service.search_knowledge",
        lambda query, max_results=3: [
            {
                "articleId": "approval-rules",
                "title": "Approval Rules",
                "category": "Policy",
                "summary": "Compensation above threshold requires approval.",
                "confidence": 0.91,
                "source": "approval-rules.md",
                "riskCategory": "High",
            }
        ],
    )

    result = search_knowledge_articles("refund approval", max_results=3)

    assert result["query"] == "refund approval"
    assert result["results"][0]["articleId"] == "approval-rules"
