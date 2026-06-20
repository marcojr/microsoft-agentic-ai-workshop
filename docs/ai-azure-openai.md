# Azure OpenAI Integration Guide

Azure OpenAI is the primary enterprise LLM provider for this Microsoft Agentic AI case.

Runtime path:

```text
Azure OpenAI -> primary enterprise provider
Gemini -> secondary comparison provider
Direct OpenAI -> not active in this case
Anthropic -> not active
```

## Environment

Use:

```env
AI_PRIMARY_PROVIDER=azure_openai
AI_PRIMARY_VENDOR=Azure OpenAI
AI_PRIMARY_MODEL=gpt-5-mini

AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5-mini
```

Important:

- Azure OpenAI calls use the deployment name, not only the underlying model name.
- GPT-5 deployments require an explicit model version in infrastructure.
- The current deployment uses model `gpt-5-mini`, version `2025-08-07`, SKU `GlobalStandard`.
- GPT-5 chat completions use `max_completion_tokens`, not `max_tokens`.
- This repo keeps Azure OpenAI values in `AZURE_OPENAI_*` variables to avoid confusion with direct OpenAI API keys.

Official sources:

- https://learn.microsoft.com/en-us/azure/foundry-classic/openai/how-to/create-resource
- https://learn.microsoft.com/en-us/azure/foundry-classic/openai/how-to/switching-endpoints
- https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle

## Infrastructure

Azure OpenAI is provisioned by Pulumi as part of the study environment:

- account: `resources.azureOpenAi` from `infrastructure/config/azure-context.json`
- model deployment: `gpt-5-mini`
- model name: `gpt-5-mini`
- model version: `2025-08-07`
- deployment SKU: `GlobalStandard`
- Key Vault secrets:
  - `AZURE-OPENAI-ENDPOINT`
  - `AZURE-OPENAI-API-KEY`
  - `AZURE-OPENAI-DEPLOYMENT-NAME`

After `pulumi up`, copy those values into the local ignored `.env` for local MCP/orchestrator runs.

Shortcut:

```powershell
powershell -ExecutionPolicy Bypass -File infrastructure/scripts/Sync-AzureOpenAiEnv.ps1
```

The script reads `infrastructure/config/azure-context.json`, pulls the Azure OpenAI key with Azure CLI, and updates `mcp-server/.env` without printing the secret.

## Other Large Models On Azure

There is no separate product named "Azure Anthropic" in the same way there is "Azure OpenAI".

Anthropic Claude and other large models are consumed through Microsoft Foundry model catalog:

- Foundry Models sold by Azure
- Foundry Models from partners and community
- serverless or managed deployment options, depending on the model/provider

Examples include Anthropic Claude, Meta Llama, Mistral, DeepSeek, Cohere, Grok, Microsoft Phi, and others.

Official sources:

- https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview
- https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-from-partners
- https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-claude

## Current Status

The project is configured for Azure OpenAI as the primary provider.

The next implementation step is to replace the handcrafted summary in the orchestrator with a real Azure OpenAI call.

