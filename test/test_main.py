from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login():
    
    r1 = client.post("/account/login", data={
        "username" : "rukmini@example.com",
        "password" : "rukmini"
    })
    assert r1.status_code == 200
    return r1.json()["access_token"]

def test_me():
    token = test_login()
    r2 = client.get("/profile/me", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
