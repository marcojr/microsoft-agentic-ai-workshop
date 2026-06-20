$ErrorActionPreference = "Stop"

function Require-Command {
    param([string]$Name)

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

function Read-Value {
    param(
        [string]$Prompt,
        [string]$Default = ""
    )

    $label = if ($Default) { "$Prompt [$Default]" } else { $Prompt }
    $value = Read-Host $label

    if ([string]::IsNullOrWhiteSpace($value)) {
        return $Default
    }

    return $value.Trim()
}

function Normalize-Slug {
    param(
        [string]$Value,
        [switch]$AllowHyphen
    )

    $normalized = $Value.Trim().ToLowerInvariant()
    if ($AllowHyphen) {
        $normalized = $normalized -replace "[^a-z0-9-]", ""
        $normalized = $normalized -replace "-{2,}", "-"
        $normalized = $normalized.Trim("-")
    }
    else {
        $normalized = $normalized -replace "[^a-z0-9]", ""
    }

    if ([string]::IsNullOrWhiteSpace($normalized)) {
        throw "Value '$Value' produced an empty normalized name."
    }

    return $normalized
}

function Get-LocationShortName {
    param([string]$Location)

    $map = @{
        "eastus" = "eus"
        "eastus2" = "eus2"
        "westus" = "wus"
        "westus2" = "wus2"
        "westus3" = "wus3"
        "centralus" = "cus"
        "northcentralus" = "ncus"
        "southcentralus" = "scus"
        "uksouth" = "uks"
        "ukwest" = "ukw"
        "westeurope" = "weu"
        "northeurope" = "neu"
        "swedencentral" = "swc"
        "germanywestcentral" = "gwc"
        "francecentral" = "frc"
    }

    $key = $Location.Trim().ToLowerInvariant()
    if ($map.ContainsKey($key)) {
        return $map[$key]
    }

    return Read-Value -Prompt "No short name mapping found for region '$Location'. Enter a short region code" -Default $key
}

function Format-Sequence {
    param(
        [int]$Value,
        [int]$PadTo = 3
    )

    if ($Value -lt 1) {
        throw "Sequence value must be greater than zero."
    }

    return $Value.ToString("D$PadTo")
}

function Get-ResourceNames {
    param(
        [string]$Workload,
        [string]$Environment,
        [string]$LocationShort,
        [string]$Instance
    )

    $safeWorkload = Normalize-Slug -Value $Workload -AllowHyphen
    $safeEnvironment = Normalize-Slug -Value $Environment -AllowHyphen
    $safeLocationShort = Normalize-Slug -Value $LocationShort -AllowHyphen
    $safeInstance = Normalize-Slug -Value $Instance

    $storageWorkload = Normalize-Slug -Value $Workload
    $storageEnvironment = Normalize-Slug -Value $Environment
    $storageLocationShort = Normalize-Slug -Value $LocationShort

    $storageAccount = "st{0}{1}{2}{3}" -f $storageWorkload, $storageEnvironment, $storageLocationShort, $safeInstance
    if ($storageAccount.Length -gt 24) {
        throw "Generated storage account name '$storageAccount' exceeds 24 characters. Shorten workload or region code."
    }

    return [ordered]@{
        resourceGroup = "rg-$safeWorkload-$safeEnvironment-$safeInstance"
        storageAccount = $storageAccount
        functionApp = "func-$safeWorkload-$safeEnvironment-$safeInstance"
        appInsights = "appi-$safeWorkload-$safeEnvironment-$safeLocationShort-$safeInstance"
        logAnalyticsWorkspace = "log-$safeWorkload-$safeEnvironment-$safeLocationShort-$safeInstance"
        keyVault = "kv-$safeWorkload-$safeEnvironment-$safeLocationShort-$safeInstance"
        serviceBusNamespace = "sbns-$safeWorkload-$safeEnvironment-$safeInstance"
        aiSearch = "srch-$safeWorkload-$safeEnvironment-$safeInstance"
        azureOpenAi = "oai-$safeWorkload-$safeEnvironment-$safeLocationShort-$safeInstance"
    }
}

function Get-RecoveryNames {
    param(
        [string]$Workload,
        [string]$LocationShort,
        [string]$StateSequence
    )

    $safeWorkload = Normalize-Slug -Value $Workload -AllowHyphen
    $storageWorkload = Normalize-Slug -Value $Workload
    $storageLocationShort = Normalize-Slug -Value $LocationShort
    $safeStateSequence = Normalize-Slug -Value $StateSequence

    $storageAccount = "st{0}state{1}{2}" -f $storageWorkload, $storageLocationShort, $safeStateSequence
    if ($storageAccount.Length -gt 24) {
        throw "Generated recovery storage account name '$storageAccount' exceeds 24 characters. Shorten workload or region code."
    }

    return [ordered]@{
        resourceGroup = "rg-$safeWorkload-state"
        storageAccount = $storageAccount
        container = "environment-dumps"
    }
}

function Build-AzureContext {
    param(
        [pscustomobject]$Subscription,
        [string]$WorkloadRoot,
        [string]$Environment,
        [string]$LocationName,
        [string]$LocationShort,
        [int]$SequenceValue,
        [int]$SequencePadTo,
        [string]$Owner,
        [string]$CostCenter,
        [string]$RecoverySubscriptionId,
        [string]$RecoverySubscriptionName,
        [string]$RecoveryResourceGroup,
        [string]$RecoveryStorageAccount,
        [string]$RecoveryContainer
    )

    $sequenceCurrent = Format-Sequence -Value $SequenceValue -PadTo $SequencePadTo
    $sequenceNext = Format-Sequence -Value ($SequenceValue + 1) -PadTo $SequencePadTo

    $resourceNames = Get-ResourceNames -Workload $WorkloadRoot -Environment $Environment -LocationShort $LocationShort -Instance $sequenceCurrent

    $defaultRecoveryNames = Get-RecoveryNames -Workload $WorkloadRoot -LocationShort $LocationShort -StateSequence $sequenceCurrent

    $resolvedRecovery = if ($RecoveryResourceGroup -or $RecoveryStorageAccount -or $RecoveryContainer) {
        [ordered]@{
            resourceGroup = if ($RecoveryResourceGroup) { Normalize-Slug -Value $RecoveryResourceGroup -AllowHyphen } else { $defaultRecoveryNames.resourceGroup }
            storageAccount = if ($RecoveryStorageAccount) { Normalize-Slug -Value $RecoveryStorageAccount } else { $defaultRecoveryNames.storageAccount }
            container = if ($RecoveryContainer) { Normalize-Slug -Value $RecoveryContainer -AllowHyphen } else { "environment-dumps" }
        }
    }
    else {
        $defaultRecoveryNames
    }

    return [ordered]@{
        subscription = [ordered]@{
            id = $Subscription.id
            name = $Subscription.name
        }
        workload = [ordered]@{
            root = (Normalize-Slug -Value $WorkloadRoot -AllowHyphen)
            description = ""
        }
        environment = (Normalize-Slug -Value $Environment -AllowHyphen)
        location = [ordered]@{
            name = $LocationName.Trim().ToLowerInvariant()
            short = (Normalize-Slug -Value $LocationShort -AllowHyphen)
        }
        sequence = [ordered]@{
            current = $sequenceCurrent
            next = $sequenceNext
            padTo = $SequencePadTo
            incrementOnDecommission = $true
        }
        lifecycle = [ordered]@{
            environmentMode = "ephemeral-study"
            destroyWholeResourceGroup = $true
            restoreFromRecoveryOnProvision = $true
            exportStateBeforeDestroy = $true
        }
        naming = [ordered]@{
            standard = "microsoft-caf"
            sourceUrls = @(
                "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming",
                "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations",
                "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-name-rules"
            )
        }
        tags = [ordered]@{
            workload = (Normalize-Slug -Value $WorkloadRoot -AllowHyphen)
            environment = (Normalize-Slug -Value $Environment -AllowHyphen)
            owner = $Owner
            costCenter = $CostCenter
            managedBy = "pulumi"
            source = "bootstrap-script"
        }
        recovery = [ordered]@{
            enabled = $true
            subscription = [ordered]@{
                id = if ($RecoverySubscriptionId) { $RecoverySubscriptionId } else { $Subscription.id }
                name = if ($RecoverySubscriptionName) { $RecoverySubscriptionName } else { $Subscription.name }
            }
            resourceGroup = $resolvedRecovery.resourceGroup
            storageAccount = $resolvedRecovery.storageAccount
            container = $resolvedRecovery.container
            pathPrefix = "{0}/{1}" -f (Normalize-Slug -Value $WorkloadRoot -AllowHyphen), (Normalize-Slug -Value $Environment -AllowHyphen)
        }
        bootstrapData = [ordered]@{
            ingestOnProvision = $true
            localSeedPaths = @(
                "data/sample-documents",
                "data/sample-dataverse-records"
            )
            recoveryBlobFolders = @(
                "dataverse-dumps",
                "blob-dumps",
                "knowledge-files"
            )
        }
        resources = $resourceNames
    }
}

function Save-AzureContext {
    param(
        $Context,
        [string]$OutputPath
    )

    $targetDirectory = Split-Path -Path $OutputPath -Parent
    if (-not (Test-Path $targetDirectory)) {
        New-Item -Path $targetDirectory -ItemType Directory -Force | Out-Null
    }

    $Context | ConvertTo-Json -Depth 10 | Set-Content -Path $OutputPath -Encoding utf8
}

function Show-ResourceNames {
    param($Context)

    Write-Host ""
    Write-Host "Generated resource names:"
    $Context.resources.GetEnumerator() | ForEach-Object {
        Write-Host ("- {0}: {1}" -f $_.Key, $_.Value)
    }
}
