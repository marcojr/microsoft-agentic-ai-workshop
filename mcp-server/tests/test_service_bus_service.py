import json

from enterprise_agentops_mcp import config
from enterprise_agentops_mcp.services import service_bus_service


class FakeSender:
    def __init__(self, sent_messages: list) -> None:
        self.sent_messages = sent_messages

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def send_messages(self, message) -> None:
        self.sent_messages.append(message)


class FakeMessage:
    def __init__(self, body: str, content_type: str) -> None:
        self.body = body
        self.content_type = content_type


class FakeClient:
    sent_messages = []
    queue_name = None
    connection_string = None

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
        FakeClient.connection_string = connection_string

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    @classmethod
    def from_connection_string(cls, connection_string: str):
        return cls(connection_string)

    def get_queue_sender(self, queue_name: str):
        FakeClient.queue_name = queue_name
        return FakeSender(FakeClient.sent_messages)


def test_send_agent_run_event_publishes_json_message(monkeypatch) -> None:
    FakeClient.sent_messages = []
    monkeypatch.setattr(config, "AZURE_SERVICE_BUS_CONNECTION_STRING", "Endpoint=sb://fake")
    monkeypatch.setattr(config, "SERVICE_BUS_AGENT_RUN_EVENTS_QUEUE", "agent-run-events")
    monkeypatch.setattr(service_bus_service, "ServiceBusClient", FakeClient)
    monkeypatch.setattr(service_bus_service, "ServiceBusMessage", FakeMessage)

    result = service_bus_service.send_agent_run_event(
        {
            "runId": "run-001",
            "workflowName": "WebshopOrderSupport",
        }
    )

    sent_message = FakeClient.sent_messages[0]
    sent_payload = json.loads(sent_message.body)
    assert result["published"] is True
    assert result["queue"] == "agent-run-events"
    assert FakeClient.queue_name == "agent-run-events"
    assert sent_message.content_type == "application/json"
    assert sent_payload["messageType"] == "AgentRunCompleted"
    assert sent_payload["runId"] == "run-001"
