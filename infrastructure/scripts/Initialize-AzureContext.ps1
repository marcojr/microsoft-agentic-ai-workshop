[CmdletBinding()]
param(
    [string]$OutputPath = "infrastructure/config/azure-context.json"
)

$ErrorActionPreference = "Stop"
. "$PSScriptRoot/AzureContext.Common.ps1"

Require-Command -Name "az"

Write-Host ""
Write-Host "Azure context bootstrap"
Write-Host ""

$accountProbe = $null
try {
    $accountProbe = az account show --output json 2>$null | ConvertFrom-Json
}
catch {
    $accountProbe = $null
}

if (-not $accountProbe) {
    Write-Host "No active Azure session found. Opening 'az login'..."
    az login | Out-Null
}

$subscriptions = az account list --all --output json | ConvertFrom-Json
if (-not $subscriptions -or $subscriptions.Count -eq 0) {
    throw "No Azure subscriptions were returned by 'az account list'."
}

$enabledSubscriptions = @($subscriptions | Where-Object { $_.state -eq "Enabled" })
if (-not $enabledSubscriptions -or $enabledSubscriptions.Count -eq 0) {
    throw "No enabled Azure subscriptions were found."
}

Write-Host ""
Write-Host "Available subscriptions:"
for ($i = 0; $i -lt $enabledSubscriptions.Count; $i++) {
    $subscription = $enabledSubscriptions[$i]
    Write-Host ("[{0}] {1} ({2})" -f $i, $subscription.name, $subscription.id)
}

$selectionRaw = Read-Value -Prompt "Choose the subscription number" -Default "0"
$parsedSelection = 0
if (-not [int]::TryParse($selectionRaw, [ref]$parsedSelection)) {
    throw "Subscription selection must be a number."
}

$selection = $parsedSelection
if ($selection -lt 0 -or $selection -ge $enabledSubscriptions.Count) {
    throw "Subscription selection '$selection' is out of range."
}

$selectedSubscription = $enabledSubscriptions[$selection]
az account set --subscription $selectedSubscription.id

$workloadRoot = Read-Value -Prompt "Workload root / project root" -Default "agentops"
$environment = Read-Value -Prompt "Environment" -Default "dev"
$locationName = Read-Value -Prompt "Azure region" -Default "uksouth"
$locationShort = Get-LocationShortName -Location $locationName

$sequenceStartRaw = Read-Value -Prompt "Initial resource sequence number" -Default "1"
$sequenceStart = 0
if (-not [int]::TryParse($sequenceStartRaw, [ref]$sequenceStart)) {
    throw "Initial resource sequence number must be numeric."
}

$owner = Read-Value -Prompt "Owner tag" -Default ""
$costCenter = Read-Value -Prompt "Cost center tag" -Default ""

$defaultRecoveryResourceGroup = "rg-{0}-state" -f (Normalize-Slug -Value $workloadRoot -AllowHyphen)
$defaultRecoveryStorageAccount = (Get-RecoveryNames -Workload $workloadRoot -LocationShort $locationShort -StateSequence "001").storageAccount
$defaultRecoveryContainer = "environment-dumps"

$recoveryResourceGroup = Read-Value -Prompt "Persistent recovery resource group" -Default $defaultRecoveryResourceGroup
$recoveryStorageAccount = Read-Value -Prompt "Persistent recovery storage account" -Default $defaultRecoveryStorageAccount
$recoveryContainer = Read-Value -Prompt "Persistent recovery blob container" -Default $defaultRecoveryContainer

$context = Build-AzureContext `
    -Subscription $selectedSubscription `
    -WorkloadRoot $workloadRoot `
    -Environment $environment `
    -LocationName $locationName `
    -LocationShort $locationShort `
    -SequenceValue $sequenceStart `
    -SequencePadTo 3 `
    -Owner $owner `
    -CostCenter $costCenter `
    -RecoverySubscriptionId $selectedSubscription.id `
    -RecoverySubscriptionName $selectedSubscription.name `
    -RecoveryResourceGroup $recoveryResourceGroup `
    -RecoveryStorageAccount $recoveryStorageAccount `
    -RecoveryContainer $recoveryContainer

Save-AzureContext -Context $context -OutputPath $OutputPath

Write-Host ""
Write-Host "Saved Azure context to: $OutputPath"
Show-ResourceNames -Context $context
Write-Host ""
Write-Host ("Persistent recovery target: {0}/{1}/{2}" -f $context.recovery.resourceGroup, $context.recovery.storageAccount, $context.recovery.container)
