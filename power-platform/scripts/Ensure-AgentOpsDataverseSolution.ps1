[CmdletBinding()]
param(
    [string]$EnvPath = "",
    [string]$PublisherUniqueName = "agentops_workshop_publisher",
    [string]$PublisherFriendlyName = "AgentOps Workshop Publisher",
    [string]$CustomizationPrefix = "agop",
    [int]$CustomizationOptionValuePrefix = 91500,
    [string]$SolutionUniqueName = "agentops_workshop",
    [string]$SolutionFriendlyName = "AgentOps Workshop",
    [string]$SolutionVersion = "1.0.0.0"
)

$ErrorActionPreference = "Stop"
. "$PSScriptRoot/Dataverse.Common.ps1"

function Escape-ODataString {
    param([Parameter(Mandatory = $true)][string]$Value)
    return $Value.Replace("'", "''")
}

function Get-SingleValue {
    param([object]$Response)
    if ($Response.value -and $Response.value.Count -gt 0) {
        return $Response.value[0]
    }
    return $null
}

function Get-Publisher {
    param(
        [hashtable]$Settings,
        [hashtable]$Headers,
        [string]$UniqueName
    )

    $escaped = Escape-ODataString -Value $UniqueName
    return Get-SingleValue -Response (Invoke-DataverseGet `
        -Settings $Settings `
        -Headers $Headers `
        -Path ("publishers?`$select=publisherid,uniquename,friendlyname&`$filter=uniquename eq '{0}'" -f $escaped))
}

function Get-Solution {
    param(
        [hashtable]$Settings,
        [hashtable]$Headers,
        [string]$UniqueName
    )

    $escaped = Escape-ODataString -Value $UniqueName
    return Get-SingleValue -Response (Invoke-DataverseGet `
        -Settings $Settings `
        -Headers $Headers `
        -Path ("solutions?`$select=solutionid,uniquename,friendlyname&`$filter=uniquename eq '{0}'" -f $escaped))
}

function Get-EntityMetadataId {
    param(
        [hashtable]$Settings,
        [hashtable]$Headers,
        [string]$LogicalName
    )

    $entity = Invoke-DataverseGet `
        -Settings $Settings `
        -Headers $Headers `
        -Path ("EntityDefinitions(LogicalName='{0}')?`$select=MetadataId" -f $LogicalName)

    if (-not $entity.MetadataId) {
        throw "Could not find MetadataId for table '$LogicalName'."
    }

    return $entity.MetadataId
}

function Add-TableToSolution {
    param(
        [hashtable]$Settings,
        [hashtable]$Headers,
        [string]$SolutionUniqueName,
        [string]$TableLogicalName
    )

    $metadataId = Get-EntityMetadataId -Settings $Settings -Headers $Headers -LogicalName $TableLogicalName
    Write-Host ("Adding table {0} to solution {1}..." -f $TableLogicalName, $SolutionUniqueName)

    Invoke-DataversePost `
        -Settings $Settings `
        -Headers $Headers `
        -Path "AddSolutionComponent" `
        -Body @{
            ComponentId = $metadataId
            ComponentType = 1
            SolutionUniqueName = $SolutionUniqueName
            AddRequiredComponents = $true
        } | Out-Null
}

$settings = Get-DataverseConnectionSettings -EnvPath $EnvPath
$token = Get-DataverseAccessToken -Settings $settings
$headers = Get-DataverseHeaders -AccessToken $token

Write-Host ""
Write-Host ("Ensuring Dataverse solution in {0}" -f $settings.Url)

$publisher = Get-Publisher -Settings $settings -Headers $headers -UniqueName $PublisherUniqueName
if (-not $publisher) {
    Write-Host ("Creating publisher {0}..." -f $PublisherUniqueName)
    Invoke-DataversePost `
        -Settings $settings `
        -Headers $headers `
        -Path "publishers" `
        -Body @{
            uniquename = $PublisherUniqueName
            friendlyname = $PublisherFriendlyName
            customizationprefix = $CustomizationPrefix
            customizationoptionvalueprefix = $CustomizationOptionValuePrefix
        } | Out-Null
    $publisher = Get-Publisher -Settings $settings -Headers $headers -UniqueName $PublisherUniqueName
}
else {
    Write-Host ("Publisher {0} already exists." -f $PublisherUniqueName)
}

if (-not $publisher.publisherid) {
    throw "Publisher '$PublisherUniqueName' was not created or found."
}

$solution = Get-Solution -Settings $settings -Headers $headers -UniqueName $SolutionUniqueName
if (-not $solution) {
    Write-Host ("Creating solution {0}..." -f $SolutionUniqueName)
    Invoke-DataversePost `
        -Settings $settings `
        -Headers $headers `
        -Path "solutions" `
        -Body @{
            uniquename = $SolutionUniqueName
            friendlyname = $SolutionFriendlyName
            version = $SolutionVersion
            "publisherid@odata.bind" = ("/publishers({0})" -f $publisher.publisherid)
        } | Out-Null
}
else {
    Write-Host ("Solution {0} already exists." -f $SolutionUniqueName)
}

$tables = @(
    "cr_order",
    "cr_orderitem",
    "cr_shipment",
    "cr_returnrequest",
    "cr_refund",
    "cr_approvalrequest",
    "cr_agentrun"
)

foreach ($table in $tables) {
    Add-TableToSolution `
        -Settings $settings `
        -Headers $headers `
        -SolutionUniqueName $SolutionUniqueName `
        -TableLogicalName $table
}

Write-Host ""
Write-Host ("Dataverse solution is ready: {0}" -f $SolutionUniqueName)
