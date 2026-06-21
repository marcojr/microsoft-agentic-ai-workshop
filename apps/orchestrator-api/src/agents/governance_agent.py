class GovernanceAgent:
    """Applies deterministic approval and risk rules for order-support workflows."""

    def assess_order_support_risk(
        self,
        *,
        shipment: dict,
        refunds: dict,
        returns: dict,
        intake: dict,
    ) -> dict:
        # Step 1: Extract the business signals that affect risk and approvals.
        has_delay = shipment.get("status") == "Delayed"
        refund_rows = refunds.get("refunds", [])
        return_rows = returns.get("returns", [])
        has_approval_refund = any(item.get("requiresApproval") for item in refund_rows)

        # Step 2: Apply the current deterministic approval rules.
        requires_approval = has_delay and has_approval_refund
        risk = self._select_risk_level(
            has_delay=has_delay,
            has_approval_refund=has_approval_refund,
            has_returns=bool(return_rows),
            intake_risk=intake.get("riskLevel"),
        )

        # Step 3: Return a shaped governance decision for downstream agents.
        return {
            "risk": risk,
            "requiresApproval": requires_approval,
            "approvalType": "Compensation" if requires_approval else "None",
            "reason": (
                "Delayed shipment with pending refund"
                if requires_approval
                else "No approval required by current deterministic rules"
            ),
            "approvalTrigger": (
                "DelayedShipmentWithRefundApproval"
                if requires_approval
                else "None"
            ),
        }

    @staticmethod
    def _select_risk_level(
        *,
        has_delay: bool,
        has_approval_refund: bool,
        has_returns: bool,
        intake_risk: str | None,
    ) -> str:
        if has_delay and has_approval_refund:
            return "High"
        if intake_risk == "High" or has_delay or has_approval_refund or has_returns:
            return "Medium"
        return "Low"
