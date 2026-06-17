# Stage 8: Secure RAG (Day 8)

Create policy documents, index them in Azure AI Search, and wire `search_knowledge_articles` to return live results with citations and confidence scores.

---

## Day 8 Deliverables

- [ ] Policy documents created in `data/sample-documents/`
- [ ] Azure AI Search index created
- [ ] Documents ingested with embeddings
- [ ] `search_knowledge_articles` returning real Azure AI Search results
- [ ] Citations, confidence scores and source metadata included
- [ ] Mock fallback retained

---

## Policy Documents to Create

Place in `data/sample-documents/`:

```
customer-compensation-policy.md
delivery-delay-policy.md
refund-policy.md
ai-usage-policy.md
responsible-ai-policy.md
data-privacy-policy.md
security-policy.md
approval-rules.md
customer-service-playbook.md
sla-policy.md
```

### Example: `customer-compensation-policy.md`

```markdown
# Customer Compensation Policy

## Scope
This policy applies to all customer-facing compensation decisions.

## Approval Requirements
- Compensation below £50: approved by team lead
- Compensation £50–£500: requires service manager approval
- Compensation above £500: requires director sign-off
- All external compensation communication must be approved before sending

## Eligibility
Premium customers who experience repeated SLA breaches (2+ incidents in 30 days)
are eligible for compensation credit.

## Process
1. Log the compensation request as an Approval Request
2. Attach relevant order and shipment records
3. Submit for approval via Power Automate flow
4. Only communicate compensation after approval is confirmed
```

---

## Create Azure AI Search (via Pulumi)

Add to `infrastructure/pulumi/resources/aiSearch.ts`:

```typescript
import * as azure from "@pulumi/azure-native";
import { resourceGroup } from "./resourceGroup";
import { suffix } from "../config";

export const searchService = new azure.search.Service("search", {
    resourceGroupName: resourceGroup.name,
    location: resourceGroup.location,
    searchServiceName: `srch-${suffix}`,
    sku: { name: "free" },  // Free tier for dev
});

export const searchEndpoint = searchService.name.apply(
    name => `https://${name}.search.windows.net`
);
```

Or via Azure CLI:
```bash
az search service create \
  --name srch-agentops-dev \
  --resource-group rg-agentops-dev \
  --sku free \
  --location uksouth

az search admin-key show \
  --service-name srch-agentops-dev \
  --resource-group rg-agentops-dev
```

---

## Create Index

**File:** `infrastructure/scripts/create_search_index.py`

```python
import os
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField, SearchField,
    SearchFieldDataType, VectorSearch, HnswAlgorithmConfiguration,
    VectorSearchProfile, SemanticConfiguration, SemanticSearch,
    SemanticPrioritizedFields, SemanticField
)
from azure.core.credentials import AzureKeyCredential

client = SearchIndexClient(
    os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
    AzureKeyCredential(os.getenv("AZURE_AI_SEARCH_KEY"))
)

index = SearchIndex(
    name=os.getenv("AZURE_AI_SEARCH_INDEX", "enterprise-knowledge"),
    fields=[
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="title", type=SearchFieldDataType.String),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="category", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="source", type=SearchFieldDataType.String, retrievable=True),
        SimpleField(name="riskCategory", type=SearchFieldDataType.String, filterable=True),
        SearchField(
            name="contentVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True, vector_search_dimensions=1536,
            vector_search_profile_name="myProfile"
        )
    ],
    vector_search=VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="myHnsw")],
        profiles=[VectorSearchProfile(name="myProfile", algorithm_configuration_name="myHnsw")]
    ),
    semantic_search=SemanticSearch(configurations=[
        SemanticConfiguration(
            name="my-semantic-config",
            prioritized_fields=SemanticPrioritizedFields(
                title_field=SemanticField(field_name="title"),
                content_fields=[SemanticField(field_name="content")]
            )
        )
    ])
)

client.create_or_update_index(index)
print(f"Index created: {index.name}")
```

---

## Ingest Documents

**File:** `infrastructure/scripts/ingest_documents.py`

```python
import os, uuid
from pathlib import Path
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI

openai_client = OpenAI()
search_client = SearchClient(
    os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
    os.getenv("AZURE_AI_SEARCH_INDEX", "enterprise-knowledge"),
    AzureKeyCredential(os.getenv("AZURE_AI_SEARCH_KEY"))
)

documents = []
for doc_file in Path("data/sample-documents").glob("*.md"):
    content = doc_file.read_text(encoding="utf-8")
    embedding = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=content[:8000]
    ).data[0].embedding

    documents.append({
        "id": str(uuid.uuid4()),
        "title": doc_file.stem.replace("-", " ").title(),
        "content": content,
        "category": "Policy",
        "source": doc_file.name,
        "riskCategory": "Medium",
        "contentVector": embedding
    })

results = search_client.upload_documents(documents)
print(f"Ingested {len(documents)} documents.")
```

```bash
uv run python infrastructure/scripts/create_search_index.py
uv run python infrastructure/scripts/ingest_documents.py
```

---

## Azure Search Service

**File:** `mcp-server/src/enterprise_agentops_mcp/services/azure_search_service.py`

```python
import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

def search_knowledge(query: str, max_results: int = 3) -> list[dict]:
    client = SearchClient(
        os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
        os.getenv("AZURE_AI_SEARCH_INDEX", "enterprise-knowledge"),
        AzureKeyCredential(os.getenv("AZURE_AI_SEARCH_KEY"))
    )

    results = client.search(
        search_text=query,
        query_type="semantic",
        semantic_configuration_name="my-semantic-config",
        top=max_results,
        select=["id", "title", "content", "category", "source", "riskCategory"]
    )

    return [
        {
            "articleId": r["id"],
            "title": r["title"],
            "category": r["category"],
            "summary": r["content"][:400],
            "confidence": round(r.get("@search.reranker_score", 3.0) / 4, 2),
            "source": r["source"]
        }
        for r in results
    ]
```

---

## Switching Between Mock and Azure AI Search

```env
MCP_DATA_MODE=mock    # keyword search against local JSON
MCP_DATA_MODE=search  # Azure AI Search semantic + vector
```

Or use a separate variable to decouple knowledge mode from data mode:

```env
MCP_KNOWLEDGE_MODE=search  # mock | search
```

---

## Next Step

[docs/09-agent-framework.md](09-agent-framework.md) — Day 9: Semantic Kernel agents + Copilot Studio.
