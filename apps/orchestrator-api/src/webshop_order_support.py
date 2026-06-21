import time
import asyncio

from src.agents.data_agent import DataAgent
from src.agents.intake_agent import IntakeAgent
from src.agents.knowledge_agent import KnowledgeAgent
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
    from enterprise_agentops_mcp.services.service_bus_service import (
        send_agent_run_event,
        send_approval_request_event,
    )
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

    data = DataAgent(client).fetch_order_support_data(customer_email)
    if "error" in data:
        return {"error": data["error"]}, data.get("statusCode", 500)

    customer = data["customer"]
    order = data["order"]
    order_items = data["orderItems"]
    shipment = data["shipment"]
    returns = data["returns"]
    refunds = data["refunds"]

    has_delay = shipment.get("status") == "Delayed"
    refund_rows = refunds.get("refunds", [])
    has_refund = any(item.get("requiresApproval") for item in refund_rows)
    risk = "High" if has_delay and has_refund else "Medium"
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

    evaluation = client.call(
        "evaluate_response",
        {
            "response": summary,
            "required_sources": [order["orderId"], order.get("shipmentId", "")],
            "risk_level": risk,
        },
    )

    approval_id = None
    if has_delay and has_refund:
        approval = client.call(
            "create_approval_request",
            {
                "related_record_id": order["orderId"],
                "related_record_type": "order",
                "approval_type": "Compensation",
                "reason": "Delayed shipment with pending refund",
                "risk_level": "High",
                "requested_by": "orchestrator",
            },
        )
        approval_id = approval.get("approvalId")
        send_approval_request_event(
            {
                "approvalId": approval_id,
                "relatedRecordId": order["orderId"],
                "relatedRecordType": "order",
                "approvalType": "Compensation",
                "riskLevel": "High",
                "customerEmail": customer_email,
                "customerName": customer["fullName"],
                "orderNumber": order["orderNumber"],
                "reason": "Delayed shipment with pending refund",
            }
        )

    latency_ms = int((time.time() - start) * 1000)
    model_used = config.AI_PRIMARY_MODEL
    vendor = config.AI_PRIMARY_VENDOR

    cost = client.call(
        "calculate_agent_run_cost",
        {
            "vendor": vendor,
            "model": model_used,
            "input_tokens": ai_summary["inputTokens"],
            "output_tokens": ai_summary["outputTokens"],
        },
    )
    tools_called = data["toolsCalled"] + knowledge["toolsCalled"] + [
        "evaluate_response",
        "calculate_agent_run_cost",
    ]
    if approval_id is not None:
        tools_called.append("create_approval_request")

    log = client.call(
        "log_agent_run",
        {
            "workflow_name": "WebshopOrderSupport",
            "intent": intent,
            "model_used": model_used,
            "vendor": vendor,
            "input_tokens": ai_summary["inputTokens"],
            "output_tokens": ai_summary["outputTokens"],
            "latency_ms": latency_ms,
            "tools_called": tools_called,
            "requires_approval": approval_id is not None,
            "risk_score": evaluation.get("riskScore", 0.0),
            "quality_score": evaluation.get("qualityScore", 0.0),
            "groundedness_score": evaluation.get("groundednessScore", 0.0),
        },
    )
    send_agent_run_event(
        {
            "runId": log.get("runId"),
            "workflowName": "WebshopOrderSupport",
            "intent": intent,
            "customerEmail": customer_email,
            "customerName": customer["fullName"],
            "orderNumber": order["orderNumber"],
            "intakeToolsRequired": intake_tools_required,
            "requiresApproval": approval_id is not None,
            "approvalId": approval_id,
            "riskScore": evaluation.get("riskScore", 0.0),
            "qualityScore": evaluation.get("qualityScore", 0.0),
            "groundednessScore": evaluation.get("groundednessScore", 0.0),
            "estimatedCost": cost.get("estimatedCost"),
            "modelUsed": model_used,
            "latencyMs": latency_ms,
        }
    )

    return {
        "runId": log.get("runId"),
        "customerName": customer["fullName"],
        "orderNumber": order["orderNumber"],
        "summary": summary,
        "approvalRequired": approval_id is not None,
        "approvalId": approval_id,
        "qualityScore": evaluation.get("qualityScore"),
        "groundednessScore": evaluation.get("groundednessScore"),
        "estimatedCost": cost.get("estimatedCost"),
        "modelUsed": model_used,
        "latencyMs": latency_ms,
        "intent": intent,
        "intake": intake,
        "items": order_items.get("items", []),
        "returns": returns.get("returns", []),
        "refunds": refund_rows,
        "knowledge": knowledge.get("results", []),
    }, 200
