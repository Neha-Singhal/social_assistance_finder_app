import pytest
from .conftest import client
from app.models.user import User
from app.main import app
from app.auth.auth import get_current_user

# Override get_current_user
def override_get_current_user():
    return User(id=1, name="Test User", email="test@example.com", password="fakehashed")

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture(scope="module")
def created_service():
    payload = {"name": "Shelter"}
    response = client.post("/services/ServiceRead", json=payload)
    assert response.status_code in (200, 201)
    return response.json()

def test_create_service():
    payload = {"name": "Food"}
    response = client.post("/services/ServiceRead", json=payload)
    assert response.status_code in (200, 201)
    assert response.json()["name"] == "Food"

def test_get_services():
    response = client.get("/services/ServiceRead", params={"service_id": 1})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_service(created_service):
    service_id = created_service["id"]
    update_payload = {"name": "Updated Shelter"}
    response = client.put(f"/services/service/{service_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Shelter"

def test_delete_service(created_service):
    service_id = created_service["id"]
    response = client.delete(f"/services/service/{service_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

def test_get_nonexistent_support_request():
    response = client.get("/services/support/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Support request not found"