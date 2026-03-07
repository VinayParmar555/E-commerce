import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from app.cache.redis_client import redis_client

client = TestClient(app)

# ─────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_rate_limits():
    for key in redis_client.scan_iter("rate:ip:*"):
        redis_client.delete(key)
    for key in redis_client.scan_iter("rate:user:*"):
        redis_client.delete(key)
    yield

@pytest.fixture(autouse=True)
def ensure_user_exists():
    register_user()
    yield

# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def register_user(email="demo@example.com", password="demo123", name="demo"):
    return client.post("/account/register", json={
        "name": name, "email": email, "password": password
    })

def login_user(email="demo@example.com", password="demo123"):
    return client.post("/account/login", data={
        "username": email, "password": password
    })

def auth_headers(email="demo@example.com", password="demo123"):
    res = login_user(email, password)
    token = res.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

# ─────────────────────────────────────────────────────────────
# Auth Tests
# ─────────────────────────────────────────────────────────────

def test_register_fresh():
    response = register_user(email="fresh@example.com", password="fresh123", name="fresh")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "fresh@example.com"
    assert "id" in data
    assert "password" not in data

def test_login():
    response = login_user()
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_wrong_password():
    response = login_user(password="wrongpassword")
    assert response.status_code in (400, 401)

def test_verify_request():
    headers = auth_headers()
    response = client.post("/account/verify-request", headers=headers)
    assert response.status_code == 200

def test_protected_route_without_token():
    response = client.get("/Cart/see_cart")
    assert response.status_code == 401

# ─────────────────────────────────────────────────────────────
# Products Tests
# ─────────────────────────────────────────────────────────────

def test_get_all_products_unauthenticated():
    response = client.get("/products/all")
    assert response.status_code in (200, 404, 429)

def test_get_products_pagination():
    response = client.get("/products/pagination?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "page" in data
    assert "limit" in data
    assert "count" in data
    assert "data" in data

def test_get_products_filter_missing_category():
    response = client.get("/products/filter")
    assert response.status_code == 422

def test_get_products_filter_with_category():
    response = client.get("/products/filter?category=electronics")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data

def test_add_product_requires_admin():
    headers = auth_headers()
    payload = {
        "name": "Test Phone",
        "price": 9999.0,
        "description": "A test product",
        "quantity": 50,
        "category_id": 1
    }
    response = client.post("/products/add_product", json=payload, headers=headers)
    assert response.status_code == 403

def test_add_product_unauthenticated():
    payload = {
        "name": "Test Phone",
        "price": 9999.0,
        "description": "A test product",
        "quantity": 50,
        "category_id": 1
    }
    response = client.post("/products/add_product", json=payload)
    assert response.status_code == 401

def test_search_product_not_found():
    response = client.get("/products/search/999999")
    assert response.status_code == 404

def test_delete_product_requires_admin():
    headers = auth_headers()
    response = client.delete("/products/delete/1", headers=headers)
    assert response.status_code == 403

# ─────────────────────────────────────────────────────────────
# Cart Tests
# ─────────────────────────────────────────────────────────────

def test_see_cart_unauthenticated():
    response = client.get("/Cart/see_cart")
    assert response.status_code == 401

def test_see_cart_empty():
    headers = auth_headers()
    response = client.get("/Cart/see_cart", headers=headers)
    assert response.status_code in (200, 404)

def test_add_to_cart_unauthenticated():
    response = client.post("/Cart/add_cart", json={"product_id": 1, "quantity": 1})
    assert response.status_code == 401

def test_add_to_cart_nonexistent_product():
    headers = auth_headers()
    response = client.post("/Cart/add_cart",
                           json={"product_id": 999999, "quantity": 1},
                           headers=headers)
    assert response.status_code == 404

def test_delete_cart_not_found():
    headers = auth_headers()
    response = client.delete("/Cart/delete_cart/999999", headers=headers)
    assert response.status_code == 404

# ─────────────────────────────────────────────────────────────
# Order / Checkout Tests
# ─────────────────────────────────────────────────────────────

def test_checkout_unauthenticated():
    payload = {
        "amount": 1000,
        "shipping_address_id": 1,
        "gateway": "mock",
        "simulate_succ": True
    }
    response = client.post("/order/checkout", json=payload)
    assert response.status_code == 401

def test_checkout_empty_cart():
    headers = auth_headers()
    payload = {
        "amount": 1000,
        "shipping_address_id": 1,
        "gateway": "mock",
        "simulate_succ": True
    }
    response = client.post("/order/checkout", json=payload, headers=headers)
    assert response.status_code in (400, 404)

def test_fetch_placed_orders_unauthenticated():
    response = client.get("/order/fetch_placed_order")
    assert response.status_code == 401

def test_fetch_placed_orders_empty():
    headers = auth_headers()
    response = client.get("/order/fetch_placed_order", headers=headers)
    assert response.status_code in (200, 404)

def test_cancel_nonexistent_order():
    headers = auth_headers()
    response = client.patch("/order/cancel/999999", headers=headers)
    assert response.status_code == 404

def test_shipping_status_not_found():
    headers = auth_headers()
    response = client.get("/order/shipping_status/999999", headers=headers)
    assert response.status_code == 404

def test_update_shipping_status_requires_admin():
    headers = auth_headers()
    response = client.patch(
        "/order/update_shipping_status/1",
        params={"new_status": "processing"},
        headers=headers
    )
    assert response.status_code == 403