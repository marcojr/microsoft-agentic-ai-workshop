from fastmcp import FastMCP

mcp = FastMCP("enterprise-agentops-mcp-server")

from enterprise_agentops_mcp.tools.accounts import router as accounts_router
from enterprise_agentops_mcp.tools.approvals import router as approvals_router
from enterprise_agentops_mcp.tools.cases import router as cases_router
from enterprise_agentops_mcp.tools.cost import router as cost_router
from enterprise_agentops_mcp.tools.customers import router as customers_router
from enterprise_agentops_mcp.tools.evaluation import router as evaluation_router
from enterprise_agentops_mcp.tools.knowledge import router as knowledge_router
from enterprise_agentops_mcp.tools.observability import router as observability_router
from enterprise_agentops_mcp.tools.orders import router as orders_router
from enterprise_agentops_mcp.tools.returns import router as returns_router
from enterprise_agentops_mcp.tools.shipments import router as shipments_router

mcp.mount(accounts_router)
mcp.mount(approvals_router)
mcp.mount(cases_router)
mcp.mount(cost_router)
mcp.mount(customers_router)
mcp.mount(evaluation_router)
mcp.mount(knowledge_router)
mcp.mount(observability_router)
mcp.mount(orders_router)
mcp.mount(returns_router)
mcp.mount(shipments_router)


if __name__ == "__main__":
    mcp.run()
