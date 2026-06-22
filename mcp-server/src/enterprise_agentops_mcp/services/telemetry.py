import os

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor


_CONFIGURED = False
_PROVIDER = None


def init_telemetry() -> bool:
    """Configure OpenTelemetry so MCP operations can be inspected in Azure Monitor."""
    global _CONFIGURED, _PROVIDER

    # Step 1: keep telemetry initialization idempotent. Azure Functions may reuse
    # the same worker process across requests, so we only configure tracing once.
    if _CONFIGURED:
        return True

    # Step 2: Application Insights is optional for local development. When the
    # connection string is not present, the caller can still execute normally.
    connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if not connection_string:
        return False

    # Step 3: create the Azure Monitor exporter. This is the component that sends
    # OpenTelemetry spans to the Application Insights resource.
    exporter = AzureMonitorTraceExporter(connection_string=connection_string)

    # Step 4: identify this service in Azure Monitor. The service.name value is
    # useful later when filtering telemetry across Functions, MCP tools, or agents.
    _PROVIDER = TracerProvider(
        resource=Resource.create({"service.name": "enterprise-agentops-mcp"})
    )

    # Step 5: use a simple processor so demo spans are exported immediately.
    # This trades throughput for visibility, which is exactly what we want here.
    _PROVIDER.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(_PROVIDER)
    _CONFIGURED = True
    return True


def get_tracer():
    # Step 6: every caller asks for the same named tracer. If telemetry is not
    # configured, OpenTelemetry returns a no-op tracer and the code still runs.
    init_telemetry()
    return trace.get_tracer("enterprise-agentops-mcp")


def flush_telemetry() -> None:
    # Step 7: force pending spans out before the Function request ends. Without
    # this, short-lived executions can finish before telemetry reaches Azure.
    if _PROVIDER:
        _PROVIDER.force_flush()
