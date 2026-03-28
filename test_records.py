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
    
    
def test_get_records_unauthorized():
    response = client.get("/records/")
    assert response.status_code == 401


def test_get_records_authorized():
    response = client.get("/records/", headers=auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_record_not_found():
    response = client.get("/records/9999", headers=auth_headers())
    assert response.status_code == 404
    assert response.json()["detail"] == "Record not found"


def test_get_record_invalid_id():
    response = client.get("/records/0", headers=auth_headers())
    assert response.status_code == 422  # validation error — id must be >= 1


def test_create_record_missing_fields():
    response = client.post(
        "/records/",
        headers=auth_headers(),
        json={"patient_name": "John"}  # missing required fields
    )
    assert response.status_code == 422
    
def dummy_record():
    return {
        "patient_name": "Test Patient",
        "age": 25,
        "blood_type": "A+",
        "diagnosis": "Test diagnosis here",
        "doctor_id": 1,
        "email": "test@example.com",
        "phone": "+14155551234",
        "admitted_at": "2024-01-15T09:00:00",
        "is_admitted": True,
        "notes": "Test notes",
        "weight": 70.0,
        "height": 170.0
    }


def test_create_record_success():
    response = client.post(
        "/records/",
        headers=auth_headers(),
        json=dummy_record()
    )
    assert response.status_code == 201
    assert response.json()["patient_name"] == "Test Patient"
    assert "id" in response.json()


def test_create_record_invalid_age():
    data = dummy_record()
    data["age"] = 200  # age > 120 → invalid
    response = client.post(
        "/records/",
        headers=auth_headers(),
        json=data
    )
    assert response.status_code == 422


def test_create_record_invalid_blood_type():
    data = dummy_record()
    data["blood_type"] = "Z+"  # invalid blood type
    response = client.post(
        "/records/",
        headers=auth_headers(),
        json=data
    )
    assert response.status_code == 422


def test_get_record_success():
    # first create a record
    create = client.post(
        "/records/",
        headers=auth_headers(),
        json=dummy_record()
    )
    record_id = create.json()["id"]

    # then get it
    response = client.get(
        f"/records/{record_id}",
        headers=auth_headers()
    )
    assert response.status_code == 200
    assert response.json()["id"] == record_id


def test_update_record_success():
    # first create a record
    create = client.post(
        "/records/",
        headers=auth_headers(),
        json=dummy_record()
    )
    record_id = create.json()["id"]

    # then update it
    updated_data = dummy_record()
    updated_data["patient_name"] = "Updated Patient"
    response = client.put(
        f"/records/{record_id}",
        headers=auth_headers(),
        json=updated_data
    )
    assert response.status_code == 200
    assert response.json()["patient_name"] == "Updated Patient"


def test_delete_record_success():
    # first create a record
    create = client.post(
        "/records/",
        headers=auth_headers(),
        json=dummy_record()
    )
    record_id = create.json()["id"]

    # then delete it
    response = client.delete(
        f"/records/{record_id}",
        headers=auth_headers()
    )
    assert response.status_code == 204

    # verify it's gone
    response = client.get(
        f"/records/{record_id}",
        headers=auth_headers()
    )
    assert response.status_code == 404


def test_delete_record_not_found():
    response = client.delete(
        "/records/9999",
        headers=auth_headers()
    )
    assert response.status_code == 404