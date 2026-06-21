import time
import asyncio

from src.agents.critic_agent import CriticAgent
from src.agents.cost_agent import CostAgent
from src.agents.data_agent import DataAgent
from src.agents.governance_agent import GovernanceAgent
from src.agents.intake_agent import IntakeAgent
from src.agents.knowledge_agent import KnowledgeAgent
from src.agents.workflow_agent import WorkflowAgent
from src.shared.azure_openai_client import generate_order_support_summary
from src.shared.mcp_client import MCPClient


def classify_order_support_request(user_message: str) -> dict:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(IntakeAgent().classify_request(user_message))

    raise RuntimeError(
        "classify_order_support_request cannot run inside an active event loop. "
        "Use IntakeAgent.classify_request directly from async code."
    )


def handle_webshop_order_support(body: dict) -> tuple[dict, int]:
    start = time.time()
    client = MCPClient()
    from enterprise_agentops_mcp import config

    customer_email = body.get("customerEmail")
    user_message = body.get("message") or body.get("userMessage") or body.get("prompt")
    if not user_message and customer_email:
        user_message = f"Summarise the latest order support issue for {customer_email}."
    if not user_message:
        return {"error": "customerEmail or message is required"}, 400

    intake = classify_order_support_request(user_message)
    customer_email = customer_email or intake.get("contactEmail")
    if not customer_email:
        return {"error": "customerEmail is required or must be present in message"}, 400

    intent = intake.get("intent") or "SummariseLatestOrderIssue"
    intake_tools_required = intake.get("toolsRequired", [])
    workflow = WorkflowAgent(client)
    thread_state = workflow.start_thread(
        thread_id=body.get("threadId"),
        workflow_name="WebshopOrderSupport",
        customer_email=customer_email,
        intent=intent,
    )

    data = DataAgent(client).fetch_order_support_data(customer_email)
    if "error" in data:
        return {"error": data["error"]}, data.get("statusCode", 500)

    customer = data["customer"]
    order = data["order"]
    order_items = data["orderItems"]
    shipment = data["shipment"]
    returns = data["returns"]
    refunds = data["refunds"]

    refund_rows = refunds.get("refunds", [])
    governance = GovernanceAgent().assess_order_support_risk(
        shipment=shipment,
        refunds=refunds,
        returns=returns,
        intake=intake,
    )
    risk = governance["risk"]
    knowledge = KnowledgeAgent(client).search_order_support_knowledge(
        shipment=shipment,
        refunds=refunds,
        returns=returns,
        intake=intake,
        risk=risk,
        max_results=3,
    )

    ai_summary = generate_order_support_summary(
        customer=customer,
        order=order,
        shipment=shipment,
        refunds=refund_rows,
        returns=returns.get("returns", []),
        knowledge=knowledge.get("results", []),
        risk=risk,
    )
    summary = ai_summary["summary"]

    evaluation = CriticAgent(client).evaluate_order_support_summary(
        summary=summary,
        order=order,
        shipment=shipment,
        risk=risk,
    )

    approval_outcome = workflow.create_approval_if_required(
        governance=governance,
        order=order,
        customer=customer,
        customer_email=customer_email,
        thread_state=thread_state,
    ).model_dump()

    latency_ms = int((time.time() - start) * 1000)
    model_used = config.AI_PRIMARY_MODEL
    vendor = config.AI_PRIMARY_VENDOR

    cost = CostAgent(client).calculate_run_cost(
        vendor=vendor,
        model=model_used,
        input_tokens=ai_summary["inputTokens"],
        output_tokens=ai_summary["outputTokens"],
    )
    tools_called = (
        data["toolsCalled"]
        + knowledge["toolsCalled"]
        + evaluation["toolsCalled"]
        + cost["toolsCalled"]
        + approval_outcome["toolsCalled"]
    )

    log = workflow.log_and_publish_run(
        thread_state=thread_state,
        intent=intent,
        model_used=model_used,
        vendor=vendor,
        input_tokens=ai_summary["inputTokens"],
        output_tokens=ai_summary["outputTokens"],
        latency_ms=latency_ms,
        tools_called=tools_called,
        approval_outcome=approval_outcome,
        governance=governance,
        evaluation=evaluation,
        cost=cost,
        customer_email=customer_email,
        customer=customer,
        order=order,
    )

    return {
        "runId": log.get("runId"),
        "threadId": thread_state.threadId,
        "threadStatus": thread_state.status,
        "customerName": customer["fullName"],
        "orderNumber": order["orderNumber"],
        "summary": summary,
        "approvalRequired": approval_outcome["humanInTheLoop"],
        "approvalStatus": approval_outcome["approvalStatus"],
        "approvalId": approval_outcome["approvalId"],
        "qualityScore": evaluation.get("qualityScore"),
        "groundednessScore": evaluation.get("groundednessScore"),
        "estimatedCost": cost.get("estimatedCost"),
        "modelUsed": model_used,
        "latencyMs": latency_ms,
        "intent": intent,
        "intake": intake,
        "governance": governance,
        "humanInTheLoop": approval_outcome["humanInTheLoop"],
        "items": order_items.get("items", []),
        "returns": returns.get("returns", []),
        "refunds": refund_rows,
        "knowledge": knowledge.get("results", []),
    }, 200
