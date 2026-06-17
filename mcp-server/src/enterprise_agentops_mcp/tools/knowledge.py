from fastmcp import FastMCP

from enterprise_agentops_mcp.config import DATA_MODE
from enterprise_agentops_mcp.services.mock_data_service import load

router = FastMCP()


@router.tool()
def search_knowledge_articles(query: str, max_results: int = 3) -> dict:
    """Search internal policy documents and knowledge articles."""
    if DATA_MODE != "mock":
        raise NotImplementedError("Azure AI Search mode not yet implemented - see Stage 8")

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
