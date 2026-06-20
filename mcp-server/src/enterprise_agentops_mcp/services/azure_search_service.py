from __future__ import annotations

from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from enterprise_agentops_mcp.config import (
    AZURE_AI_SEARCH_ENDPOINT,
    AZURE_AI_SEARCH_INDEX,
    AZURE_AI_SEARCH_KEY,
)


def _require_search_settings() -> None:
    missing = [
        name
        for name, value in (
            ("AZURE_AI_SEARCH_ENDPOINT", AZURE_AI_SEARCH_ENDPOINT),
            ("AZURE_AI_SEARCH_KEY", AZURE_AI_SEARCH_KEY),
            ("AZURE_AI_SEARCH_INDEX", AZURE_AI_SEARCH_INDEX),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(
            f"Missing required Azure AI Search settings: {', '.join(missing)}"
        )


def _client() -> SearchClient:
    _require_search_settings()
    return SearchClient(
        endpoint=AZURE_AI_SEARCH_ENDPOINT,
        index_name=AZURE_AI_SEARCH_INDEX,
        credential=AzureKeyCredential(AZURE_AI_SEARCH_KEY),
    )


def search_knowledge(query: str, max_results: int = 3) -> list[dict[str, Any]]:
    results = _client().search(
        search_text=query,
        top=max_results,
        include_total_count=True,
    )

    mapped: list[dict[str, Any]] = []
    for result in results:
        score = float(result.get("@search.score", 0.0))
        mapped.append(
            {
                "articleId": result.get("id", ""),
                "title": result.get("title", ""),
                "category": result.get("category", ""),
                "summary": str(result.get("content", ""))[:400],
                "confidence": round(min(0.99, 0.45 + score / 4), 2),
                "source": result.get("source", ""),
                "riskCategory": result.get("riskCategory", ""),
            }
        )

    return mapped
