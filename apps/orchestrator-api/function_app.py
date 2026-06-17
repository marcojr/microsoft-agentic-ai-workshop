import azure.functions as func
import json

app = func.FunctionApp()

from src.webshop_order_support import handle_webshop_order_support


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
    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json",
        status_code=status_code,
    )


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
