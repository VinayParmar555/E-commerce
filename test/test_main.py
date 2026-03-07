"""
Expanded test suite for the E-commerce backend.
Tests cover: Auth, Products (CRUD, pagination, filter), Cart, and Order checkout.

These tests use FastAPI's TestClient and run against an in-memory SQLite DB
so they require no external services (no Postgres/Redis needed).
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

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
    token = res.json().get("access_token", "")
    return {"Authorization": f"Bearer {token}"}


# ─────────────────────────────────────────────────────────────
# Auth Tests
# ─────────────────────────────────────────────────────────────

def test_register():
    response = register_user()
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "demo@example.com"
    assert "id" in data
    assert "password" not in data


def test_register_duplicate():
    response = register_user()
    assert response.status_code == 400


def test_login():
    response = login_user()
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_password():
    response = login_user(password="wrongpassword")
    assert response.status_code in (400, 401)


def test_verify_request():
    headers = auth_headers()
    response = client.post("/account/verify-request", headers=headers)
    assert response.status_code == 200


def test_protected_route_without_token():
    """Any protected route should return 401 when no token is provided."""
    response = client.get("/Cart/see_cart")
    assert response.status_code == 401


# ─────────────────────────────────────────────────────────────
# Products Tests
# ─────────────────────────────────────────────────────────────

def test_get_all_products_unauthenticated():
    """Product listing is public (rate-limited by IP)."""
    response = client.get("/products/all")
    # 200 with data or 404 if DB is empty — both are valid
    assert response.status_code in (200, 404)


def test_get_products_pagination():
    response = client.get("/products/pagination?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "page" in data
    assert "limit" in data
    assert "count" in data
    assert "data" in data


def test_get_products_filter_missing_category():
    """Filter requires the `category` query param — missing it should 422."""
    response = client.get("/products/filter")
    assert response.status_code == 422


def test_get_products_filter_with_category():
    response = client.get("/products/filter?category=electronics")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


def test_add_product_requires_admin():
    """Non-admin authenticated user should get 403."""
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
    # 404 when cart is empty, 200 when it has items
    assert response.status_code in (200, 404)


def test_add_to_cart_unauthenticated():
    response = client.post("/Cart/add_cart", json={"product_id": 1, "quantity": 1})
    assert response.status_code == 401


def test_add_to_cart_nonexistent_product():
    """Adding a product that doesn't exist should return 404."""
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
    """Checkout with an empty cart should return 404 (CartItemError)."""
    headers = auth_headers()
    payload = {
        "amount": 1000,
        "shipping_address_id": 1,
        "gateway": "mock",
        "simulate_succ": True
    }
    response = client.post("/order/checkout", json=payload, headers=headers)
    # 404 for empty cart (CartItemError) or 404 for invalid address
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
