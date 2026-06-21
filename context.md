# Enterprise AgentOps Control Tower

## Project Overview

Enterprise AgentOps Control Tower is a portfolio/reference architecture project designed to demonstrate a serious Microsoft Agentic AI architecture.

The project shows how enterprise AI agents can be built, orchestrated, governed, monitored and connected to real business systems using the Microsoft ecosystem.

The system is not a generic chatbot. It is an enterprise-grade agentic workflow platform demonstrating:

* Copilot Studio as the business-facing agent interface
* Microsoft Foundry (formerly Azure AI Foundry) for managed AI agent capabilities
* Microsoft Agent Framework (successor to Semantic Kernel + AutoGen) for code-first orchestration
* one Semantic Kernel Draft Agent kept intentionally for comparison, didactics and legacy understanding
* Microsoft 365 Agents SDK as the final-phase custom-engine agent surface
* A custom MCP Server as the governed enterprise tool layer
* Dataverse as the business data layer
* Azure AI Search as the Secure RAG layer
* Power Apps as the browser-based human approval console
* Logic Apps, Service Bus and optional Power Automate for integration workflow
* Azure Functions as the backend orchestrator
* Pulumi for Azure infrastructure as code
* Application Insights, Azure Monitor and Power BI for observability and AI cost engineering

The main objective is to prove the ability to design and build secure, auditable, cost-controlled AI agents connected to real business workflows.

---

## Positioning

The project supports the positioning:

**Microsoft Agentic AI Architect**

Positioning statement:

> I design and govern enterprise AI agents inside the Microsoft ecosystem, not just chatbots, but secure, auditable, cost-controlled agentic workflows connected to real business systems.

---

## Core Scenario

## Webshop Order Support Agent

The primary scenario is a webshop-style customer support workflow built on Dataverse.

A business user interacts with a Copilot Studio agent and asks questions about customer orders, deliveries, returns, refunds and compensation approvals.

The agent must retrieve structured customer/order data, search policy documents, evaluate business risk, create approval requests when required, and log all execution metadata for observability and cost tracking.

The workflow is thread-aware. Each conversation or case can carry a `threadId` so later turns can rehydrate customer context, pending approval state, last run metadata and the current workflow step.

Human-in-the-loop is a first-class design requirement. High-risk actions such as compensation, exception refunds and escalation must create explicit approval state and must not be communicated externally as resolved while approval is pending.

### Example User Prompt

```text
Find the latest order for john.smith@contoso.com, check delivery and refund issues, validate the delivery postcode, summarise the situation and create an approval request if compensation is required.
```

### Expected Behaviour

The system must:

1. Identify the customer by email.
2. Retrieve the latest order.
3. Retrieve order items.
4. Retrieve shipment status.
5. Validate the delivery postcode or address using the public Maps/Geocoding MCP Server.
6. Retrieve route or distance context when relevant.
7. Check returns linked to the order.
8. Check refunds linked to the order.
9. Search compensation/refund policy documents.
10. Determine whether approval is required.
11. Generate a customer-safe summary.
12. Evaluate the response before returning it.
13. Create an approval request if required.
14. Calculate estimated AI cost.
15. Log the agent run with tokens, latency, tools called, model used and risk scores.
16. Persist thread state with the current workflow step and approval state.
17. Return a concise response to the user.

---

## Secondary Scenario

## Customer Support Case Intelligence Agent

The secondary scenario demonstrates agentic workflows over Dataverse/Dynamics-style customer service data.

The project does not implement Dynamics 365. It uses Dataverse tables that represent common customer service objects such as accounts, contacts, support cases, activities, knowledge articles and approvals.

### Example User Prompt

```text
Find open support cases for Contoso, summarise the situation, check SLA risk, suggest the next action and create an escalation approval if required.
```

### Expected Behaviour

The system must:

1. Resolve the customer account.
2. Retrieve open support cases.
3. Retrieve related case details and activities.
4. Search relevant knowledge articles.
5. Detect SLA risk.
6. Suggest next action.
7. Create an escalation approval when required.
8. Log the full agent run.
9. Return a grounded and auditable summary.

---

## Architecture

## High-Level Architecture

MVP path:

```text
User
  ↓
Copilot Studio Test Chat
  ↓
Copilot Studio Action / REST Action
  ↓
Azure Function Orchestrator API
  ↓
Microsoft Agent Framework (successor to Semantic Kernel + AutoGen)
  ↓
MCP Client
  ↓
Enterprise AgentOps MCP Server
  ↓
Controlled MCP Tools
  ↓
Dataverse / Azure AI Search / Power Apps / Application Insights
  ↓
Response + AgentOps Metrics
```

Future custom-engine agent surface:

```text
Microsoft 365 Agents SDK / Agents Playground / optional Teams deployment
  ↓
Azure Function Orchestrator API
  ↓
same orchestration and MCP tool layer
```

---

## Main Components

## 1. Copilot Studio Agent

Copilot Studio is the main business-facing interface for MVP.

The agent will be tested using Copilot Studio Test Chat.

The agent must:

