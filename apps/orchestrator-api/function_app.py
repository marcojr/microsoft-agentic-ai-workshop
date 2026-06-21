import json
from pathlib import Path

import azure.functions as func

app = func.FunctionApp()

from src.approval_console import decide_approval, list_pending_approvals
from src.webshop_order_support import handle_webshop_order_support


def _json_response(result: dict, status_code: int) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json",
        status_code=status_code,
    )


@app.route(
    route="agents/webshop/order-support",
    methods=["POST"],
    auth_level=func.AuthLevel.FUNCTION,
)
def webshop_order_support(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON"}),
            mimetype="application/json",
            status_code=400,
        )

    result, status_code = handle_webshop_order_support(body)
    return _json_response(result, status_code)


@app.route(
    route="approval-console",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS,
)
def approval_console(req: func.HttpRequest) -> func.HttpResponse:
    html_path = Path(__file__).resolve().parents[1] / "frontend-demo" / "approval-console.html"
    if not html_path.exists():
        return func.HttpResponse("Approval console not found.", status_code=404)

    return func.HttpResponse(
        html_path.read_text(encoding="utf-8"),
        mimetype="text/html",
        status_code=200,
    )


@app.route(
    route="approvals/pending",
    methods=["GET"],
    auth_level=func.AuthLevel.FUNCTION,
)
def approvals_pending(req: func.HttpRequest) -> func.HttpResponse:
    result, status_code = list_pending_approvals()
    return _json_response(result, status_code)


@app.route(
    route="approvals/decision",
    methods=["POST"],
    auth_level=func.AuthLevel.FUNCTION,
)
def approvals_decision(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON"}),
            mimetype="application/json",
            status_code=400,
        )

    result, status_code = decide_approval(body)
    return _json_response(result, status_code)


@app.route(
    route="agents/customer-case/summarise",
    methods=["POST"],
    auth_level=func.AuthLevel.FUNCTION,
)
def customer_case_summarise(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"error": "Not implemented yet"}),
        mimetype="application/json",
        status_code=501,
    )


@app.route(
    route="agent-runs/{runId?}",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS,
)
def agent_runs(req: func.HttpRequest) -> func.HttpResponse:
    run_id = req.route_params.get("runId")
    return func.HttpResponse(
        json.dumps({"message": "Not implemented yet", "runId": run_id}),
        mimetype="application/json",
        status_code=501,
    )
