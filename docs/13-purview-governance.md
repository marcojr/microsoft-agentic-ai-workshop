# Stage 13: Microsoft Purview Governance

Add Microsoft Purview to the project as the governance, compliance and data protection layer.

---

## Goal

Use Microsoft Purview after the core agent workflow is stable to show how enterprise AI systems can be governed, audited and protected.

This stage is not required for the MVP approval flow. It is a post-core-workflow governance phase.

---

## Why Purview Matters Here

The project already has:

- Copilot Studio agent surface
- Azure Function orchestration
- Dataverse business data
- Azure AI Search policy documents
- Service Bus events
- Application Insights telemetry
- Power Apps approval console

Purview adds the enterprise governance layer around those assets.

---

## Candidate Purview Scope

### Data Discovery and Catalog

- catalog Dataverse tables used by the project
- catalog Azure Storage assets
- catalog policy documents used for RAG/search
- document ownership and business glossary terms

### Classification

- identify customer emails, names and support records as sensitive data
- classify policy and approval records
- classify AI-related operational telemetry where relevant

### Data Protection

- evaluate sensitivity labels for exported reports and documents
- review DLP rules for Power Platform connectors and approval data
- define which data can be used by agents and which data should be restricted

### Audit and Compliance

- use Purview Audit for user/admin activity where Microsoft 365 and Power Platform logs apply
- document approval decision traceability
- map the demo to GDPR/LGPD-style concerns:
  - purpose limitation
  - access control
  - auditability
  - retention
  - sensitive data handling

### AI Governance Narrative

- explain which data the agent can see
- explain which tool calls are audited
- explain how human approval gates reduce operational risk
- explain how sensitive data should be classified before scaling the pattern

---

## Suggested Implementation Order

1. Identify sensitive data fields in Dataverse:
   - customer name
   - customer email
   - order details
   - approval comments

2. Document data classifications in the schema docs.

3. Review Power Platform connector DLP policy impact.

4. Review audit evidence:
   - Copilot Studio test activity
   - Dataverse approval records
   - Azure Function logs
   - App Insights traces

5. Add Purview screenshots and notes to the final demo deck.

---

## Current Status

Planned.

Do not implement Purview before the Power Apps approval console and observability dashboard are stable.