* receive natural language requests
* ask for missing parameters when needed
* call backend actions
* call backend actions when appropriate
* return structured responses
* avoid exposing raw system complexity to the user

Example actions:

```text
summarise_customer_order
summarise_customer_cases
search_enterprise_knowledge
create_approval_request
get_agent_run_status
```

---

## 2. Azure Function Orchestrator API

The Orchestrator API is the backend entry point between Copilot Studio and the pro-code agentic architecture.

It must:

* validate requests
* authenticate callers
* route requests to the correct workflow
* call Microsoft Agent Framework (successor to Semantic Kernel + AutoGen) orchestration
* call MCP tools through the MCP client
* trigger Service Bus, Logic Apps or optional Power Automate integration when required
* log execution metadata
* return structured JSON responses

Example endpoints:

```text
POST /api/agents/webshop/order-support
POST /api/agents/customer-case/summarise
POST /api/agents/knowledge/search
GET  /api/approvals/pending
POST /api/approvals/decision
GET  /api/agent-runs/{runId}
```

---

## 3. Microsoft Agent Framework (successor to Semantic Kernel + AutoGen)

Microsoft Agent Framework (successor to Semantic Kernel + AutoGen) is the pro-code orchestration layer.

It is responsible for coordinating specialised agents and deciding which tools must be called.

Semantic Kernel is not the strategic direction for the whole project. It remains in exactly one place: the Draft Agent. That agent is kept as a practical comparison track so the project can explain the evolution from Semantic Kernel to Microsoft Agent Framework.

All agent and orchestration code should include short step-by-step comments in English. The goal is educational clarity: explain the major execution steps and why they exist, without adding comments that simply repeat obvious syntax.

### Coding Agent Implementation Rules

Coding agents working in this repository must prefer the correct production-shaped path over the fastest local shortcut.

Rules:

* Use the project source of truth instead of duplicating local lists. Examples: MCP tool names come from the MCP client/tool registry; Azure resource names come from Azure context/Pulumi config; model names come from environment/config.
* Do not make prompts invent infrastructure. If an agent returns `toolsRequired`, the allowed tool names must be derived from the registered MCP tools and injected into the prompt or validated after the model response.
* Keep agents behind typed contracts where practical. For Python agent outputs, prefer Pydantic response models and explicit validation.
* Treat human approval as state, not only as a side effect. Approval ID, status and pending workflow step must be available to downstream callers.
* Use a browser-based Power Apps Approval Console as the primary human approval UX. Dataverse stores approval records; Orchestrator decision endpoints update approval status and thread state.
* Preserve thread state for workflows that can span multiple user turns or approval events. Prefer explicit `threadId` handling over hidden conversational memory.
* Store runtime thread state in Azure Table Storage for production-shaped execution. Use Dataverse for business/audit records; use Blob Storage only for larger snapshots if needed.
* Build an extensive typed domain model incrementally. Customer, order, shipment, return, refund, knowledge, governance, approval, telemetry and thread-state payloads should move toward Pydantic contracts as they become internal agent boundaries.
* Keep MCP as the governed business-tool boundary. Agents should not directly manipulate Dataverse, approvals, cost, or observability data when an MCP tool exists.
* Avoid silent fallbacks that hide broken integrations. If Azure OpenAI, MCP, Dataverse, Search, Service Bus, or a contract validation path fails, surface the failure clearly.
* Add tests around contracts, tool registry behavior, and orchestration boundaries whenever changing agent behavior.
* Update `progress.md` after meaningful implementation, verification, decision, or blocker events.

Specialised agents:

```text
Intake Agent
Data Agent
Knowledge Agent
Governance Agent
Draft Agent (Semantic Kernel comparison track)
Critic / Evaluator Agent
Cost Agent
Workflow Agent
```

Shared orchestration model:

```text
ThreadState
GovernanceDecision
ApprovalOutcome
AgentRunTelemetry
OrderSupportContext
```

The first implementation uses `ThreadState`, `GovernanceDecision` and `ApprovalOutcome` as typed Pydantic contracts. The remaining domain contracts should be added as the corresponding agent boundaries harden.

Thread-state persistence:

```text
Local development: file store under apps/orchestrator-api/.state/
Production-shaped runtime: Azure Table Storage
Dataverse: business/audit records, not conversational thread state blobs
```

### Intake Agent

Classifies the request and extracts:

* intent
* business domain
* required tools
* urgency
* risk level
* approval likelihood

### Data Agent

Retrieves structured business data using MCP tools.

Responsible for:

* customers
* accounts
* contacts
* orders
* order items
* shipments
* returns
* refunds
* support cases
* activities

### Knowledge Agent

Retrieves grounded knowledge using Secure RAG.

Responsible for:

* policy search
* knowledge article retrieval
* source citations
* confidence scoring
* missing-context detection

### Governance Agent

Checks whether the request or response requires approval.

Responsible for:

* policy risk
* sensitive data detection
* human-in-the-loop decisions
* blocked actions
* approval requirements

### Draft Agent

Generates business-safe outputs.

Responsible for:

