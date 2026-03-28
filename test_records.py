import pytest
from fastapi.testclient import TestClient
from main import app

# ── Test client ───────────────────────────
client = TestClient(app)

# ── Helper — login and get token ──────────
def get_token():
    response = client.post("/token", data={
        "username": "john",
        "password": "secret123"
    })
    return response.json()["access_token"]

# ── Helper — auth headers ─────────────────
def auth_headers():
    return {"Authorization": f"Bearer {get_token()}"}




def test_root():
    response = client.get("/")
    assert response.status_code == 200



def test_login_success():
    response = client.post("/token", data={
        "username": "john",
        "password": "secret123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password():
    response = client.post("/token", data={
        "username": "john",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_wrong_username():
    response = client.post("/token", data={
        "username": "nobody",
        "password": "secret123"
    })
    assert response.status_code == 401


def test_get_me():
    response = client.get("/me", headers=auth_headers())
    assert response.status_code == 200
    assert response.json()["username"] == "john"


def test_get_me_no_token():
    response = client.get("/me")
    assert response.status_code == 401