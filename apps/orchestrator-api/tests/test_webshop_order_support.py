from src.webshop_order_support import handle_webshop_order_support


def test_handle_webshop_order_support_success() -> None:
    result, status = handle_webshop_order_support(
        {"customerEmail": "john.smith@contoso.com", "userId": "user-001"}
    )
    assert status == 200
    assert result["customerName"] == "John Smith"
    assert result["orderNumber"] == "WEB-1001"
    assert result["approvalRequired"] is True


def test_handle_webshop_order_support_requires_email() -> None:
    result, status = handle_webshop_order_support({})
    assert status == 400
    assert result["error"] == "customerEmail is required"
