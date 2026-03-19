import pytest
from httpx import AsyncClient


async def create_product(client: AsyncClient, headers: dict, **kwargs) -> dict:
    data = {
        "name": kwargs.get("name", "Test Product"),
        "price": kwargs.get("price", 1000.0),
        "stock": kwargs.get("stock", 50),
        "category": kwargs.get("category", "general"),
        "sku": kwargs.get("sku", "SKU-001"),
    }
    if "description" in kwargs:
        data["description"] = kwargs["description"]
    resp = await client.post("/api/v1/products", json=data, headers=headers)
    assert resp.status_code == 201, resp.text
    return resp.json()


async def test_create_product(client: AsyncClient, api_headers: dict):
    resp = await client.post(
        "/api/v1/products",
        json={"name": "Widget", "price": 500.0, "stock": 100, "category": "widgets", "sku": "WGT-001"},
        headers=api_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert data["name"] == "Widget"


async def test_list_products(client: AsyncClient, api_headers: dict):
    await create_product(client, api_headers, name="Product 1", sku="P-001")
    await create_product(client, api_headers, name="Product 2", sku="P-002")

    resp = await client.get("/api/v1/products", headers=api_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2


async def test_get_product(client: AsyncClient, api_headers: dict):
    created = await create_product(client, api_headers, name="Gadget", price=750.0, sku="GDG-001")
    product_id = created["id"]

    resp = await client.get(f"/api/v1/products/{product_id}", headers=api_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == product_id
    assert data["name"] == "Gadget"
    assert data["price"] == 750.0


async def test_update_product(client: AsyncClient, api_headers: dict):
    created = await create_product(client, api_headers, name="Old Name", price=100.0, sku="UPD-001")
    product_id = created["id"]

    resp = await client.put(
        f"/api/v1/products/{product_id}",
        json={"price": 200.0},
        headers=api_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["price"] == 200.0


async def test_delete_product(client: AsyncClient, api_headers: dict):
    created = await create_product(client, api_headers, name="To Delete", sku="DEL-001")
    product_id = created["id"]

    resp = await client.delete(f"/api/v1/products/{product_id}", headers=api_headers)
    assert resp.status_code == 204

    resp = await client.get(f"/api/v1/products/{product_id}", headers=api_headers)
    assert resp.status_code == 404


async def test_filter_by_category(client: AsyncClient, api_headers: dict):
    await create_product(client, api_headers, name="Electronics 1", category="electronics", sku="EL-001")
    await create_product(client, api_headers, name="Electronics 2", category="electronics", sku="EL-002")
    await create_product(client, api_headers, name="Food Item", category="food", sku="FD-001")

    resp = await client.get("/api/v1/products?category=electronics", headers=api_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2


async def test_low_stock(client: AsyncClient, api_headers: dict):
    created = await create_product(client, api_headers, name="Low Stock Product", stock=3, sku="LOW-001")

    resp = await client.get("/api/v1/products/low-stock", headers=api_headers)
    assert resp.status_code == 200
    data = resp.json()
    product_ids = [p["id"] for p in data]
    assert created["id"] in product_ids
