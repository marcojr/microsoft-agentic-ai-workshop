from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


RiskLevel = Literal["Low", "Medium", "High"]
ApprovalType = Literal["Compensation", "Refund", "Escalation", "None"]
ApprovalStatus = Literal["NotRequired", "Pending", "Approved", "Rejected"]
ThreadStatus = Literal[
    "Started",
    "WaitingForApproval",
    "Completed",
    "Blocked",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class GovernanceDecision(BaseModel):
    risk: RiskLevel
    requiresApproval: bool
    approvalType: ApprovalType
    reason: str
    approvalTrigger: str


class ApprovalOutcome(BaseModel):
    approvalId: str | None = None
    approvalStatus: ApprovalStatus
    humanInTheLoop: bool
    toolsCalled: list[str] = Field(default_factory=list)


class ApprovalDecisionRequest(BaseModel):
    approvalId: str
    decision: Literal["Approved", "Rejected"]
    approvedBy: str
    comment: str | None = None
    threadId: str | None = None


class ThreadState(BaseModel):
    threadId: str = Field(default_factory=lambda: f"thread-{uuid4().hex[:8]}")
    workflowName: str
    status: ThreadStatus = "Started"
    customerEmail: str | None = None
    intent: str | None = None
    orderId: str | None = None
    approvalId: str | None = None
    currentStep: str = "intake"
    createdAt: str = Field(default_factory=utc_now)
    updatedAt: str = Field(default_factory=utc_now)
    context: dict[str, Any] = Field(default_factory=dict)
