from __future__ import annotations

import os
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchFieldDataType,
    SearchIndex,
    SearchableField,
    SimpleField,
)
from dotenv import load_dotenv


repo_root = Path(__file__).resolve().parents[2]
load_dotenv(repo_root / "mcp-server" / ".env")


def require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


endpoint = require("AZURE_AI_SEARCH_ENDPOINT")
key = require("AZURE_AI_SEARCH_KEY")
index_name = os.getenv("AZURE_AI_SEARCH_INDEX", "enterprise-knowledge")

client = SearchIndexClient(endpoint, AzureKeyCredential(key))

index = SearchIndex(
    name=index_name,
    fields=[
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="title", type=SearchFieldDataType.String),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="category", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="source", type=SearchFieldDataType.String),
        SimpleField(
            name="riskCategory",
            type=SearchFieldDataType.String,
            filterable=True,
        ),
    ],
)

client.create_or_update_index(index)
print(f"Index created or updated: {index_name}")
