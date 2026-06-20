from enterprise_agentops_mcp.tools import customers, observability, orders


def test_get_customer_by_email_dataverse_mode(monkeypatch) -> None:
    monkeypatch.setattr(customers, "DATA_MODE", "dataverse")

    def fake_dv_get(entity_set: str, **kwargs):
        if entity_set == "contacts":
            return [
                {
                    "contactid": "00000000-0000-0000-0000-000000000001",
                    "fullname": "John Smith",
                    "emailaddress1": "john.smith@contoso.com",
                    "jobtitle": "Operations Director",
                    "telephone1": "+44 20 0000 0001",
                    "_parentcustomerid_value": "00000000-0000-0000-0000-0000000000aa",
                    "address1_line1": "12 Market Street, Ipswich",
                    "address1_postalcode": "IP1 1AA",
                }
            ]
        if entity_set == "accounts":
            return [{"accountid": "00000000-0000-0000-0000-0000000000aa", "name": "Contoso Ltd"}]
        raise AssertionError(entity_set)

    monkeypatch.setattr(
        "enterprise_agentops_mcp.services.dataverse_service.dv_get",
        fake_dv_get,
    )

    result = customers.get_customer_by_email("john.smith@contoso.com")

    assert result["contactId"] == "00000000-0000-0000-0000-000000000001"
    assert result["accountName"] == "Contoso Ltd"
    assert result["riskLevel"] == "Unknown"


def test_get_latest_order_dataverse_mode(monkeypatch) -> None:
    monkeypatch.setattr(orders, "DATA_MODE", "dataverse")

    monkeypatch.setattr(
        "enterprise_agentops_mcp.services.dataverse_service.dv_get",
        lambda entity_set, **kwargs: [
            {
                "cr_orderkey": "ord-1001",
                "cr_ordernumber": "WEB-1001",
                "cr_accountid": "acc-001",
                "cr_contactid": "con-001",
                "cr_orderdate": "2026-06-10T10:00:00Z",
                "cr_status": "Shipped",
                "cr_totalamount": 349.98,
                "cr_paymentstatus": "Paid",
                "cr_deliverystatus": "Delayed",
                "cr_shipmentkeyref": "ship-9001",
                "cr_risklevel": "High",
                "cr_deliveryaddress": "12 Market Street, Ipswich",
                "cr_deliverypostcode": "IP1 1AA",
            }
        ],
    )

    result = orders.get_latest_order("00000000-0000-0000-0000-000000000001")

    assert result["orderId"] == "ord-1001"
    assert result["orderNumber"] == "WEB-1001"
    assert result["deliveryStatus"] == "Delayed"


def test_log_agent_run_dataverse_mode(monkeypatch) -> None:
    monkeypatch.setattr(observability, "DATA_MODE", "dataverse")
    captured: dict = {}

    def fake_dv_post(entity_set: str, data: dict) -> dict:
        captured["entity_set"] = entity_set
        captured["data"] = data
        return {"status": "created"}

    monkeypatch.setattr(
        "enterprise_agentops_mcp.services.dataverse_service.dv_post",
        fake_dv_post,
    )

    result = observability.log_agent_run(
        workflow_name="WebshopOrderSupport",
        intent="SummariseLatestOrderIssue",
        model_used="gpt-5-mini",
        vendor="OpenAI",
        input_tokens=1800,
        output_tokens=450,
        latency_ms=3200,
        tools_called=["get_customer_by_email", "get_latest_order"],
        requires_approval=True,
        risk_score=0.82,
        quality_score=0.88,
        groundedness_score=0.91,
    )

    assert result["logged"] is True
    assert captured["entity_set"] == "cr_agentruns"
    assert captured["data"]["cr_workflowname"] == "WebshopOrderSupport"
    assert captured["data"]["cr_runkey"].startswith("run-")

