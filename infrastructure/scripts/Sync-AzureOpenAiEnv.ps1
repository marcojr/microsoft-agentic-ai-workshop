param(
    [string]$ContextPath = "infrastructure/config/azure-context.json",
    [string]$EnvPath = "mcp-server/.env",
    [string]$DeploymentName = "gpt-5-mini"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    throw "Azure CLI 'az' was not found on PATH."
}

if (-not (Test-Path $ContextPath)) {
    throw "Azure context file not found: $ContextPath"
}

if (-not (Test-Path $EnvPath)) {
    throw "Environment file not found: $EnvPath"
}

$context = Get-Content -LiteralPath $ContextPath -Raw | ConvertFrom-Json
$resourceGroup = $context.resources.resourceGroup
$accountName = $context.resources.azureOpenAi

if ([string]::IsNullOrWhiteSpace($resourceGroup)) {
    throw "Missing resources.resourceGroup in $ContextPath."
}

if ([string]::IsNullOrWhiteSpace($accountName)) {
    throw "Missing resources.azureOpenAi in $ContextPath."
}

$key = az cognitiveservices account keys list `
    --resource-group $resourceGroup `
    --name $accountName `
    --query key1 `
    --output tsv

if ([string]::IsNullOrWhiteSpace($key)) {
    throw "Azure OpenAI key1 was empty for account '$accountName'."
}

$endpoint = "https://$accountName.openai.azure.com/"

function Set-EnvValue {
    param(
        [string[]]$Lines,
        [string]$Name,
        [string]$Value
    )

    $found = $false
    $updated = $Lines | ForEach-Object {
        if ($_ -match "^$([regex]::Escape($Name))=") {
            $found = $true
            "$Name=$Value"
        }
        else {
            $_
        }
    }

    if (-not $found) {
        $updated += "$Name=$Value"
    }

    return $updated
}

$lines = Get-Content -LiteralPath $EnvPath
$lines = Set-EnvValue -Lines $lines -Name "AI_PRIMARY_PROVIDER" -Value "azure_openai"
$lines = Set-EnvValue -Lines $lines -Name "AI_PRIMARY_VENDOR" -Value "Azure OpenAI"
$lines = Set-EnvValue -Lines $lines -Name "AI_PRIMARY_MODEL" -Value "gpt-5-mini"
$lines = Set-EnvValue -Lines $lines -Name "AZURE_OPENAI_ENDPOINT" -Value $endpoint
$lines = Set-EnvValue -Lines $lines -Name "AZURE_OPENAI_API_KEY" -Value $key
$lines = Set-EnvValue -Lines $lines -Name "AZURE_OPENAI_DEPLOYMENT_NAME" -Value $DeploymentName

Set-Content -LiteralPath $EnvPath -Value $lines -Encoding utf8

Write-Host "Azure OpenAI env synced for account '$accountName' and deployment '$DeploymentName'. Secret value was not printed."

