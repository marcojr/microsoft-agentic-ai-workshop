[CmdletBinding()]
param(
    [string]$EnvPath = ""
)

$ErrorActionPreference = "Stop"
. "$PSScriptRoot/Dataverse.Common.ps1"

function Invoke-DataverseGetValue {
    param(
        [hashtable]$Settings,
        [string]$Path,
        [hashtable]$Headers
    )

    $response = Invoke-DataverseGet -Settings $Settings -Path $Path -Headers $Headers
    if ($null -eq $response.value) {
        return @()
    }
    return ,$response.value
}

function Escape-ODataString {
    param([string]$Value)
    return $Value.Replace("'", "''")
}

function Upsert-Row {
    param(
        [hashtable]$Settings,
        [hashtable]$Headers,
        [string]$EntitySetName,
        [string]$KeyField,
        [string]$KeyValue,
        [string]$PrimaryIdField,
        [hashtable]$Payload
    )

    $query = "{0}?`$select={1},{2}&`$filter={1} eq '{3}'&`$top=1" -f $EntitySetName, $KeyField, $PrimaryIdField, (Escape-ODataString -Value $KeyValue)
    $existing = Invoke-DataverseGetValue -Settings $Settings -Path $query -Headers $Headers

    if ($existing.Count -gt 0) {
        $idValue = $existing[0].$PrimaryIdField
        Write-Host ("Updating {0} row where {1}={2}" -f $EntitySetName, $KeyField, $KeyValue)
        Invoke-DataversePatch -Settings $Settings -Path ("{0}({1})" -f $EntitySetName, $idValue) -Body $Payload -Headers $Headers
        return
    }

    Write-Host ("Creating {0} row where {1}={2}" -f $EntitySetName, $KeyField, $KeyValue)
    Invoke-DataversePost -Settings $Settings -Path $EntitySetName -Body $Payload -Headers $Headers | Out-Null
}

$settings = Get-DataverseConnectionSettings -EnvPath $EnvPath
$token = Get-DataverseAccessToken -Settings $settings
$headers = Get-DataverseHeaders -AccessToken $token

$accounts = Get-Content "mcp-server/src/enterprise_agentops_mcp/data/accounts.json" -Raw | ConvertFrom-Json
$contacts = Get-Content "mcp-server/src/enterprise_agentops_mcp/data/contacts.json" -Raw | ConvertFrom-Json
$orders = Get-Content "mcp-server/src/enterprise_agentops_mcp/data/orders.json" -Raw | ConvertFrom-Json
$orderItems = Get-Content "mcp-server/src/enterprise_agentops_mcp/data/order_items.json" -Raw | ConvertFrom-Json
$shipments = Get-Content "mcp-server/src/enterprise_agentops_mcp/data/shipments.json" -Raw | ConvertFrom-Json
$returns = Get-Content "mcp-server/src/enterprise_agentops_mcp/data/returns.json" -Raw | ConvertFrom-Json
$refunds = Get-Content "mcp-server/src/enterprise_agentops_mcp/data/refunds.json" -Raw | ConvertFrom-Json

$accountIdMap = @{}
$contactIdMap = @{}

foreach ($account in $accounts) {
    $query = "accounts?`$select=accountid,name&`$filter=name eq '{0}'&`$top=1" -f (Escape-ODataString -Value $account.name)
    $existing = Invoke-DataverseGetValue -Settings $settings -Path $query -Headers $headers

    if ($existing.Count -gt 0) {
        $accountGuid = $existing[0].accountid
        Write-Host ("Updating account {0}" -f $account.name)
        Invoke-DataversePatch -Settings $settings -Path ("accounts({0})" -f $accountGuid) -Body @{
            name = $account.name
            address1_line1 = $account.address1
            address1_postalcode = $account.postcode
        } -Headers $headers
    }
    else {
        Write-Host ("Creating account {0}" -f $account.name)
        Invoke-DataversePost -Settings $settings -Path "accounts" -Body @{
            name = $account.name
            address1_line1 = $account.address1
            address1_postalcode = $account.postcode
        } -Headers $headers | Out-Null

        $created = Invoke-DataverseGetValue -Settings $settings -Path $query -Headers $headers
        if ($created.Count -eq 0) {
            throw "Failed to create account '$($account.name)'."
        }
        $accountGuid = $created[0].accountid
    }

    $accountIdMap[$account.accountId] = $accountGuid
}

