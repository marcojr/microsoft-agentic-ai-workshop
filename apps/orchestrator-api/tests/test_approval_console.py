from src.approval_console import decide_approval, list_pending_approvals
from src.shared.thread_state_store import ThreadStateStore


def test_list_pending_approvals_returns_mcp_payload(monkeypatch) -> None:
    class FakeClient:
        def call(self, tool_name: str, params: dict) -> dict:
            assert tool_name == "list_pending_approval_requests"
            assert params == {"limit": 100}
            return {"approvals": [{"approvalId": "apr-1", "status": "Pending"}]}

    monkeypatch.setattr("src.approval_console.MCPClient", FakeClient)

    result, status = list_pending_approvals()

    assert status == 200
    assert result["approvals"][0]["approvalId"] == "apr-1"


def test_decide_approval_updates_thread_state(tmp_path, monkeypatch) -> None:
    store = ThreadStateStore(tmp_path / "thread_state.json")
    state = store.get_or_create(
        thread_id="thread-1",
        workflow_name="WebshopOrderSupport",
        customer_email="john.smith@contoso.com",
        intent="Investigate delayed order",
    )
    state.status = "WaitingForApproval"
    state.approvalId = "apr-1"
    store.save(state)

    class FakeClient:
        def call(self, tool_name: str, params: dict) -> dict:
            assert tool_name == "decide_approval_request"
            return {
                "approvalId": params["approval_id"],
                "status": params["decision"],
                "approvedBy": params["approved_by"],
                "threadId": "thread-1",
                "customerEmail": "john.smith@contoso.com",
                "decidedOn": "2026-06-21T12:00:00+00:00",
            }

    monkeypatch.setattr("src.approval_console.MCPClient", FakeClient)
    monkeypatch.setattr(
        "src.approval_console.ThreadStateStore",
        lambda: store,
    )

    result, status = decide_approval(
        {
            "approvalId": "apr-1",
            "decision": "Approved",
            "approvedBy": "manager@contoso.com",
            "comment": "Approved.",
        }
    )

    assert status == 200
    assert result["threadStatus"] == "Completed"
    rehydrated = store.get_or_create(
        thread_id="thread-1",
        workflow_name="WebshopOrderSupport",
        customer_email=None,
        intent=None,
    )
    assert rehydrated.status == "Completed"
    assert rehydrated.context["approvalDecision"] == "Approved"


def test_decide_approval_rejects_invalid_decision() -> None:
    result, status = decide_approval(
        {
            "approvalId": "apr-1",
            "decision": "Maybe",
            "approvedBy": "manager@contoso.com",
        }
    )

    assert status == 400
    assert result["error"] == "Invalid approval decision request"
