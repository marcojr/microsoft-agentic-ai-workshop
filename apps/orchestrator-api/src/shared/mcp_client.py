import os
import sys
from pathlib import Path


def _ensure_import_paths() -> None:
    root = Path(__file__).resolve().parents[4]
    mcp_server_root = root / "mcp-server"
    mcp_server_src = Path(
        os.getenv("MCP_SERVER_SRC_PATH", mcp_server_root / "src")
    ).resolve()
    path_str = str(mcp_server_src)
    if mcp_server_src.exists() and path_str not in sys.path:
        sys.path.insert(0, path_str)


class MCPClient:
    def __init__(self) -> None:
        _ensure_import_paths()

    def call(self, tool_name: str, params: dict) -> dict:
        from enterprise_agentops_mcp.tools.accounts import get_account_by_name
        from enterprise_agentops_mcp.tools.approvals import (
            create_approval_request,
            create_follow_up_task,
        )
        from enterprise_agentops_mcp.tools.cases import get_case_details, get_open_cases
        from enterprise_agentops_mcp.tools.cost import calculate_agent_run_cost
        from enterprise_agentops_mcp.tools.customers import get_customer_by_email
        from enterprise_agentops_mcp.tools.evaluation import evaluate_response
        from enterprise_agentops_mcp.tools.knowledge import search_knowledge_articles
        from enterprise_agentops_mcp.tools.observability import log_agent_run
        from enterprise_agentops_mcp.tools.orders import (
            get_latest_order,
            get_order_details,
            get_order_items,
        )
        from enterprise_agentops_mcp.tools.returns import (
            get_refunds_for_order,
            get_returns_for_order,
        )
        from enterprise_agentops_mcp.tools.shipments import get_shipment_status

        tool_map = {
            "calculate_agent_run_cost": calculate_agent_run_cost,
            "create_approval_request": create_approval_request,
            "create_follow_up_task": create_follow_up_task,
            "evaluate_response": evaluate_response,
            "get_account_by_name": get_account_by_name,
            "get_case_details": get_case_details,
            "get_customer_by_email": get_customer_by_email,
            "get_latest_order": get_latest_order,
            "get_open_cases": get_open_cases,
            "get_order_details": get_order_details,
            "get_order_items": get_order_items,
            "get_refunds_for_order": get_refunds_for_order,
            "get_returns_for_order": get_returns_for_order,
            "get_shipment_status": get_shipment_status,
            "log_agent_run": log_agent_run,
            "search_knowledge_articles": search_knowledge_articles,
        }
        fn = tool_map.get(tool_name)
        if fn is None:
            return {"error": f"Unknown tool: {tool_name}"}
        return fn(**params)
