from http.client import responses
import uuid
from .conftest import client


def test_read_user():
    response = client.get("/users/2")
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "name": "amy",
        "email": "amy@gmail.com",
        "location": "France",
        "user_type": "user",
        "phone_number": None
    }


def test_create_user():
    unique_email = f"bina_{uuid.uuid4().hex}@gmail.com"
    payload = {
        "name": "Bina",
        "email": unique_email,
        "password": "strongpassword123",
        "location": "France",
        "user_type": "user",
        "phone_number": "1234567"
    }

    response = client.post("/users/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == unique_email
    assert data["name"] == "Bina"
    assert "id" in data


def test_get_all_user():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(),list)


def test_get_user_by_id():
    user_id = 4
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "name" in data


def test_create_user_invalid():
    payload = {
    "name":"invalid_user",
    "location": "Berlin",
    "user_type": "user"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 422