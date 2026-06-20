import asyncio


def generate_order_support_summary(
    *,
    customer: dict,
    order: dict,
    shipment: dict,
    refunds: list[dict],
    returns: list[dict],
    knowledge: list[dict],
    risk: str,
) -> dict:
    from src.agents.draft_agent import DraftAgent

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(
            DraftAgent().generate_summary(
                customer=customer,
                order=order,
                shipment=shipment,
                refunds=refunds,
                returns=returns,
                knowledge=knowledge,
                risk=risk,
            )
        )

    raise RuntimeError(
        "generate_order_support_summary cannot run inside an active event loop. "
        "Use DraftAgent.generate_summary directly from async code."
    )