* customer-safe summaries
* internal support summaries
* escalation notes
* refund/compensation explanations

### Critic / Evaluator Agent

Reviews generated outputs before returning them.

Responsible for:

* clarity
* groundedness
* tone
* policy alignment
* missing evidence
* approval readiness

### Cost Agent

Tracks AI usage and cost.

Responsible for:

* input tokens
* output tokens
* model used
* vendor used
* estimated cost
* cost per operation
* cost per workflow

### Workflow Agent

Triggers enterprise actions.

Responsible for:

* approval creation
* task creation
* Dataverse write-back
* Power Automate triggers
* Logic Apps triggers

---

## 4. Enterprise AgentOps MCP Server

The MCP Server is the governed enterprise tool layer.

Agents must not directly manipulate business systems. They must call typed and controlled tools.

The MCP Server exposes tools for:

* customer lookup
* account lookup
* order lookup
* order item retrieval
* shipment status
* returns and refunds
* support case retrieval
* knowledge search
* approval creation
* task creation
* response evaluation
* cost calculation
* agent run logging

### MCP Server Name

```text
enterprise-agentops-mcp-server
```

### MCP Server Responsibilities

The MCP Server must:

* expose business tools through MCP
* provide typed inputs and outputs
* validate tool input
* return safe and shaped responses
* log tool calls
* support auditability
* support future Dataverse integration
* support future Azure AI Search integration
* support the Power Apps Approval Console and optional Power Automate integration

### Initial Implementation

Initial version must run locally with mock JSON data.

Future versions will replace mock data with:

* Dataverse Web API
* Azure AI Search
* Power Apps Approval Console custom connector
* optional Power Automate HTTP-triggered flows
* Application Insights
* Azure Table Storage for runtime thread state
* Azure SQL or Cosmos DB only if a future requirement clearly exceeds the current Dataverse/Table Storage model

---

## 5. Public MCP Server

The project should also consume one external/public MCP Server that is directly related to the webshop delivery scenario.

### Selected Public MCP Server

OpenStreetMap / Geocoding MCP Server

Alternative: Mapbox MCP Server

### Purpose

The public MCP Server provides external geospatial and delivery-context capabilities.

It is used to:

- validate delivery postcodes or addresses
- geocode customer delivery locations
- calculate distance or route context
- enrich shipment delay analysis
- support delivery risk assessment
- provide additional context for refund, compensation or escalation decisions

### Business Use Case

When an order has a delayed shipment, the agent can use the public Maps/Geocoding MCP Server to validate the delivery location and enrich the delivery issue with external location context.

Example user request:

Find the latest order for john.smith@contoso.com, check delivery and refund issues, validate the delivery postcode, summarise the situation and create an approval request if compensation is required.

Example tool chain:

- get_customer_by_email
- get_latest_order
- get_order_items
- get_shipment_status
- geocode_delivery_postcode
- calculate_delivery_distance_or_route
- search_knowledge_articles
- evaluate_response
- create_approval_request
- calculate_agent_run_cost
- log_agent_run

### Boundary

The custom Enterprise AgentOps MCP Server handles internal business data and controlled enterprise workflows.

The public Maps/Geocoding MCP Server handles external delivery-location context.

enterprise-agentops-mcp-server:
- customer, order, shipment, refund, approval, cost and observability tools

maps/geocoding-mcp-server:
- postcode validation, geocoding, route distance and delivery context

---

## 6. Microsoft Foundry (formerly Azure AI Foundry)

Microsoft Foundry (formerly Azure AI Foundry) is used to demonstrate managed AI agent capability.

A dedicated managed agent should be created for policy and governance.

### Policy and Governance Agent

Responsibilities:

* answer questions over AI policy, refund policy and approval rules
* decide whether an action needs approval
* return explanation and source references
* participate in the larger agent-to-agent workflow

---

## 7. Microsoft 365 Agents SDK

Microsoft 365 Agents SDK is included as the final-phase custom-engine agent surface.

It is not required for the MVP.

The MVP uses Copilot Studio Test Chat as the business-facing interface. Microsoft 365 Agents SDK will be tested later through Microsoft 365 Agents Playground. If a suitable Microsoft 365 developer tenant is available, the same agent can optionally be tested inside Microsoft Teams.

### Purpose

The Microsoft 365 Agents SDK demonstrates that the architecture is not limited to Copilot Studio.

It allows the same backend capabilities to be reused by a custom-engine Microsoft 365 or Teams agent.

### Future Responsibilities

* run in Microsoft 365 Agents Playground during development
* optionally run in Microsoft Teams when a suitable developer tenant is available
* call the same Azure Function Orchestrator API
* use the same Microsoft Agent Framework (successor to Semantic Kernel + AutoGen) orchestration
* consume the same Enterprise AgentOps MCP Server tools
* support the same Dataverse, Secure RAG, approval, observability and cost-tracking workflows

### Future Architecture

```text
Microsoft 365 Agents SDK Agent
  ↓
Azure Function Orchestrator API
  ↓
Microsoft Agent Framework (successor to Semantic Kernel + AutoGen)
  ↓
MCP Client
  ↓
Enterprise AgentOps MCP Server
  ↓
Dataverse / Azure AI Search / Power Apps Approval Console / Observability
```