foreach ($contact in $contacts) {
    $query = "contacts?`$select=contactid,emailaddress1&`$filter=emailaddress1 eq '{0}'&`$top=1" -f (Escape-ODataString -Value $contact.email)
    $existing = Invoke-DataverseGetValue -Settings $settings -Path $query -Headers $headers
    $payload = @{
        firstname = ($contact.fullName -split " ")[0]
        lastname = (($contact.fullName -split " ", 2)[1])
        jobtitle = $contact.role
        telephone1 = $contact.phone
        emailaddress1 = $contact.email
        address1_line1 = $contact.deliveryAddress
        address1_postalcode = $contact.deliveryPostcode
        "parentcustomerid_account@odata.bind" = "/accounts($($accountIdMap[$contact.accountId]))"
    }

    if ($existing.Count -gt 0) {
        Write-Host ("Updating contact {0}" -f $contact.email)
        Invoke-DataversePatch -Settings $settings -Path ("contacts({0})" -f $existing[0].contactid) -Body $payload -Headers $headers
        $contactGuid = $existing[0].contactid
    }
    else {
        Write-Host ("Creating contact {0}" -f $contact.email)
        Invoke-DataversePost -Settings $settings -Path "contacts" -Body $payload -Headers $headers | Out-Null

        $created = Invoke-DataverseGetValue -Settings $settings -Path $query -Headers $headers
        if ($created.Count -eq 0) {
            throw "Failed to create contact '$($contact.email)'."
        }
        $contactGuid = $created[0].contactid
    }

    $contactIdMap[$contact.contactId] = $contactGuid
}

foreach ($order in $orders) {
    Upsert-Row -Settings $settings -Headers $headers -EntitySetName "cr_orders" -KeyField "cr_orderkey" -KeyValue $order.orderId -PrimaryIdField "cr_orderid" -Payload @{
        cr_orderkey = $order.orderId
        cr_ordernumber = $order.orderNumber
        cr_accountid = $accountIdMap[$order.accountId]
        cr_contactid = $contactIdMap[$order.contactId]
        cr_orderdate = $order.orderDate
        cr_status = $order.status
        cr_totalamount = $order.totalAmount
        cr_paymentstatus = $order.paymentStatus
        cr_deliverystatus = $order.deliveryStatus
        cr_shipmentkeyref = $order.shipmentId
        cr_risklevel = $order.riskLevel
        cr_deliveryaddress = $order.deliveryAddress
        cr_deliverypostcode = $order.deliveryPostcode
    }
}

foreach ($item in $orderItems) {
    Upsert-Row -Settings $settings -Headers $headers -EntitySetName "cr_orderitems" -KeyField "cr_orderitemkey" -KeyValue $item.orderItemId -PrimaryIdField "cr_orderitemid" -Payload @{
        cr_orderitemkey = $item.orderItemId
        cr_orderkeyref = $item.orderId
        cr_productname = $item.productName
        cr_sku = $item.sku
        cr_quantity = $item.quantity
        cr_unitprice = $item.unitPrice
        cr_totalprice = $item.totalPrice
    }
}

foreach ($shipment in $shipments) {
    Upsert-Row -Settings $settings -Headers $headers -EntitySetName "cr_shipments" -KeyField "cr_shipmentkey" -KeyValue $shipment.shipmentId -PrimaryIdField "cr_shipmentid" -Payload @{
        cr_shipmentkey = $shipment.shipmentId
        cr_orderkeyref = $shipment.orderId
        cr_carrier = $shipment.carrier
        cr_trackingnumber = $shipment.trackingNumber
        cr_status = $shipment.status
        cr_estimateddeliverydate = $shipment.estimatedDeliveryDate
        cr_delivereddate = $shipment.deliveredDate
        cr_delayreason = $shipment.delayReason
        cr_originpostcode = $shipment.originPostcode
        cr_destinationpostcode = $shipment.destinationPostcode
        cr_routedistancekm = $shipment.routeDistanceKm
    }
}

foreach ($returnRequest in $returns) {
    Upsert-Row -Settings $settings -Headers $headers -EntitySetName "cr_returnrequests" -KeyField "cr_returnkey" -KeyValue $returnRequest.returnId -PrimaryIdField "cr_returnrequestid" -Payload @{
        cr_returnkey = $returnRequest.returnId
        cr_orderkeyref = $returnRequest.orderId
        cr_orderitemkeyref = $returnRequest.orderItemId
        cr_reason = $returnRequest.reason
        cr_status = $returnRequest.status
        cr_requesteddate = $returnRequest.requestedDate
        cr_refundrequired = $returnRequest.refundRequired
    }
}

foreach ($refund in $refunds) {
    Upsert-Row -Settings $settings -Headers $headers -EntitySetName "cr_refunds" -KeyField "cr_refundkey" -KeyValue $refund.refundId -PrimaryIdField "cr_refundid" -Payload @{
        cr_refundkey = $refund.refundId
        cr_orderkeyref = $refund.orderId
        cr_returnkeyref = $refund.returnId
        cr_amount = $refund.amount
        cr_status = $refund.status
        cr_reason = $refund.reason
        cr_requiresapproval = $refund.requiresApproval
        cr_approvedby = $refund.approvedBy
    }
}

Write-Host ""
Write-Host "Sample Dataverse seed completed."
