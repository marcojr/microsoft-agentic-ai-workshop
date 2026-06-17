# Stage 2: MCP Server Local MVP (Day 2)

Build the local MCP Server with mock JSON data and implement the first tools for the Webshop Order Support scenario.

---

## Day 2 Deliverables

- [ ] MCP Server running locally
- [ ] Mock data JSON files populated (accounts, contacts, orders, shipments)
- [ ] `get_customer_by_email` implemented and tested
- [ ] `get_latest_order` implemented and tested
- [ ] `get_order_details` implemented and tested
- [ ] `get_order_items` implemented and tested
- [ ] `get_shipment_status` implemented and tested
- [ ] Tested with `fastmcp dev` + MCP Inspector
- [ ] Tested with Cursor MCP client

---

## Mock Data

### contacts.json

```json
[
  {
    "contactId": "con-001",
    "accountId": "acc-001",
    "fullName": "John Smith",
    "email": "john.smith@contoso.com",
    "role": "Operations Director",
    "phone": "+44 20 0000 0001",
    "preferredLanguage": "English",
    "deliveryAddress": "12 Market Street, Ipswich",
    "deliveryPostcode": "IP1 1AA"
  },
  {
    "contactId": "con-002",
    "accountId": "acc-002",
    "fullName": "Emma Clarke",
    "email": "emma.clarke@fabrikam.com",
    "role": "Procurement Manager",
    "phone": "+44 20 0000 0002",
    "preferredLanguage": "English",
    "deliveryAddress": "45 Bridge Road, Manchester",
    "deliveryPostcode": "M1 2AB"
  }
]
```

### accounts.json

```json
[
  {
    "accountId": "acc-001",
    "name": "Contoso Ltd",
    "accountNumber": "C-1001",
    "industry": "Retail",
    "region": "UK",
    "relationshipManager": "Sarah Mitchell",
    "riskLevel": "Medium"
  },
  {
    "accountId": "acc-002",
    "name": "Fabrikam Group",
    "accountNumber": "F-2001",
    "industry": "Manufacturing",
    "region": "EU",
    "relationshipManager": "James Carter",
    "riskLevel": "Low"
  }
]
```

### orders.json

```json
[
  {
    "orderId": "ord-1001",
    "orderNumber": "WEB-1001",
    "accountId": "acc-001",
    "contactId": "con-001",
    "orderDate": "2026-06-10T10:00:00Z",
    "status": "Shipped",
    "totalAmount": 349.98,
    "paymentStatus": "Paid",
    "deliveryStatus": "Delayed",
    "shipmentId": "ship-9001",
    "riskLevel": "High",
    "deliveryAddress": "12 Market Street, Ipswich",
    "deliveryPostcode": "IP1 1AA"
  },
  {
    "orderId": "ord-1002",
    "orderNumber": "WEB-1002",
    "accountId": "acc-001",
    "contactId": "con-001",
    "orderDate": "2026-05-20T09:00:00Z",
    "status": "Delivered",
    "totalAmount": 89.99,
    "paymentStatus": "Paid",
    "deliveryStatus": "Delivered",
    "shipmentId": "ship-9002",
    "riskLevel": "Low",
    "deliveryAddress": "12 Market Street, Ipswich",
    "deliveryPostcode": "IP1 1AA"
  }
]
```

### order_items.json

```json
[
  {
    "orderItemId": "oi-001",
    "orderId": "ord-1001",
    "productId": "prod-001",
    "sku": "SKU-100",
    "productName": "Premium Coffee Machine",
    "quantity": 1,
    "unitPrice": 299.99,
    "totalPrice": 299.99
  },
  {
    "orderItemId": "oi-002",
    "orderId": "ord-1001",
    "productId": "prod-002",
    "sku": "SKU-101",
    "productName": "Coffee Capsules Pack (x50)",
    "quantity": 1,
    "unitPrice": 49.99,
    "totalPrice": 49.99
  }
]
```

### shipments.json

```json
[
  {
    "shipmentId": "ship-9001",
    "orderId": "ord-1001",
    "carrier": "DemoCarrier",
    "trackingNumber": "TRK-123456",
    "status": "Delayed",
    "estimatedDeliveryDate": "2026-06-18",
    "deliveredDate": null,
    "delayReason": "Carrier network disruption",
    "originPostcode": "SW1A 1AA",
    "destinationPostcode": "IP1 1AA",
    "routeDistanceKm": 117
  },
  {
    "shipmentId": "ship-9002",
    "orderId": "ord-1002",
    "carrier": "DemoCarrier",
    "trackingNumber": "TRK-123400",
    "status": "Delivered",
    "estimatedDeliveryDate": "2026-05-23",
    "deliveredDate": "2026-05-23T14:30:00Z",
    "delayReason": null,
    "originPostcode": "SW1A 1AA",
    "destinationPostcode": "IP1 1AA",
    "routeDistanceKm": 117
  }
]
```

### pricing.json

```json
[
  {
    "vendor": "Anthropic",
    "model": "claude-sonnet-4-6",
    "inputTokenPricePer1M": 3.00,
    "outputTokenPricePer1M": 15.00,
    "currency": "USD"
  },
  {
    "vendor": "Anthropic",
    "model": "claude-haiku-4-5-20251001",
    "inputTokenPricePer1M": 0.80,
    "outputTokenPricePer1M": 4.00,
    "currency": "USD"
  },
  {
    "vendor": "OpenAI",
    "model": "gpt-4.1-mini",
    "inputTokenPricePer1M": 0.40,
    "outputTokenPricePer1M": 1.60,
    "currency": "USD"
  },
  {
    "vendor": "OpenAI",
    "model": "gpt-4o-mini",
    "inputTokenPricePer1M": 0.15,
    "outputTokenPricePer1M": 0.60,
    "currency": "USD"
  }
]
```