---

## 8. Azure AI Search / Secure RAG

Azure AI Search is the Secure RAG layer.

It stores and retrieves enterprise policy and knowledge documents.

Knowledge sources:

```text
AI Usage Policy
Responsible AI Policy
Customer Compensation Policy
Refund Policy
Delivery Policy
SLA Policy
Data Privacy Policy
Security Policy
Approval Rules
Customer Service Playbook
Sales Process Guide
Knowledge Articles
```

Secure RAG must support:

* hybrid search
* semantic search
* vector search
* metadata filters
* source citations
* confidence scoring
* document type classification
* retrieval logging
* query logging

MCP tool:

```text
search_knowledge_articles
```

Example output:

```json
{
  "query": "What approval is required before offering compensation for delayed delivery?",
  "topSources": [
    {
      "document": "Customer Compensation Policy",
      "section": "Approval Requirements",
      "confidence": 0.87
    }
  ],
  "answer": "Customer compensation for repeated delivery failure requires service manager approval before being communicated externally.",
  "requiresApproval": true
}
```

---

## 9. Dataverse Business Data Layer

Dataverse is the business data layer.

The project uses default-style customer records and custom webshop/support tables.

The schema must support the primary Webshop Order Support scenario and the secondary Customer Support Case Intelligence scenario.

---

## Dataverse Tables

## Account

Fields:

```text
accountId
name
accountNumber
industry
region
relationshipManager
riskLevel
```

## Contact

Fields:

```text
contactId
accountId
fullName
email
role
phone
preferredLanguage
deliveryAddress
deliveryPostcode
```

## Product

Fields:

```text
productId
sku
name
category
price
stockLevel
supplier
active
```

## Order

Fields:

```text
orderId
orderNumber
accountId
contactId
orderDate
status
totalAmount
paymentStatus
deliveryStatus
shipmentId
riskLevel
deliveryAddress
deliveryPostcode
```

## Order Item

Fields:

```text
orderItemId
orderId
productId
sku
productName
quantity
unitPrice
totalPrice
```

## Shipment

Fields:

```text
shipmentId
orderId
carrier
trackingNumber
status
estimatedDeliveryDate
deliveredDate
delayReason
originPostcode
destinationPostcode
routeDistanceKm
```

## Return Request

Fields:

```text
returnId
orderId
orderItemId
reason
status
requestedDate
approvedDate
refundRequired
```

## Refund

Fields:

```text
refundId
orderId
returnId
amount
status
reason
requiresApproval
approvedBy
```

## Support Case

Fields:

```text
caseId
accountId
contactId
orderId
title
description
status
priority
createdOn
slaDeadline
slaRisk
owner
category
```

## Activity

Fields:

```text
activityId
regardingId
regardingType
type
subject
description
createdOn
owner
```

## Knowledge Article

Fields:

```text
articleId
title
category
content
effectiveDate
riskCategory
```

## Approval Request

Fields:

```text
approvalId
relatedRecordId
relatedRecordType
requestedBy
approvalType
status
riskLevel
reason
createdOn
approvedBy
```

## Agent Run

Fields:

```text
runId
userId
workflowName
intent
startedAt
completedAt
status
modelUsed
vendorUsed
inputTokens
outputTokens
estimatedCost
latencyMs
riskScore
qualityScore
groundednessScore
requiresApproval
toolsCalled
```

---

## MCP Tools

The MCP Server must expose the following tools.

## get_customer_by_email

Finds a customer/contact by email.

Input:

```json
{
  "email": "john.smith@contoso.com"
}
```

Output:

```json
{
  "contactId": "con-001",
  "accountId": "acc-001",
  "fullName": "John Smith",
  "email": "john.smith@contoso.com",
  "accountName": "Contoso Ltd",
  "preferredLanguage": "English",
  "riskLevel": "Medium"
}
```

---

## get_account_by_name

Finds an account by name.

Input:

```json
{
  "accountName": "Contoso"
}
```

Output:

```json
{
  "accountId": "acc-001",
  "name": "Contoso Ltd",
  "accountNumber": "C-1001",
  "industry": "Retail",
  "region": "UK",
  "relationshipManager": "Sarah Mitchell",
  "riskLevel": "Medium"
}
```

---

## get_latest_order

Retrieves the latest order for a contact.

Input:

```json
{
  "contactId": "con-001"
}
```

Output:

```json
{
  "orderId": "ord-1001",
  "orderNumber": "WEB-1001",
  "orderDate": "2026-06-10T10:00:00Z",
  "status": "Shipped",
  "totalAmount": 349.98,
  "paymentStatus": "Paid",
  "deliveryStatus": "Delayed",
  "shipmentId": "ship-9001",
  "riskLevel": "High"
}
```

---

## get_order_details

Retrieves order header and key metadata.

Input:

```json
{
  "orderId": "ord-1001"
}
```

Output:

