from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE, KNOWLEDGE_MODE
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def search_knowledge_articles(query: str, max_results: int = 3) -> dict:
    """Search internal policy documents and knowledge articles."""
    if KNOWLEDGE_MODE == "search":
        from enterprise_agentops_mcp.services.azure_search_service import search_knowledge

        return {"query": query, "results": search_knowledge(query, max_results=max_results)}
    if KNOWLEDGE_MODE != "mock":
        raise ValueError(f"Unsupported MCP_KNOWLEDGE_MODE: {KNOWLEDGE_MODE}")
    if DATA_MODE != "mock" and KNOWLEDGE_MODE == "mock":
        raise RuntimeError(
            "Knowledge mode is mock while MCP_DATA_MODE is live. Configure MCP_KNOWLEDGE_MODE=search."
        )

    articles = load("knowledge_articles.json")
    terms = [term for term in query.lower().split() if term]
    results = []
    for article in articles:
        haystack = f"{article['title']} {article['content']} {article['category']}".lower()
        score = sum(1 for term in terms if term in haystack)
        if score == 0:
            continue
        results.append(
            {
                "articleId": article["articleId"],
                "title": article["title"],
                "category": article["category"],
                "summary": article["content"][:300],
                "confidence": round(min(0.99, 0.55 + score * 0.12), 2),
                "source": article["title"],
            }
        )

    results.sort(key=lambda item: item["confidence"], reverse=True)
    return {"query": query, "results": results[:max_results]}
