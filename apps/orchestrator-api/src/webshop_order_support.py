import time

from src.shared.azure_openai_client import generate_order_support_summary
from src.shared.mcp_client import MCPClient


def handle_webshop_order_support(body: dict) -> tuple[dict, int]:
    start = time.time()
    client = MCPClient()
    from enterprise_agentops_mcp.services.service_bus_service import (
        send_agent_run_event,
        send_approval_request_event,
    )
    from enterprise_agentops_mcp import config

    customer_email = body.get("customerEmail")
    if not customer_email:
        return {"error": "customerEmail is required"}, 400

    customer = client.call("get_customer_by_email", {"email": customer_email})
    if "error" in customer:
        return customer, 404

    order = client.call("get_latest_order", {"contact_id": customer["contactId"]})
    if "error" in order:
        return order, 404

    order_items = client.call("get_order_items", {"order_id": order["orderId"]})
    shipment = client.call("get_shipment_status", {"shipment_id": order["shipmentId"]})
    returns = client.call("get_returns_for_order", {"order_id": order["orderId"]})
    refunds = client.call("get_refunds_for_order", {"order_id": order["orderId"]})
    knowledge = client.call(
        "search_knowledge_articles",
        {"query": "delivery delay compensation refund approval policy", "max_results": 3},
    )

    has_delay = shipment.get("status") == "Delayed"
    refund_rows = refunds.get("refunds", [])
    has_refund = any(item.get("requiresApproval") for item in refund_rows)
    risk = "High" if has_delay and has_refund else "Medium"

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
    log = client.call(
        "log_agent_run",
        {
            "workflow_name": "WebshopOrderSupport",
            "intent": "SummariseLatestOrderIssue",
            "model_used": model_used,
            "vendor": vendor,
            "input_tokens": ai_summary["inputTokens"],
            "output_tokens": ai_summary["outputTokens"],
            "latency_ms": latency_ms,
            "tools_called": [
                "get_customer_by_email",
                "get_latest_order",
                "get_order_items",
                "get_shipment_status",
                "get_returns_for_order",
                "get_refunds_for_order",
                "search_knowledge_articles",
                "evaluate_response",
                "create_approval_request",
            ],
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
            "intent": "SummariseLatestOrderIssue",
            "customerEmail": customer_email,
            "customerName": customer["fullName"],
            "orderNumber": order["orderNumber"],
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
        "items": order_items.get("items", []),
        "returns": returns.get("returns", []),
        "refunds": refund_rows,
        "knowledge": knowledge.get("results", []),
    }, 200