```json
{
  "orderId": "ord-1001",
  "orderNumber": "WEB-1001",
  "status": "Shipped",
  "totalAmount": 349.98,
  "paymentStatus": "Paid",
  "deliveryStatus": "Delayed",
  "riskLevel": "High"
}
```

---

## get_order_items

Retrieves order items.

Input:

```json
{
  "orderId": "ord-1001"
}
```

Output:

```json
{
  "orderId": "ord-1001",
  "items": [
    {
      "orderItemId": "oi-001",
      "sku": "SKU-100",
      "productName": "Premium Coffee Machine",
      "quantity": 1,
      "unitPrice": 299.99,
      "totalPrice": 299.99
    }
  ]
}
```

---

## get_shipment_status

Retrieves shipment status.

Input:

```json
{
  "shipmentId": "ship-9001"
}
```

Output:

```json
{
  "shipmentId": "ship-9001",
  "carrier": "DemoCarrier",
  "trackingNumber": "TRK-123456",
  "status": "Delayed",
  "estimatedDeliveryDate": "2026-06-18",
  "delayReason": "Carrier network disruption"
}
```

---

## get_returns_for_order

Retrieves return requests related to an order.

Input:

```json
{
  "orderId": "ord-1001"
}
```

Output:

```json
{
  "orderId": "ord-1001",
  "returns": [
    {
      "returnId": "ret-3001",
      "reason": "Delivery delay",
      "status": "Requested",
      "refundRequired": true
    }
  ]
}
```

---

## get_refunds_for_order

Retrieves refund records for an order.

Input:

```json
{
  "orderId": "ord-1001"
}
```

Output:

```json
{
  "orderId": "ord-1001",
  "refunds": [
    {
      "refundId": "ref-4001",
      "amount": 49.99,
      "status": "Pending Approval",
      "reason": "Delivery delay compensation",
      "requiresApproval": true
    }
  ]
}
```

---

## get_open_cases

Retrieves open support cases for an account.

Input:

```json
{
  "accountId": "acc-001"
}
```

Output:

```json
{
  "accountId": "acc-001",
  "openCases": [
    {
      "caseId": "case-1001",
      "title": "Delayed shipment complaint",
      "status": "Open",
      "priority": "High",
      "slaRisk": "High",
      "createdOn": "2026-06-11",
      "owner": "Support Team A"
    }
  ]
}
```

---

## get_case_details

Retrieves support case details.

Input:

```json
{
  "caseId": "case-1001"
}
```

Output:

```json
{
  "caseId": "case-1001",
  "title": "Delayed shipment complaint",
  "description": "Customer reported repeated delivery delays affecting store operations.",
  "status": "Open",
  "priority": "High",
  "slaRisk": "High",
  "slaDeadline": "2026-06-18T17:00:00Z"
}
```

---

## search_knowledge_articles

Searches internal policy and knowledge articles.

Input:

```json
{
  "query": "delayed shipment compensation policy",
  "maxResults": 3
}
```

Output:

```json
{
  "query": "delayed shipment compensation policy",
  "results": [
    {
      "articleId": "ka-001",
      "title": "Customer Compensation Policy",
      "category": "Customer Service",
      "summary": "Customer compensation requires approval when refund or credit exceeds the standard threshold.",
      "confidence": 0.86,
      "source": "Customer Service Playbook"
    }
  ]
}
```

---

## create_approval_request

Creates a human approval request.

Input:

```json
{
  "relatedRecordId": "ord-1001",
  "relatedRecordType": "order",
  "approvalType": "Compensation",
  "reason": "Delayed shipment and requested refund compensation",
  "riskLevel": "High",
  "requestedBy": "agent"
}
```

Output:

```json
{
  "approvalId": "apr-9001",
  "status": "Pending",
  "relatedRecordId": "ord-1001",
  "riskLevel": "High",
  "createdOn": "2026-06-17T12:00:00Z"
}
```

---

## create_follow_up_task

Creates a follow-up task.

Input:

```json
{
  "relatedRecordId": "ord-1001",
  "relatedRecordType": "order",
  "subject": "Follow up with John Smith about delayed delivery",
  "dueDate": "2026-06-19",
  "owner": "Support Team A"
}
```

Output:

```json
{
  "taskId": "task-7001",
  "status": "Created",
  "subject": "Follow up with John Smith about delayed delivery",
  "dueDate": "2026-06-19"
}
```

---

## calculate_agent_run_cost

Calculates estimated LLM cost.

Input:

```json
{
  "vendor": "OpenAI",
  "model": "gpt-5-mini",
  "inputTokens": 1800,
  "outputTokens": 450
}
```

Output:

```json
{
  "vendor": "OpenAI",
  "model": "gpt-5-mini",
  "inputTokens": 1800,
  "outputTokens": 450,
  "estimatedCost": 0.012,
  "currency": "USD"
}
```

---

## log_agent_run

Logs agent execution telemetry.

Input:

