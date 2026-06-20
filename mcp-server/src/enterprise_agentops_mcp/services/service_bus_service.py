import json
from datetime import UTC, datetime
from typing import Any

from azure.servicebus import ServiceBusClient, ServiceBusMessage

from enterprise_agentops_mcp import config


def _send_json_message(queue_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    if not config.AZURE_SERVICE_BUS_CONNECTION_STRING:
        raise RuntimeError("AZURE_SERVICE_BUS_CONNECTION_STRING is required")

    message_payload = {
        "publishedAt": datetime.now(UTC).isoformat(),
        **payload,
    }
    message = ServiceBusMessage(
        json.dumps(message_payload),
        content_type="application/json",
    )

    with ServiceBusClient.from_connection_string(
        config.AZURE_SERVICE_BUS_CONNECTION_STRING
    ) as client:
        with client.get_queue_sender(queue_name=queue_name) as sender:
            sender.send_messages(message)

    return {
        "queue": queue_name,
        "messageType": payload.get("messageType"),
        "published": True,
    }


def send_approval_request_event(payload: dict[str, Any]) -> dict[str, Any]:
    return _send_json_message(
        config.SERVICE_BUS_APPROVAL_REQUESTS_QUEUE,
        {
            "messageType": "ApprovalRequestCreated",
            **payload,
        },
    )


def send_agent_run_event(payload: dict[str, Any]) -> dict[str, Any]:
    return _send_json_message(
        config.SERVICE_BUS_AGENT_RUN_EVENTS_QUEUE,
        {
            "messageType": "AgentRunCompleted",
            **payload,
        },
    )
