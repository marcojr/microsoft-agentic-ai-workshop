[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

function Read-EnvFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Env file not found: $Path"
    }

    $result = @{}
    foreach ($line in Get-Content -LiteralPath $Path) {
        $trimmed = $line.Trim()
        if (-not $trimmed -or $trimmed.StartsWith("#")) {
            continue
        }

        $separatorIndex = $trimmed.IndexOf("=")
        if ($separatorIndex -lt 1) {
            continue
        }

        $name = $trimmed.Substring(0, $separatorIndex).Trim()
        $value = $trimmed.Substring($separatorIndex + 1).Trim()
        $result[$name] = $value
    }

    return $result
}

function Get-DataverseConnectionSettings {
    param(
        [string]$EnvPath = "mcp-server/.env"
    )

    $envValues = Read-EnvFile -Path $EnvPath
    $required = @(
        "DATAVERSE_URL",
        "DATAVERSE_SP_CLIENT_ID",
        "DATAVERSE_SP_CLIENT_SECRET",
        "DATAVERSE_SP_TENANT_ID"
    )

    foreach ($name in $required) {
        if (-not $envValues.ContainsKey($name) -or [string]::IsNullOrWhiteSpace($envValues[$name])) {
            throw "Missing required Dataverse setting '$name' in $EnvPath"
        }
    }

    return @{
        Url = $envValues["DATAVERSE_URL"].TrimEnd("/")
        ClientId = $envValues["DATAVERSE_SP_CLIENT_ID"]
        ClientSecret = $envValues["DATAVERSE_SP_CLIENT_SECRET"]
        TenantId = $envValues["DATAVERSE_SP_TENANT_ID"]
    }
}

function Get-DataverseAccessToken {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Settings
    )

    $tokenResponse = Invoke-RestMethod `
        -Method Post `
        -Uri ("https://login.microsoftonline.com/{0}/oauth2/v2.0/token" -f $Settings.TenantId) `
        -ContentType "application/x-www-form-urlencoded" `
        -Body @{
            client_id = $Settings.ClientId
            client_secret = $Settings.ClientSecret
            scope = ("{0}/.default" -f $Settings.Url)
            grant_type = "client_credentials"
        }

    if (-not $tokenResponse.access_token) {
        throw "Failed to acquire Dataverse access token."
    }

    return $tokenResponse.access_token
}

function Get-DataverseHeaders {
    param(
        [Parameter(Mandatory = $true)]
        [string]$AccessToken,

        [string]$SolutionUniqueName
    )

    $headers = @{
        Authorization = "Bearer $AccessToken"
        Accept = "application/json"
        "OData-MaxVersion" = "4.0"
        "OData-Version" = "4.0"
        "Content-Type" = "application/json; charset=utf-8"
    }

    if ($SolutionUniqueName) {
        $headers["MSCRM.SolutionUniqueName"] = $SolutionUniqueName
    }

    return $headers
}

function Invoke-DataverseGet {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Settings,

        [Parameter(Mandatory = $true)]
        [string]$Path,

        [hashtable]$Headers = @{}
    )

    return Invoke-RestMethod -Method Get -Uri ("{0}/api/data/v9.2/{1}" -f $Settings.Url, $Path) -Headers $Headers
}

function Invoke-DataversePost {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Settings,

        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [object]$Body,

        [hashtable]$Headers = @{}
    )

    $jsonBody = $Body | ConvertTo-Json -Depth 20
    $attempt = 0
    $maxAttempts = 30

    while ($true) {
        try {
            return Invoke-RestMethod `
                -Method Post `
                -Uri ("{0}/api/data/v9.2/{1}" -f $Settings.Url, $Path) `
                -Headers $Headers `
                -Body $jsonBody
        }
        catch {
            $attempt += 1
            $message = $_.ErrorDetails.Message
            if ($message -match "Cannot start another \[EntityCustomization\]" -and $attempt -lt $maxAttempts) {
                Write-Host ("Dataverse customization lock detected for POST {0}. Waiting 10s before retry {1}/{2}..." -f $Path, $attempt, $maxAttempts)
                Start-Sleep -Seconds 10
                continue
            }
            throw
        }
    }
}

function Invoke-DataversePatch {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Settings,

        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [object]$Body,

        [hashtable]$Headers = @{}
    )

    $jsonBody = $Body | ConvertTo-Json -Depth 20
    $attempt = 0
    $maxAttempts = 30

    while ($true) {
        try {
            Invoke-RestMethod `
                -Method Patch `
                -Uri ("{0}/api/data/v9.2/{1}" -f $Settings.Url, $Path) `
                -Headers $Headers `
                -Body $jsonBody | Out-Null
            return
        }
        catch {
            $attempt += 1
            $message = $_.ErrorDetails.Message
            if ($message -match "Cannot start another \[EntityCustomization\]" -and $attempt -lt $maxAttempts) {
                Write-Host ("Dataverse customization lock detected for PATCH {0}. Waiting 10s before retry {1}/{2}..." -f $Path, $attempt, $maxAttempts)
                Start-Sleep -Seconds 10
                continue
            }
            throw
        }
    }
}

function Invoke-DataverseDelete {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Settings,

        [Parameter(Mandatory = $true)]
        [string]$Path,

        [hashtable]$Headers = @{}
    )

    Invoke-RestMethod `
        -Method Delete `
        -Uri ("{0}/api/data/v9.2/{1}" -f $Settings.Url, $Path) `
        -Headers $Headers | Out-Null
}

function Test-DataverseEntityExists {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Settings,

        [Parameter(Mandatory = $true)]
        [string]$LogicalName,

        [Parameter(Mandatory = $true)]
        [hashtable]$Headers
    )

    try {
        Invoke-DataverseGet -Settings $Settings -Path ("EntityDefinitions(LogicalName='{0}')?`$select=LogicalName,EntitySetName" -f $LogicalName) -Headers $Headers | Out-Null
        return $true
    }
    catch {
        if ($_.Exception.Response.StatusCode.value__ -eq 404) {
            return $false
        }
        if ($_.ErrorDetails.Message -match "does not exist") {
            return $false
        }
        throw
    }
}

function Test-DataverseAttributeExists {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Settings,

        [Parameter(Mandatory = $true)]
        [string]$EntityLogicalName,

        [Parameter(Mandatory = $true)]
        [string]$AttributeLogicalName,

        [Parameter(Mandatory = $true)]
        [hashtable]$Headers
    )

    try {
        Invoke-DataverseGet -Settings $Settings -Path ("EntityDefinitions(LogicalName='{0}')/Attributes(LogicalName='{1}')?`$select=LogicalName" -f $EntityLogicalName, $AttributeLogicalName) -Headers $Headers | Out-Null
        return $true
    }
    catch {
        if ($_.Exception.Response.StatusCode.value__ -eq 404) {
            return $false
        }
        if ($_.ErrorDetails.Message -match "does not exist") {
            return $false
        }
        throw
    }
}
