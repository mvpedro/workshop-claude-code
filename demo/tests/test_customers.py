import pytest
from httpx import AsyncClient


async def create_customer(client: AsyncClient, headers: dict, **kwargs) -> dict:
    data = {
        "name": kwargs.get("name", "Test Customer"),
        "email": kwargs.get("email", "test@example.com"),
        "segment": kwargs.get("segment", "bronze"),
    }
    if "phone" in kwargs:
        data["phone"] = kwargs["phone"]
    resp = await client.post("/api/v1/customers", json=data, headers=headers)
    assert resp.status_code == 201, resp.text
    return resp.json()


async def test_create_customer(client: AsyncClient, api_headers: dict):
    resp = await client.post(
        "/api/v1/customers",
        json={"name": "Alice", "email": "alice@example.com"},
        headers=api_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"


async def test_list_customers(client: AsyncClient, api_headers: dict):
    for i in range(3):
        await create_customer(client, api_headers, name=f"Customer {i}", email=f"c{i}@example.com")

    resp = await client.get("/api/v1/customers", headers=api_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3


async def test_get_customer(client: AsyncClient, api_headers: dict):
    created = await create_customer(client, api_headers, name="Bob", email="bob@example.com")
    customer_id = created["id"]

    resp = await client.get(f"/api/v1/customers/{customer_id}", headers=api_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == customer_id
    assert data["name"] == "Bob"
    assert data["email"] == "bob@example.com"


async def test_update_customer(client: AsyncClient, api_headers: dict):
    created = await create_customer(client, api_headers, name="Charlie", email="charlie@example.com")
    customer_id = created["id"]

    resp = await client.put(
        f"/api/v1/customers/{customer_id}",
        json={"name": "Charlie Updated"},
        headers=api_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Charlie Updated"


async def test_delete_customer(client: AsyncClient, api_headers: dict):
    created = await create_customer(client, api_headers, name="Dave", email="dave@example.com")
    customer_id = created["id"]

    resp = await client.delete(f"/api/v1/customers/{customer_id}", headers=api_headers)
    assert resp.status_code == 204

    resp = await client.get(f"/api/v1/customers/{customer_id}", headers=api_headers)
    assert resp.status_code == 404


async def test_filter_by_segment(client: AsyncClient, api_headers: dict):
    await create_customer(client, api_headers, name="Bronze User", email="bronze@example.com", segment="bronze")
    await create_customer(client, api_headers, name="Gold User", email="gold@example.com", segment="gold")

    resp = await client.get("/api/v1/customers?segment=gold", headers=api_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["segment"] == "gold"


async def test_duplicate_email(client: AsyncClient, api_headers: dict):
    await create_customer(client, api_headers, name="Original", email="dup@example.com")

    resp = await client.post(
        "/api/v1/customers",
        json={"name": "Duplicate", "email": "dup@example.com"},
        headers=api_headers,
    )
    assert resp.status_code == 409
