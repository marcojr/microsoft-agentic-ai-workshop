from src.agents.workflow_agent import WorkflowAgent
from src.shared.thread_state_store import ThreadStateStore


class _FakeMCPClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def call(self, tool_name: str, params: dict) -> dict:
        self.calls.append((tool_name, params))
        if tool_name == "create_approval_request":
            return {"approvalId": "apr-1", "status": "Pending"}
        if tool_name == "log_agent_run":
            return {"logged": True, "runId": "run-1", "estimatedCost": 0.0001}
        raise AssertionError(f"Unexpected tool: {tool_name}")


def test_workflow_agent_creates_human_approval_and_updates_thread(
    tmp_path,
    monkeypatch,
) -> None:
    from enterprise_agentops_mcp.services import service_bus_service

    events = []
    monkeypatch.setattr(
        service_bus_service,
        "send_approval_request_event",
        lambda payload: events.append(payload),
    )
    agent = WorkflowAgent(
        _FakeMCPClient(),
        ThreadStateStore(tmp_path / "thread_state.json"),
    )
    thread = agent.start_thread(
        thread_id=None,
        workflow_name="WebshopOrderSupport",
        customer_email="john.smith@contoso.com",
        intent="Investigate delayed order",
    )

    result = agent.create_approval_if_required(
        governance={
            "risk": "High",
            "requiresApproval": True,
            "approvalType": "Compensation",
            "reason": "Delayed shipment with pending refund",
            "approvalTrigger": "DelayedShipmentWithRefundApproval",
        },
        order={"orderId": "ord-1", "orderNumber": "WEB-1"},
        customer={"fullName": "John Smith"},
        customer_email="john.smith@contoso.com",
        thread_state=thread,
    )

    assert result.approvalId == "apr-1"
    assert result.approvalStatus == "Pending"
    assert result.humanInTheLoop is True
    assert thread.status == "WaitingForApproval"
    assert agent.mcp.calls[0][1]["thread_id"] == thread.threadId
    assert agent.mcp.calls[0][1]["customer_name"] == "John Smith"
    assert agent.mcp.calls[0][1]["order_number"] == "WEB-1"
    assert events[0]["threadId"] == thread.threadId


def test_workflow_agent_logs_and_publishes_run(tmp_path, monkeypatch) -> None:
    from enterprise_agentops_mcp.services import service_bus_service

    events = []
    monkeypatch.setattr(
        service_bus_service,
        "send_agent_run_event",
        lambda payload: events.append(payload),
    )
    agent = WorkflowAgent(
        _FakeMCPClient(),
        ThreadStateStore(tmp_path / "thread_state.json"),
    )
    thread = agent.start_thread(
        thread_id=None,
        workflow_name="WebshopOrderSupport",
        customer_email="john.smith@contoso.com",
        intent="Investigate delayed order",
    )

    result = agent.log_and_publish_run(
        thread_state=thread,
        intent="Investigate delayed order",
        model_used="gpt-5-mini",
        vendor="Azure OpenAI",
        input_tokens=100,
        output_tokens=30,
        latency_ms=250,
        tools_called=["get_customer_by_email"],
        approval_outcome={
            "approvalId": None,
            "approvalStatus": "NotRequired",
            "humanInTheLoop": False,
            "toolsCalled": [],
        },
        governance={
            "risk": "Low",
            "requiresApproval": False,
            "approvalType": "None",
            "reason": "No approval required",
            "approvalTrigger": "None",
        },
        evaluation={"riskScore": 0.2, "qualityScore": 0.92, "groundednessScore": 0.88},
        cost={"estimatedCost": 0.0001},
        customer_email="john.smith@contoso.com",
        customer={"fullName": "John Smith"},
        order={"orderNumber": "WEB-1"},
    )

    assert result["runId"] == "run-1"
    assert events[0]["threadId"] == thread.threadId
    assert thread.status == "Completed"