---

## Mock Data Service

**File:** `mcp-server/src/enterprise_agentops_mcp/services/mock_data_service.py`

```python
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def load(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)

def save(filename: str, data: list[dict]) -> None:
    with open(DATA_DIR / filename, "w") as f:
        json.dump(data, f, indent=2, default=str)
```

---

## Tool: get_customer_by_email

**File:** `mcp-server/src/enterprise_agentops_mcp/tools/customers.py`

```python
from fastmcp import FastMCP
from enterprise_agentops_mcp.services.mock_data_service import load
from enterprise_agentops_mcp.config import DATA_MODE

router = FastMCP()

@router.tool()
def get_customer_by_email(email: str) -> dict:
    """Find a customer/contact by email address."""
    if DATA_MODE == "mock":
        contacts = load("contacts.json")
        accounts = load("accounts.json")
        contact = next((c for c in contacts if c["email"].lower() == email.lower()), None)
        if not contact:
            return {"error": f"Customer not found: {email}"}
        account = next((a for a in accounts if a["accountId"] == contact["accountId"]), {})
        return {
            **contact,
            "accountName": account.get("name", ""),
            "riskLevel": account.get("riskLevel", "Unknown")
        }
    raise NotImplementedError("Dataverse mode not yet implemented — see Stage 7")
```

---

## Tool: Orders

**File:** `mcp-server/src/enterprise_agentops_mcp/tools/orders.py`

```python
from fastmcp import FastMCP
from enterprise_agentops_mcp.services.mock_data_service import load
from enterprise_agentops_mcp.config import DATA_MODE

router = FastMCP()

@router.tool()
def get_latest_order(contact_id: str) -> dict:
    """Retrieve the most recent order for a contact."""
    if DATA_MODE == "mock":
        orders = load("orders.json")
        contact_orders = [o for o in orders if o["contactId"] == contact_id]
        if not contact_orders:
            return {"error": f"No orders found for contact: {contact_id}"}
        return sorted(contact_orders, key=lambda o: o["orderDate"], reverse=True)[0]
    raise NotImplementedError("Dataverse mode not yet implemented — see Stage 7")

@router.tool()
def get_order_details(order_id: str) -> dict:
    """Retrieve order header and key metadata."""
    if DATA_MODE == "mock":
        orders = load("orders.json")
        order = next((o for o in orders if o["orderId"] == order_id), None)
        if not order:
            return {"error": f"Order not found: {order_id}"}
        return order
    raise NotImplementedError("Dataverse mode not yet implemented — see Stage 7")

@router.tool()
def get_order_items(order_id: str) -> dict:
    """Retrieve all line items for an order."""
    if DATA_MODE == "mock":
        items = load("order_items.json")
        return {"orderId": order_id, "items": [i for i in items if i["orderId"] == order_id]}
    raise NotImplementedError("Dataverse mode not yet implemented — see Stage 7")
```

---

## Tool: get_shipment_status

**File:** `mcp-server/src/enterprise_agentops_mcp/tools/shipments.py`

```python
from fastmcp import FastMCP
from enterprise_agentops_mcp.services.mock_data_service import load
from enterprise_agentops_mcp.config import DATA_MODE

router = FastMCP()

@router.tool()
def get_shipment_status(shipment_id: str) -> dict:
    """Retrieve shipment status and tracking information."""
    if DATA_MODE == "mock":
        shipments = load("shipments.json")
        shipment = next((s for s in shipments if s["shipmentId"] == shipment_id), None)
        if not shipment:
            return {"error": f"Shipment not found: {shipment_id}"}
        return shipment
    raise NotImplementedError("Dataverse mode not yet implemented — see Stage 7")
```

---

## MCP Server Entry Point

**File:** `mcp-server/src/enterprise_agentops_mcp/server.py`

```python
from fastmcp import FastMCP

mcp = FastMCP("enterprise-agentops-mcp-server")

from enterprise_agentops_mcp.tools.customers import router as customers_router
from enterprise_agentops_mcp.tools.accounts import router as accounts_router
from enterprise_agentops_mcp.tools.orders import router as orders_router
from enterprise_agentops_mcp.tools.shipments import router as shipments_router

mcp.include_router(customers_router)
mcp.include_router(accounts_router)
mcp.include_router(orders_router)
mcp.include_router(shipments_router)

if __name__ == "__main__":
    mcp.run()
```

---

## Running the MCP Server

```bash
cd mcp-server

# Install dependencies
uv sync

# Development mode with MCP Inspector UI
uv run fastmcp dev src/enterprise_agentops_mcp/server.py
# Opens at http://localhost:5173
```

---

## Connecting Cursor

Add to `~/.cursor/mcp.json` (or Settings > MCP):

```json
{
  "mcpServers": {
    "enterprise-agentops": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:/Users/conta/codebases/MS Agentic AI/mcp-server",
        "fastmcp",
        "run",
        "src/enterprise_agentops_mcp/server.py"
      ]
    }
  }
}
```

---

## Next Step

[docs/03-mcp-tools-extended.md](03-mcp-tools-extended.md) — Day 3: remaining tools (returns, refunds, cases, knowledge, approvals, cost, logging, evaluation).
