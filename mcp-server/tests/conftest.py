from enterprise_agentops_mcp import config
from enterprise_agentops_mcp.tools import (
    accounts,
    approvals,
    cases,
    customers,
    knowledge,
    observability,
    orders,
    returns,
    shipments,
)


def pytest_runtest_setup() -> None:
    config.DATA_MODE = "mock"

    for module in (
        accounts,
        approvals,
        cases,
        customers,
        knowledge,
        observability,
        orders,
        returns,
        shipments,
    ):
        module.DATA_MODE = "mock"