```json
{
  "workflowName": "WebshopOrderSupport",
  "intent": "SummariseLatestOrderIssue",
  "modelUsed": "gpt-5-mini",
  "vendor": "OpenAI",
  "inputTokens": 1800,
  "outputTokens": 450,
  "latencyMs": 3200,
  "toolsCalled": [
    "get_customer_by_email",
    "get_latest_order",
    "get_order_items",
    "get_shipment_status",
    "search_knowledge_articles",
    "create_approval_request"
  ],
  "requiresApproval": true,
  "riskScore": 0.82,
  "qualityScore": 0.88
}
```

Output:

```json
{
  "logged": true,
  "runId": "run-0001",
  "estimatedCost": 0.012
}
```

---

## evaluate_response

Evaluates generated output before returning it.

Input:

```json
{
  "response": "John Smith's latest order is delayed and compensation may be required...",
  "requiredSources": [
    "ord-1001",
    "ship-9001",
    "ka-001"
  ],
  "riskLevel": "High"
}
```

Output:

```json
{
  "qualityScore": 0.88,
  "groundednessScore": 0.91,
  "riskScore": 0.76,
  "issues": [
    "Response should mention that compensation requires approval before being communicated externally."
  ],
  "approvedForUser": false
}
```

---

## Power Apps Approval Console

Power Apps is the primary browser-based human-in-the-loop surface.

The approval console must:

```text
List pending approval requests from Dataverse or Orchestrator API
Show customer, order, risk, reason, approval type and thread ID
Call POST /api/approvals/decision with Approved or Rejected
Leave thread-state mutation to the Orchestrator API
```

Power Automate remains optional for notifications, reminders or external workflow routing, but it is not the primary approval UI direction.

---

## Logic Apps

Logic Apps are used for enterprise integration and more technical orchestration.

Potential uses:

```text
External shipment status simulation
Async workflow processing
API orchestration
Event-based workflow
```

---

## Service Bus

Service Bus is used for asynchronous event-driven architecture.

Example event:

```json
{
  "eventType": "AgentRunCompleted",
  "runId": "RUN-001",
  "workflowName": "WebshopOrderSupport",
  "requiresApproval": true,
  "estimatedCost": 0.018
}
```

---

## Observability

The system must capture observability data for every agent run.

Metrics:

```text
runId
userId
workflowName
intent
modelUsed
vendorUsed
inputTokens
outputTokens
totalTokens
estimatedCost
latencyMs
cacheHit
toolsCalled
ragSourcesUsed
approvalRequired
approvalStatus
groundednessScore
qualityScore
riskScore
errorStatus
fallbackUsed
timestamp
```

Logging targets:

```text
Application Insights
Azure Monitor
Dataverse Agent Run table
Power BI dashboard
MCP tool execution logs
```

---

## AI Cost Engineering

The system must estimate and log LLM cost per agent run.

Pricing table fields:

```text
vendor
model
inputTokenPricePer1M
outputTokenPricePer1M
currency
effectiveDate
```

Cost formula:

```text
inputCost = inputTokens / 1_000_000 * inputTokenPricePer1M
outputCost = outputTokens / 1_000_000 * outputTokenPricePer1M
totalCost = inputCost + outputCost
```

Dashboard views:

```text
total cost per day
cost per workflow
cost per model
cost per tool chain
average cost per successful operation
high-latency runs
failed runs
approval-heavy workflows
```

---

## Governance and Responsible AI

The project must demonstrate:

```text
human approval for risky actions
blocked actions for prohibited use cases
audit trail for agent actions
risk classification
source citation for knowledge responses
access control awareness
model usage transparency
cost visibility
controlled MCP tool boundaries
logging and traceability
```

Responsible AI concepts:

```text
Microsoft Responsible AI principles
NIST AI RMF concepts
EU AI Act awareness
GDPR / UK GDPR awareness
human-in-the-loop control
auditability
transparency
privacy and security
reliability and safety
```

---

## Security

Authentication options:

```text
Entra ID
Managed Identity
Service Principal
OAuth
Power Platform connection references
```

Project standard:

```text
Service Principal for Dataverse and backend runtime access
Interactive user auth only for maker/admin setup tasks
Managed Identity may be added later for Azure-hosted components, but it is not the primary Dataverse auth model
```

Security requirements:

```text
avoid hardcoded secrets
use Key Vault
avoid raw system access from agents
use typed tools/actions
log sensitive operations
respect Dataverse security concepts
support approval before write-back
mask sensitive fields in logs
prevent agents from bypassing MCP tool boundaries
```

---

## Infrastructure

Pulumi is used for Azure infrastructure.

Azure naming for this project follows Microsoft Cloud Adoption Framework guidance plus Azure resource-specific naming rules. The working source set is:

- https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming
- https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations
- https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-name-rules

The Azure study environment is ephemeral by design. The workload resource group can be deleted as a whole, but recovery dumps and reseed artifacts must live in persistent blob storage outside that disposable resource group. Resource names therefore include a sequence number and that sequence advances after decommissioning.

Initial Pulumi scope:

```text
Resource Group
Storage Account
Azure Function App
Application Insights
Key Vault
Azure AI Search optional
Service Bus optional
API Management optional
```

Pulumi folder:

