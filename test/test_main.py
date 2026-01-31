from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def register():
    payload={
        "name" : "demo",
        "email" : "demo@example.com",
        "password" : "demo123"
    }
    return client.post("/account/register", json=payload)

def login():
     payload={
        "username" : "demo@example.com",
        "password" : "demo123"
    }
     return client.post("/account/login", data=payload)

def test_register():
    response = register()
    assert response.status_code==200
    data = response.json()
    assert data["email"] == "demo@example.com"
    assert "id" in data
    assert "password" not in data

def test_register_duplicate():
    payload={
        "name" : "demo",
        "email" : "demo@example.com",
        "password" : "demo123"
    }
    response = client.post("/account/register", json=payload)
    assert response.status_code==400

def test_login():
    response = login()
    assert response.status_code == 200
    return response.json()["access_token"]

def test_verify_request():
    fetch_token = login()
    token = fetch_token.json()["access_token"]
    response = client.post("/account/verify-request", headers={"Authorization" : f"Bearer {token}"})
    assert response.status_code==200
