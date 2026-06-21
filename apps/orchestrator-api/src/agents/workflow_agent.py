from src.agents.models import ApprovalOutcome, GovernanceDecision, ThreadState
from src.shared.mcp_client import MCPClient
from src.shared.thread_state_store import ThreadStateStore


class WorkflowAgent:
    """Coordinates human approval, run logging, events, and thread state."""

    def __init__(
        self,
        mcp_client: MCPClient | None = None,
        thread_store: ThreadStateStore | None = None,
    ) -> None:
        # Step 1: Keep workflow side effects behind MCP and a thread-state store.
        self.mcp = mcp_client or MCPClient()
        self.thread_store = thread_store or ThreadStateStore()

    def start_thread(
        self,
        *,
        thread_id: str | None,
        workflow_name: str,
        customer_email: str | None,
        intent: str | None,
    ) -> ThreadState:
        # Step 2: Rehydrate or create the thread for this workflow turn.
        return self.thread_store.get_or_create(
            thread_id=thread_id,
            workflow_name=workflow_name,
            customer_email=customer_email,
            intent=intent,
        )

    def create_approval_if_required(
        self,
        *,
        governance: dict,
        order: dict,
        customer: dict,
        customer_email: str,
        thread_state: ThreadState,
    ) -> ApprovalOutcome:
        decision = GovernanceDecision.model_validate(governance)
        if not decision.requiresApproval:
            return ApprovalOutcome(
                approvalStatus="NotRequired",
                humanInTheLoop=False,
            )

        # Step 3: Create the human approval request through the MCP approval tool.
        approval = self.mcp.call(
            "create_approval_request",
            {
                "related_record_id": order["orderId"],
                "related_record_type": "order",
                "approval_type": decision.approvalType,
                "reason": decision.reason,
                "risk_level": decision.risk,
                "requested_by": "orchestrator",
                "thread_id": thread_state.threadId,
                "customer_name": customer["fullName"],
                "customer_email": customer_email,
                "order_number": order["orderNumber"],
            },
        )
        approval_id = approval.get("approvalId")

        # Step 4: Publish the approval event for downstream human-in-the-loop workflow.
        from enterprise_agentops_mcp.services.service_bus_service import (
            send_approval_request_event,
        )

        send_approval_request_event(
            {
                "approvalId": approval_id,
                "threadId": thread_state.threadId,
                "relatedRecordId": order["orderId"],
                "relatedRecordType": "order",
                "approvalType": decision.approvalType,
                "riskLevel": decision.risk,
                "customerEmail": customer_email,
                "customerName": customer["fullName"],
                "orderNumber": order["orderNumber"],
                "reason": decision.reason,
            }
        )

        thread_state.status = "WaitingForApproval"
        thread_state.currentStep = "human_approval"
        thread_state.orderId = order["orderId"]
        thread_state.approvalId = approval_id
        self.thread_store.save(thread_state)

        return ApprovalOutcome(
            approvalId=approval_id,
            approvalStatus="Pending",
            humanInTheLoop=True,
            toolsCalled=["create_approval_request"],
        )

    def log_and_publish_run(
        self,
        *,
        thread_state: ThreadState,
        intent: str,
        model_used: str,
        vendor: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: int,
        tools_called: list[str],
        approval_outcome: dict,
        governance: dict,
        evaluation: dict,
        cost: dict,
        customer_email: str,
        customer: dict,
        order: dict,
    ) -> dict:
        approval = ApprovalOutcome.model_validate(approval_outcome)

        # Step 5: Log the agent run through the MCP observability tool.
        log = self.mcp.call(
            "log_agent_run",
            {
                "workflow_name": thread_state.workflowName,
                "intent": intent,
                "model_used": model_used,
                "vendor": vendor,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "latency_ms": latency_ms,
                "tools_called": tools_called,
                "requires_approval": approval.humanInTheLoop,
                "risk_score": evaluation.get("riskScore", 0.0),
                "quality_score": evaluation.get("qualityScore", 0.0),
                "groundedness_score": evaluation.get("groundednessScore", 0.0),
            },
        )

        # Step 6: Publish a run event and update the thread with final run metadata.
        from enterprise_agentops_mcp.services.service_bus_service import (
            send_agent_run_event,
        )

        event = {
            "runId": log.get("runId"),
            "threadId": thread_state.threadId,
            "workflowName": thread_state.workflowName,
            "intent": intent,
            "customerEmail": customer_email,
            "customerName": customer["fullName"],
            "orderNumber": order["orderNumber"],
            "governance": governance,
            "approvalStatus": approval.approvalStatus,
            "requiresApproval": approval.humanInTheLoop,
            "approvalId": approval.approvalId,
            "riskScore": evaluation.get("riskScore", 0.0),
            "qualityScore": evaluation.get("qualityScore", 0.0),
            "groundednessScore": evaluation.get("groundednessScore", 0.0),
            "estimatedCost": cost.get("estimatedCost"),
            "modelUsed": model_used,
            "latencyMs": latency_ms,
        }
        send_agent_run_event(event)

        if thread_state.status != "WaitingForApproval":
            thread_state.status = "Completed"
            thread_state.currentStep = "completed"
        thread_state.context.update({"lastRunId": log.get("runId")})
        self.thread_store.save(thread_state)

        return {
            **log,
            "event": event,
            "toolsCalled": ["log_agent_run"],
        }
