# Power Platform Custom Connectors

## AgentOps Approval Console

Import `agentops-approval-console.openapi.json` as a Power Apps custom connector.

The OpenAPI file is currently pointed at:

```text
func-agentops-dev-002.azurewebsites.net
```

If the Function App is recreated with a different name, update the OpenAPI `host` value before importing.

```text
"host": "your-function-app.azurewebsites.net"
```

For a deployed Function App, configure the connector's API key parameter as:

```text
code
```

and provide an Azure Functions host/function key when creating the Power Apps connection.

The connector exposes:

- `ListPendingApprovals`
- `SubmitApprovalDecision`

Local `localhost` testing is better done through the HTML smoke-test console at:

```text
http://localhost:7071/api/approval-console
```

Power Apps cloud connectors generally cannot call a developer machine's `localhost` directly.
