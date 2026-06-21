# Power Platform Custom Connectors

## AgentOps Approval Console

Import `agentops-approval-console.openapi.json` as a Power Apps custom connector.

Before importing, replace:

```text
REPLACE_WITH_FUNCTION_HOST
```

with the deployed Azure Function host, for example:

```text
func-agentops-dev-001.azurewebsites.net
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