```text
infrastructure/
  pulumi/
    Pulumi.yaml
    Pulumi.dev.yaml
    EnterpriseAgentOps.Infrastructure.csproj
    Program.cs
    AzureContext.cs
    AzureContextLoader.cs
    resources/
```

---

## Repository Structure

```text
enterprise-agentops-control-tower/
  README.md

  docs/
    architecture.md
    demo-script.md
    interview-talking-points.md
    secure-rag.md
    governance-model.md
    ai-cost-engineering.md
    observability.md
    dataverse-integration.md
    responsible-ai.md
    mcp-server.md
    mcp-tools.md
    public-mcp-servers.md
    pulumi-infrastructure.md

  apps/
    orchestrator-api/
      src/
      tests/
      README.md

    frontend-demo/
      src/
      README.md

    m365-agent/
      src/
      tests/
      README.md

  mcp-server/
    README.md
    pyproject.toml
    .env.example
    src/
      enterprise_agentops_mcp/
        __init__.py
        server.py
        config.py

        tools/
          __init__.py
          customers.py
          accounts.py
          contacts.py
          orders.py
          order_items.py
          shipments.py
          returns.py
          refunds.py
          cases.py
          knowledge.py
          approvals.py
          activities.py
          observability.py
          cost.py
          evaluation.py

        services/
          __init__.py
          mock_data_service.py
          dataverse_service.py
          azure_search_service.py
          power_automate_service.py
          cost_service.py
          telemetry_service.py

        models/
          __init__.py
          account.py
          contact.py
          product.py
          order.py
          order_item.py
          shipment.py
          return_request.py
          refund.py
          support_case.py
          knowledge.py
          approval.py
          activity.py
          agent_run.py
          cost.py
          evaluation.py

        data/
          accounts.json
          contacts.json
          products.json
          orders.json
          order_items.json
          shipments.json
          returns.json
          refunds.json
          cases.json
          activities.json
          knowledge_articles.json
          approvals.json
          agent_runs.json
          pricing.json

    tests/
      test_customers.py
      test_orders.py
      test_shipments.py
      test_returns.py
      test_refunds.py
      test_cases.py
      test_knowledge.py
      test_approvals.py
      test_cost.py
      test_evaluation.py

  agents/
    intake-agent/
    knowledge-agent/
    data-agent/
    governance-agent/
    draft-agent/
    critic-agent/
    cost-agent/
    workflow-agent/

  copilot-studio/
    exported-agent/
    agent-flows/
    screenshots/
    README.md

  foundry/
    agent-definitions/
    evaluation-config/
    tracing-config/
    screenshots/
    README.md

  power-platform/
    solutions/
    flows/
    dataverse-schema/
    screenshots/
    README.md

  infrastructure/
    pulumi/
    scripts/

  data/
    sample-documents/
    sample-dataverse-records/
    seed-scripts/

  dashboards/
    powerbi/
    screenshots/
    README.md
```

---

## MVP Build Plan

## Day 1: Project Setup

Deliverables:

```text
repository structure
context.md
README.md
architecture.md
MCP tool contracts
Dataverse schema draft
API contracts
```

## Day 2: MCP Server Local MVP

Deliverables:

```text
local MCP Server
mock JSON data
get_customer_by_email
get_latest_order
get_order_items
get_shipment_status
Cursor MCP test
```

## Day 3: Additional MCP Tools

Deliverables:

```text
get_returns_for_order
get_refunds_for_order
search_knowledge_articles
create_approval_request
calculate_agent_run_cost
log_agent_run
evaluate_response
```

## Day 4: Orchestrator API

Deliverables:

```text
Azure Function or local API skeleton
webshop order support endpoint
request/response models
MCP client integration
basic run logging
```

## Day 5: Pulumi Infrastructure

Deliverables:

```text
Pulumi project
Azure context JSON bootstrap
Microsoft CAF-aligned naming
Sequence-managed disposable resource names
One-line teardown script
Persistent recovery blob design
Resource Group
Storage Account
Function App
Application Insights
Key Vault
```

## Day 6: Dataverse Setup

Deliverables:

```text
Power Platform Developer Environment
custom Dataverse tables
sample records
model-driven app optional
Dataverse connector test
```

## Day 7: Dataverse Integration

Deliverables:

```text
replace mock customer/order retrieval with Dataverse
replace mock shipment/return/refund retrieval with Dataverse
replace mock approval logging with Dataverse
keep mock fallback mode
```

## Day 8: Secure RAG

Deliverables:

```text
sample policy documents
Azure AI Search index
document ingestion
search_knowledge_articles backed by Azure AI Search
citations and confidence scores
```

## Day 9: Microsoft Agent Framework + Copilot Studio

Deliverables:

```text
Intake Agent using Microsoft Agent Framework
Data Agent
Knowledge Agent
Governance Agent using Microsoft Agent Framework
Draft Agent using Semantic Kernel for comparison
Critic Agent using Microsoft Agent Framework
Cost Agent
Copilot Studio test agent
Copilot Studio action calling Orchestrator API
```

## Day 10: Workflow, Observability and Demo Polish

