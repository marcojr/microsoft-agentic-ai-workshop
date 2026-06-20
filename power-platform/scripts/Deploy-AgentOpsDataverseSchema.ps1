[CmdletBinding()]
param(
    [string]$SchemaPath = "power-platform/dataverse-schema/schema.v1.json",
    [string]$EnvPath = "mcp-server/.env",
    [string]$SolutionUniqueName = "",
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"
. "$PSScriptRoot/Dataverse.Common.ps1"

function New-LocalizedLabel {
    param([string]$Label)
    return @{
        LocalizedLabels = @(
            @{
                Label = $Label
                LanguageCode = 1033
            }
        )
    }
}

function New-RequiredLevel {
    return @{
        Value = "None"
    }
}

function New-PrimaryNameAttribute {
    param([object]$Attribute)
    return @{
        "@odata.type" = "Microsoft.Dynamics.CRM.StringAttributeMetadata"
        SchemaName = $Attribute.schemaName
        LogicalName = $Attribute.logicalName
        IsPrimaryName = $true
        DisplayName = (New-LocalizedLabel -Label $Attribute.displayName)
        RequiredLevel = (New-RequiredLevel)
        MaxLength = [int]$Attribute.maxLength
        FormatName = @{
            Value = "Text"
        }
    }
}

function New-AttributePayload {
    param([object]$Column)

    $base = @{
        SchemaName = $Column.schemaName
        LogicalName = $Column.logicalName
        DisplayName = (New-LocalizedLabel -Label $Column.displayName)
        RequiredLevel = (New-RequiredLevel)
    }

    switch ($Column.type) {
        "string" {
            $base["@odata.type"] = "Microsoft.Dynamics.CRM.StringAttributeMetadata"
            $base["MaxLength"] = [int]$Column.maxLength
            $base["FormatName"] = @{ Value = "Text" }
            return $base
        }
        "memo" {
            $base["@odata.type"] = "Microsoft.Dynamics.CRM.MemoAttributeMetadata"
            $base["MaxLength"] = [int]$Column.maxLength
            $base["Format"] = "TextArea"
            return $base
        }
        "integer" {
            $base["@odata.type"] = "Microsoft.Dynamics.CRM.IntegerAttributeMetadata"
            $base["MinValue"] = [int]$Column.minValue
            $base["MaxValue"] = [int]$Column.maxValue
            $base["Format"] = "None"
            return $base
        }
        "decimal" {
            $base["@odata.type"] = "Microsoft.Dynamics.CRM.DecimalAttributeMetadata"
            $base["MinValue"] = [decimal]$Column.minValue
            $base["MaxValue"] = [decimal]$Column.maxValue
            $base["Precision"] = [int]$Column.precision
            return $base
        }
        "money" {
            $base["@odata.type"] = "Microsoft.Dynamics.CRM.MoneyAttributeMetadata"
            $base["MinValue"] = [decimal]0
            $base["MaxValue"] = [decimal]1000000000
            $base["Precision"] = [int]$Column.precision
            return $base
        }
        "boolean" {
            $base["@odata.type"] = "Microsoft.Dynamics.CRM.BooleanAttributeMetadata"
            $base["OptionSet"] = @{
                TrueOption = @{
                    Label = (New-LocalizedLabel -Label "Yes")
                    Value = 1
                }
                FalseOption = @{
                    Label = (New-LocalizedLabel -Label "No")
                    Value = 0
                }
            }
            return $base
        }
        "datetime" {
            $base["@odata.type"] = "Microsoft.Dynamics.CRM.DateTimeAttributeMetadata"
            $base["Format"] = "DateAndTime"
            $base["DateTimeBehavior"] = @{
                Value = "UserLocal"
            }
            return $base
        }
        "date" {
            $base["@odata.type"] = "Microsoft.Dynamics.CRM.DateTimeAttributeMetadata"
            $base["Format"] = "DateOnly"
            $base["DateTimeBehavior"] = @{
                Value = "DateOnly"
            }
            return $base
        }
        default {
            throw "Unsupported column type '$($Column.type)' for '$($Column.logicalName)'."
        }
    }
}

if (-not (Test-Path -LiteralPath $SchemaPath)) {
    throw "Schema file not found: $SchemaPath"
}

$schema = Get-Content -LiteralPath $SchemaPath -Raw | ConvertFrom-Json
$settings = Get-DataverseConnectionSettings -EnvPath $EnvPath
$token = Get-DataverseAccessToken -Settings $settings
$headers = Get-DataverseHeaders -AccessToken $token -SolutionUniqueName $SolutionUniqueName

Write-Host ""
Write-Host ("Dataverse schema deploy from {0}" -f $SchemaPath)
Write-Host ("Target environment: {0}" -f $settings.Url)
Write-Host ""

foreach ($table in $schema.tables) {
    $entityExists = Test-DataverseEntityExists -Settings $settings -LogicalName $table.logicalName -Headers $headers
    if (-not $entityExists) {
        Write-Host ("Creating table {0}..." -f $table.logicalName)
        if (-not $WhatIf) {
            $entityPayload = @{
                "@odata.type" = "Microsoft.Dynamics.CRM.EntityMetadata"
                SchemaName = $table.schemaName
                LogicalName = $table.logicalName
                DisplayName = (New-LocalizedLabel -Label $table.displayName)
                DisplayCollectionName = (New-LocalizedLabel -Label $table.displayCollectionName)
                Description = (New-LocalizedLabel -Label $table.description)
                OwnershipType = "OrganizationOwned"
                HasActivities = $false
                HasNotes = $false
                IsActivity = $false
                Attributes = @(
                    (New-PrimaryNameAttribute -Attribute $table.primaryNameAttribute)
                )
            }
            Invoke-DataversePost -Settings $settings -Path "EntityDefinitions" -Body $entityPayload -Headers $headers | Out-Null
        }
    }
    else {
        Write-Host ("Table {0} already exists." -f $table.logicalName)
    }

    foreach ($column in $table.columns) {
        $attributeExists = Test-DataverseAttributeExists `
            -Settings $settings `
            -EntityLogicalName $table.logicalName `
            -AttributeLogicalName $column.logicalName `
            -Headers $headers

        if ($attributeExists) {
            Write-Host ("  Column {0} already exists." -f $column.logicalName)
            continue
        }

        Write-Host ("  Creating column {0} ({1})..." -f $column.logicalName, $column.type)
        if (-not $WhatIf) {
            $attributePayload = New-AttributePayload -Column $column
            Invoke-DataversePost `
                -Settings $settings `
                -Path ("EntityDefinitions(LogicalName='{0}')/Attributes" -f $table.logicalName) `
                -Body $attributePayload `
                -Headers $headers | Out-Null
        }
    }
}

Write-Host ""
Write-Host "Schema deploy completed."
