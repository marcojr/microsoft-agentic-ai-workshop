[CmdletBinding()]
param(
    [string]$ContextPath = "infrastructure/config/azure-context.json"
)

$ErrorActionPreference = "Stop"
. "$PSScriptRoot/AzureContext.Common.ps1"

Require-Command -Name "az"

if (-not (Test-Path $ContextPath)) {
    throw "Azure context file not found: $ContextPath"
}

$context = Get-Content $ContextPath -Raw | ConvertFrom-Json
$resourceGroupName = $context.resources.resourceGroup

if ([string]::IsNullOrWhiteSpace($resourceGroupName)) {
    throw "The Azure context file does not contain resources.resourceGroup."
}

Write-Host ""
Write-Host ("Deleting resource group: {0}" -f $resourceGroupName)
az group delete --name $resourceGroupName --yes

$nextSequenceValue = [int]$context.sequence.next
$padTo = [int]$context.sequence.padTo

$updatedContext = Build-AzureContext `
    -Subscription ([pscustomobject]@{
        id = $context.subscription.id
        name = $context.subscription.name
    }) `
    -WorkloadRoot $context.workload.root `
    -Environment $context.environment `
    -LocationName $context.location.name `
    -LocationShort $context.location.short `
    -SequenceValue $nextSequenceValue `
    -SequencePadTo $padTo `
    -Owner $context.tags.owner `
    -CostCenter $context.tags.costCenter `
    -RecoverySubscriptionId $context.recovery.subscription.id `
    -RecoverySubscriptionName $context.recovery.subscription.name `
    -RecoveryResourceGroup $context.recovery.resourceGroup `
    -RecoveryStorageAccount $context.recovery.storageAccount `
    -RecoveryContainer $context.recovery.container

Save-AzureContext -Context $updatedContext -OutputPath $ContextPath

Write-Host ""
Write-Host ("Deleted resource group '{0}'." -f $resourceGroupName)
Write-Host ("Sequence advanced from {0} to {1}." -f $context.sequence.current, $updatedContext.sequence.current)
Show-ResourceNames -Context $updatedContext
