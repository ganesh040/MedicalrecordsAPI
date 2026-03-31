import pytest
from fastapi.testclient import TestClient
from main import app

import uuid
from fastapi.testclient import TestClient
from main import app

# ── Test client ───────────────────────────
client = TestClient(app)


def create_test_doctor():
    unique_email = f"dr.test.{uuid.uuid4()}@hospital.com"
    response = client.post(
        "/doctors/",
        headers=auth_headers(),
        json={
            "name": "Dr. Test",
            "email": unique_email,
            "specialization": "General",
            "phone": "+14155551234"
        }
    )
    return response.json()["id"]


def get_token():
    response = client.post("/token", data={
        "username": "john",
        "password": "secret123"
    })
    return response.json()["access_token"]


def auth_headers():
    return {"Authorization": f"Bearer {get_token()}"}


def dummy_record(doctor_id: int = 1):
    return {
        "patient_name": "Test Patient",
        "age": 25,
        "blood_type": "A+",
        "diagnosis": "Test diagnosis here",
        "doctor_id": doctor_id,
        "email": "test@example.com",
        "phone": "+14155551234",
        "admitted_at": "2024-01-15T09:00:00",
        "is_admitted": True,
        "notes": "Test notes",
        "weight": 70.0,
        "height": 170.0
    }


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
    assert response.status_code == 422


def test_create_record_missing_fields():
    response = client.post(
        "/records/",
        headers=auth_headers(),
        json={"patient_name": "John"}
    )
    assert response.status_code == 422


def test_create_record_success():
    doctor_id = create_test_doctor()
    response = client.post(
        "/records/",
        headers=auth_headers(),
        json=dummy_record(doctor_id)
    )
    assert response.status_code == 201
    assert response.json()["patient_name"] == "Test Patient"
    assert "id" in response.json()


def test_create_record_invalid_age():
    doctor_id = create_test_doctor()
    data = dummy_record(doctor_id)
    data["age"] = 200
    response = client.post(
        "/records/",
        headers=auth_headers(),
        json=data
    )
    assert response.status_code == 422


def test_create_record_invalid_blood_type():
    doctor_id = create_test_doctor()
    data = dummy_record(doctor_id)
    data["blood_type"] = "Z+"
    response = client.post(
        "/records/",
        headers=auth_headers(),
        json=data
    )
    assert response.status_code == 422


def test_get_record_success():
    doctor_id = create_test_doctor()
    create = client.post(
        "/records/",
        headers=auth_headers(),
        json=dummy_record(doctor_id)
    )
    record_id = create.json()["id"]
    response = client.get(f"/records/{record_id}", headers=auth_headers())
    assert response.status_code == 200
    assert response.json()["id"] == record_id


def test_update_record_success():
    doctor_id = create_test_doctor()
    create = client.post(
        "/records/",
        headers=auth_headers(),
        json=dummy_record(doctor_id)
    )
    record_id = create.json()["id"]
    updated_data = dummy_record(doctor_id)
    updated_data["patient_name"] = "Updated Patient"
    response = client.put(
        f"/records/{record_id}",
        headers=auth_headers(),
        json=updated_data
    )
    assert response.status_code == 200
    assert response.json()["patient_name"] == "Updated Patient"


def test_delete_record_success():
    doctor_id = create_test_doctor()
    create = client.post(
        "/records/",
        headers=auth_headers(),
        json=dummy_record(doctor_id)
    )
    record_id = create.json()["id"]
    response = client.delete(f"/records/{record_id}", headers=auth_headers())
    assert response.status_code == 204
    response = client.get(f"/records/{record_id}", headers=auth_headers())
    assert response.status_code == 404


def test_delete_record_not_found():
    response = client.delete(
        "/records/9999",
        headers=auth_headers()
    )
    assert response.status_code == 404