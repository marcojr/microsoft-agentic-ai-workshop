# Stage 8: Secure RAG (Day 8)

Create policy documents, index them in Azure AI Search, and wire `search_knowledge_articles` to return live results with citations and confidence scores.

---

## Day 8 Deliverables

- [x] Policy documents created in `data/sample-documents/`
- [x] Azure AI Search service provisioned
- [x] Azure AI Search index created
- [x] Documents ingested
- [x] `search_knowledge_articles` wired to Azure AI Search mode
- [x] Citations, confidence scores and source metadata included
- [x] Mock fallback retained

## Current Implementation Status

Already implemented in code:

- sample policy documents under `data/sample-documents/`
- Azure AI Search client service in `mcp-server/src/enterprise_agentops_mcp/services/azure_search_service.py`
- `search_knowledge_articles` now supports `MCP_KNOWLEDGE_MODE=search`
- index creation script in `infrastructure/scripts/create_search_index.py`
- document ingestion script in `infrastructure/scripts/ingest_documents.py`
- Pulumi C# resource definition for Azure AI Search in `infrastructure/pulumi/Program.cs`

Live verification completed:

- Azure AI Search service: `srch-agentops-dev-002`
- index: `enterprise-knowledge`
- documents ingested: 10
- `search_knowledge_articles` returns live Azure AI Search results
- the local orchestrator now completes with HTTP-style status `200`

Important honesty note:

- this implementation currently uses classic Azure AI Search full-text retrieval
- vector embeddings are not wired yet
- that is intentional for this stage so the orchestrator can complete end-to-end without introducing an extra embedding dependency first

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
3. Submit for approval through the Power Apps Approval Console
4. Only communicate compensation after approval is confirmed
```

---

## Create Azure AI Search (via Pulumi)

Add to the Pulumi C# project under `infrastructure/pulumi/`:

```csharp
Pulumi is already updated in this repo to create the Azure AI Search service:

- `infrastructure/pulumi/Program.cs`

Run:

```powershell
cd infrastructure/pulumi
$env:PULUMI_CONFIG_PASSPHRASE="<your-passphrase>"
& 'C:\Program Files (x86)\Pulumi\pulumi.exe' up
```
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
    SearchIndex, SimpleField, SearchableField, SearchFieldDataType
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
        SimpleField(name="source", type=SearchFieldDataType.String),
        SimpleField(name="riskCategory", type=SearchFieldDataType.String, filterable=True),
    ],
)

client.create_or_update_index(index)
print(f"Index created: {index.name}")
```

---

## Ingest Documents

**File:** `infrastructure/scripts/ingest_documents.py`

```python
import os
from pathlib import Path
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

search_client = SearchClient(
    os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
    os.getenv("AZURE_AI_SEARCH_INDEX", "enterprise-knowledge"),
    AzureKeyCredential(os.getenv("AZURE_AI_SEARCH_KEY"))
)

documents = []
for doc_file in Path("data/sample-documents").glob("*.md"):
    content = doc_file.read_text(encoding="utf-8")

    documents.append({
        "id": doc_file.stem,
        "title": doc_file.stem.replace("-", " ").title(),
        "content": content,
        "category": "Policy",
        "source": doc_file.name,
        "riskCategory": "Medium",
    })

results = search_client.merge_or_upload_documents(documents)
print(f"Ingested {len(documents)} documents.")
```

```bash
uv run --project mcp-server python infrastructure/scripts/create_search_index.py
uv run --project mcp-server python infrastructure/scripts/ingest_documents.py
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

    results = client.search(search_text=query, top=max_results)

    return [
        {
            "articleId": r["id"],
            "title": r["title"],
            "category": r["category"],
            "summary": r["content"][:400],
            "confidence": round(min(0.99, 0.45 + r.get("@search.score", 0.0) / 4), 2),
            "source": r["source"]
        }
        for r in results
    ]
```

---

## Switching Between Mock and Azure AI Search

```env
MCP_DATA_MODE=mock    # keyword search against local JSON
MCP_DATA_MODE=search  # Azure AI Search
```

Or use a separate variable to decouple knowledge mode from data mode:

```env
MCP_KNOWLEDGE_MODE=search  # mock | search
```

---

## Next Step

[docs/09-agent-framework.md](09-agent-framework.md) — Day 9: Microsoft Agent Framework + Copilot Studio, with one Semantic Kernel comparison agent.
