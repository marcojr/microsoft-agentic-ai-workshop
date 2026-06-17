from enterprise_agentops_mcp.tools.knowledge import search_knowledge_articles


def test_search_knowledge_articles_found() -> None:
    result = search_knowledge_articles("delivery delay compensation", max_results=3)
    assert len(result["results"]) >= 1


def test_search_knowledge_articles_empty() -> None:
    result = search_knowledge_articles("unfindable phrase", max_results=3)
    assert result["results"] == []
