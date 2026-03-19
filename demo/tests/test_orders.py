import pytest
from httpx import AsyncClient


async def create_customer(client: AsyncClient, headers: dict, name: str = "Test Customer", email: str = "test@example.com") -> dict:
    resp = await client.post(
        "/api/v1/customers",
        json={"name": name, "email": email},
        headers=headers,
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


async def create_product(client: AsyncClient, headers: dict, name: str = "Test Product", price: float = 1000.0, stock: int = 100, sku: str = "SKU-001") -> dict:
    resp = await client.post(
        "/api/v1/products",
        json={"name": name, "price": price, "stock": stock, "category": "general", "sku": sku},
        headers=headers,
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


async def create_order(client: AsyncClient, headers: dict, customer_id: str, product_id: str, quantity: int = 5) -> dict:
    resp = await client.post(
        "/api/v1/orders",
        json={"customer_id": customer_id, "items": [{"product_id": product_id, "quantity": quantity}]},
        headers=headers,
    )
    return resp


async def test_create_order(client: AsyncClient, api_headers: dict):
    customer = await create_customer(client, api_headers, email="order_customer@example.com")
    product = await create_product(client, api_headers, stock=100, sku="ORD-P-001")

    resp = await create_order(client, api_headers, customer["id"], product["id"], quantity=5)
    assert resp.status_code == 201
    data = resp.json()
    assert data["customer_id"] == customer["id"]
    assert data["status"] == "pending"

    # Verify stock reduced
    product_resp = await client.get(f"/api/v1/products/{product['id']}", headers=api_headers)
    assert product_resp.status_code == 200
    assert product_resp.json()["stock"] == 95


async def test_create_order_insufficient_stock(client: AsyncClient, api_headers: dict):
    customer = await create_customer(client, api_headers, email="insuf_customer@example.com")
    product = await create_product(client, api_headers, stock=1, sku="INSUF-001")

    resp = await create_order(client, api_headers, customer["id"], product["id"], quantity=5)
    assert resp.status_code == 409


async def test_status_transition_valid(client: AsyncClient, api_headers: dict):
    customer = await create_customer(client, api_headers, email="trans_customer@example.com")
    product = await create_product(client, api_headers, stock=100, sku="TRANS-P-001")

    order_resp = await create_order(client, api_headers, customer["id"], product["id"], quantity=1)
    assert order_resp.status_code == 201
    order_id = order_resp.json()["id"]

    resp = await client.patch(
        f"/api/v1/orders/{order_id}/status",
        json={"status": "processing"},
        headers=api_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "processing"


async def test_status_transition_invalid(client: AsyncClient, api_headers: dict):
    customer = await create_customer(client, api_headers, email="invalid_trans@example.com")
    product = await create_product(client, api_headers, stock=100, sku="INV-TRANS-001")

    order_resp = await create_order(client, api_headers, customer["id"], product["id"], quantity=1)
    assert order_resp.status_code == 201
    order_id = order_resp.json()["id"]

    # Attempt to go directly from "pending" to "delivered" (invalid)
    resp = await client.patch(
        f"/api/v1/orders/{order_id}/status",
        json={"status": "delivered"},
        headers=api_headers,
    )
    assert resp.status_code == 422


async def test_cancel_order_releases_stock(client: AsyncClient, api_headers: dict):
    customer = await create_customer(client, api_headers, email="cancel_customer@example.com")
    product = await create_product(client, api_headers, stock=100, sku="CANCEL-P-001")

    order_resp = await create_order(client, api_headers, customer["id"], product["id"], quantity=10)
    assert order_resp.status_code == 201
    order_id = order_resp.json()["id"]

    # Verify stock was reduced
    product_resp = await client.get(f"/api/v1/products/{product['id']}", headers=api_headers)
    assert product_resp.json()["stock"] == 90

    # Cancel the order
    resp = await client.patch(
        f"/api/v1/orders/{order_id}/status",
        json={"status": "cancelled"},
        headers=api_headers,
    )
    assert resp.status_code == 200

    # Verify stock was restored
    product_resp = await client.get(f"/api/v1/products/{product['id']}", headers=api_headers)
    assert product_resp.json()["stock"] == 100


async def test_list_orders_by_customer(client: AsyncClient, api_headers: dict):
    customer_a = await create_customer(client, api_headers, name="Customer A", email="customer_a@example.com")
    customer_b = await create_customer(client, api_headers, name="Customer B", email="customer_b@example.com")
    product = await create_product(client, api_headers, stock=100, sku="LIST-P-001")

    await create_order(client, api_headers, customer_a["id"], product["id"], quantity=1)
    await create_order(client, api_headers, customer_a["id"], product["id"], quantity=1)
    await create_order(client, api_headers, customer_b["id"], product["id"], quantity=1)

    resp = await client.get(f"/api/v1/orders?customer_id={customer_a['id']}", headers=api_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
