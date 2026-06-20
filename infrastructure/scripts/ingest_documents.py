from __future__ import annotations

import os
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv


def require(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def infer_risk_category(filename: str) -> str:
    lowered = filename.lower()
    if "approval" in lowered or "compensation" in lowered:
        return "High"
    if "security" in lowered or "privacy" in lowered:
        return "High"
    if "refund" in lowered or "sla" in lowered:
        return "Medium"
    return "Low"


repo_root = Path(__file__).resolve().parents[2]
load_dotenv(repo_root / "mcp-server" / ".env")
docs_path = repo_root / "data" / "sample-documents"

endpoint = require("AZURE_AI_SEARCH_ENDPOINT")
key = require("AZURE_AI_SEARCH_KEY")
index_name = os.getenv("AZURE_AI_SEARCH_INDEX", "enterprise-knowledge")

client = SearchClient(endpoint, index_name, AzureKeyCredential(key))

documents = []
for doc_file in sorted(docs_path.glob("*.md")):
    content = doc_file.read_text(encoding="utf-8")
    documents.append(
        {
            "id": doc_file.stem,
            "title": doc_file.stem.replace("-", " ").title(),
            "content": content,
            "category": "Policy",
            "source": doc_file.name,
            "riskCategory": infer_risk_category(doc_file.name),
        }
    )

if not documents:
    raise RuntimeError(f"No markdown documents found in {docs_path}")

results = client.merge_or_upload_documents(documents)
failed = [item for item in results if not item.succeeded]
if failed:
    raise RuntimeError(f"Failed to ingest some documents: {failed}")

print(f"Ingested {len(documents)} documents into {index_name}")
