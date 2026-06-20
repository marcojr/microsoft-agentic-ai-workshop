[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$DataverseTenantId
)

$ErrorActionPreference = "Stop"

function Require-Command {
    param([Parameter(Mandatory = $true)][string]$Name)

    if (-not (Get-Command -Name $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

Require-Command -Name "az"

$azureAccount = az account show --output json | ConvertFrom-Json
if (-not $azureAccount) {
    throw "No active Azure CLI session found."
}

$azureTenantId = [string]$azureAccount.tenantId
$subscriptionName = [string]$azureAccount.name
$subscriptionId = [string]$azureAccount.id

Write-Host ""
Write-Host "Tenant alignment check"
Write-Host ("Azure subscription : {0} ({1})" -f $subscriptionName, $subscriptionId)
Write-Host ("Azure tenant       : {0}" -f $azureTenantId)
Write-Host ("Dataverse tenant   : {0}" -f $DataverseTenantId)
Write-Host ""

if ($azureTenantId -ne $DataverseTenantId) {
    throw ("Tenant mismatch. Pulumi is creating identities in Azure tenant '{0}', but Dataverse expects tenant '{1}'. A single Pulumi-owned Dataverse identity is not possible until both sides target the same Entra tenant." -f $azureTenantId, $DataverseTenantId)
}

Write-Host "Tenant alignment OK. Pulumi and Dataverse are targeting the same Entra tenant."