Deliverables:

```text
Power Apps approval console
token/cost tracking
latency logging
model tracking
Application Insights or Dataverse logging
Power BI dashboard
demo video
architecture diagram
interview talking points
CV bullet
LinkedIn post
```

---

## Post-MVP Phase: Microsoft 365 Agents SDK

Deliverables:

```text
Microsoft 365 Agents SDK project
Microsoft 365 Agents Playground test
custom-engine agent connected to Orchestrator API
reuse of Microsoft Agent Framework orchestration
reuse of the single Semantic Kernel Draft Agent only as comparison track
reuse of Enterprise AgentOps MCP Server tools
optional Teams deployment if tenant/sideloading is available
screenshots and demo notes
```

---

## Demo Conversation

User:

```text
Find the latest order for john.smith@contoso.com, check delivery and refund issues, validate the delivery postcode, summarise the situation and create an approval request if compensation is required.
```

Tool calls:

```text
get_customer_by_email(email="john.smith@contoso.com")
get_latest_order(contactId="con-001")
get_order_details(orderId="ord-1001")
get_order_items(orderId="ord-1001")
get_shipment_status(shipmentId="ship-9001")
geocode_delivery_postcode(postcode="IP1 1AA")
calculate_delivery_distance_or_route(origin="Demo Warehouse", destinationPostcode="IP1 1AA")
get_returns_for_order(orderId="ord-1001")
get_refunds_for_order(orderId="ord-1001")
search_knowledge_articles(query="delivery delay compensation refund approval policy")
evaluate_response(...)
create_approval_request(...)
calculate_agent_run_cost(...)
log_agent_run(...)
```

Expected final response:

```text
John Smith's latest order is WEB-1001 for Contoso Ltd.

The order has been paid and shipped, but the shipment is currently delayed due to a carrier network disruption. The order includes a Premium Coffee Machine and a Coffee Capsules Pack.

There is a return request linked to the delivery delay, and a refund record for £49.99 is currently pending approval.

Relevant policy indicates that compensation or refund communication for high-risk delivery issues requires service manager approval before being sent externally.

I created an approval request for compensation review.

Approval ID: apr-9001
Status: Pending

Estimated agent run cost: $0.012
```

---

## Interview Summary

This project is a Microsoft Agentic AI reference architecture.

It combines Copilot Studio for the business-facing test chat agent, Microsoft Foundry (formerly Azure AI Foundry) for managed agent capability, Microsoft Agent Framework (successor to Semantic Kernel + AutoGen) for code-first orchestration, a custom MCP Server for governed enterprise tools, Dataverse for business data and approval records, Power Apps for the approval console, Azure AI Search for Secure RAG, Logic Apps and Service Bus for integration workflow, Pulumi for Azure infrastructure, and Application Insights / Power BI for observability and AI cost engineering.

The architecture also includes Microsoft 365 Agents SDK as a final-phase custom-engine agent surface, allowing the same Orchestrator API and MCP-based tool layer to be reused beyond Copilot Studio.

The purpose is to show how enterprise AI agents can move beyond chatbot demos and become governed, auditable, cost-aware workflows connected to real business systems.

---

## CV Bullet

Built an Enterprise AgentOps Control Tower reference architecture demonstrating end-to-end Microsoft Agentic AI across Copilot Studio, Microsoft Foundry (formerly Azure AI Foundry), Foundry Agent Service, Microsoft Agent Framework (successor to Semantic Kernel + AutoGen), MCP Server, Secure RAG, Azure AI Search, Dataverse, Power Apps, Power Platform, Logic Apps, Service Bus, Azure Functions, Pulumi, observability and AI cost engineering. The solution orchestrates multiple agents, enterprise data, workflow approvals, governance checks, audit trails, token/cost tracking, MCP tools and operational dashboards into a single controlled agentic workflow.

---

## Final Architecture Message

Copilot Studio test chat is the business-facing agent layer for MVP.

Microsoft 365 Agents SDK is the final-phase custom-engine agent surface, initially tested through Microsoft 365 Agents Playground and optionally deployable to Teams when a suitable tenant is available.

Microsoft Foundry (formerly Azure AI Foundry) is the managed AI agent platform.

Microsoft Agent Framework (successor to Semantic Kernel + AutoGen) is the pro-code orchestration layer.

Semantic Kernel remains only as the Draft Agent comparison implementation.

The Enterprise AgentOps MCP Server is the governed enterprise tool layer.

OpenStreetMap / Geocoding MCP Server is the external/public MCP server used to enrich delivery workflows with postcode validation, geocoding, route distance and delivery-location context.

Dataverse is the business data layer.

Azure AI Search is the Secure RAG layer.

Power Apps is the human approval surface. Logic Apps, Service Bus and Azure Functions are the workflow and integration layer. Power Automate remains an optional notification/integration channel.

Pulumi is the infrastructure as code layer.

Application Insights, Azure Monitor and Power BI are the observability and cost engineering layer.

Together, they form a practical enterprise architecture for secure, auditable, cost-controlled AI agents connected to real business systems.
