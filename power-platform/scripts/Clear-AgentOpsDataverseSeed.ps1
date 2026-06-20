[CmdletBinding()]
param(
    [string]$EnvPath = "mcp-server/.env"
)

$ErrorActionPreference = "Stop"
. "$PSScriptRoot/Dataverse.Common.ps1"

function Remove-AllRows {
    param(
        [hashtable]$Settings,
        [hashtable]$Headers,
        [string]$EntitySetName,
        [string]$PrimaryIdField
    )

    $rows = Invoke-DataverseGet -Settings $Settings -Path ("{0}?`$select={1}" -f $EntitySetName, $PrimaryIdField) -Headers $Headers
    foreach ($row in @($rows.value)) {
        if ($null -eq $row) {
            continue
        }

        $idValue = $row.$PrimaryIdField
        if ([string]::IsNullOrWhiteSpace($idValue)) {
            continue
        }

        Write-Host ("Deleting {0}({1})" -f $EntitySetName, $idValue)
        Invoke-DataverseDelete -Settings $Settings -Path ("{0}({1})" -f $EntitySetName, $idValue) -Headers $Headers
    }
}

function Remove-FilteredRows {
    param(
        [hashtable]$Settings,
        [hashtable]$Headers,
        [string]$EntitySetName,
        [string]$PrimaryIdField,
        [string]$SelectField,
        [string]$FilterQuery
    )

    $rows = Invoke-DataverseGet -Settings $Settings -Path ("{0}?`$select={1},{2}&`$filter={3}" -f $EntitySetName, $PrimaryIdField, $SelectField, $FilterQuery) -Headers $Headers
    foreach ($row in @($rows.value)) {
        if ($null -eq $row) {
            continue
        }

        $idValue = $row.$PrimaryIdField
        if ([string]::IsNullOrWhiteSpace($idValue)) {
            continue
        }

        Write-Host ("Deleting {0}({1})" -f $EntitySetName, $idValue)
        Invoke-DataverseDelete -Settings $Settings -Path ("{0}({1})" -f $EntitySetName, $idValue) -Headers $Headers
    }
}

$settings = Get-DataverseConnectionSettings -EnvPath $EnvPath
$token = Get-DataverseAccessToken -Settings $settings
$headers = Get-DataverseHeaders -AccessToken $token

Remove-AllRows -Settings $settings -Headers $headers -EntitySetName "cr_refunds" -PrimaryIdField "cr_refundid"
Remove-AllRows -Settings $settings -Headers $headers -EntitySetName "cr_returnrequests" -PrimaryIdField "cr_returnrequestid"
Remove-AllRows -Settings $settings -Headers $headers -EntitySetName "cr_shipments" -PrimaryIdField "cr_shipmentid"
Remove-AllRows -Settings $settings -Headers $headers -EntitySetName "cr_orderitems" -PrimaryIdField "cr_orderitemid"
Remove-AllRows -Settings $settings -Headers $headers -EntitySetName "cr_orders" -PrimaryIdField "cr_orderid"
Remove-AllRows -Settings $settings -Headers $headers -EntitySetName "cr_approvalrequests" -PrimaryIdField "cr_approvalrequestid"
Remove-AllRows -Settings $settings -Headers $headers -EntitySetName "cr_agentruns" -PrimaryIdField "cr_agentrunid"
Remove-FilteredRows -Settings $settings -Headers $headers -EntitySetName "contacts" -PrimaryIdField "contactid" -SelectField "emailaddress1" -FilterQuery "emailaddress1 eq 'john.smith@contoso.com' or emailaddress1 eq 'emma.clarke@fabrikam.com'"
Remove-FilteredRows -Settings $settings -Headers $headers -EntitySetName "accounts" -PrimaryIdField "accountid" -SelectField "name" -FilterQuery "name eq 'Contoso Ltd' or name eq 'Fabrikam Group'"

Write-Host ""
Write-Host "Custom AgentOps Dataverse seed data cleared."
