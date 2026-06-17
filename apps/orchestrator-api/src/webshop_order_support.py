import time

from src.shared.mcp_client import MCPClient


def handle_webshop_order_support(body: dict) -> tuple[dict, int]:
    start = time.time()
    client = MCPClient()

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

    summary = (
        f"{customer['fullName']}'s latest order is {order['orderNumber']}. "
        f"Delivery status: {order['deliveryStatus']}."
    )
    if has_delay:
        summary += f" Shipment delayed: {shipment.get('delayReason', 'unknown reason')}."
    if has_refund:
        summary += " A refund request is pending approval."

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

    latency_ms = int((time.time() - start) * 1000)
    model_used = "claude-sonnet-4-6"
    vendor = "Anthropic"

    cost = client.call(
        "calculate_agent_run_cost",
        {
            "vendor": vendor,
            "model": model_used,
            "input_tokens": 1500,
            "output_tokens": 400,
        },
    )
    log = client.call(
        "log_agent_run",
        {
            "workflow_name": "WebshopOrderSupport",
            "intent": "SummariseLatestOrderIssue",
            "model_used": model_used,
            "vendor": vendor,
            "input_tokens": 1500,
            "output_tokens": 400,
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
