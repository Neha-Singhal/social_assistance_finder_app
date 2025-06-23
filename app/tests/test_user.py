from http.client import responses
import uuid
import pytest
from sqlmodel import Session
from .conftest import client
from ..models.user import User


def test_read_user(test_user: User):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["name"] == test_user.name
    assert data["email"] == test_user.email


@pytest.fixture
def test_user(session: Session):
    user = User(
        name="Test User",
        email="test@example.com",
        password="hashed_password",
        location="Test City",
        user_type="user",
        phone_number="1234567890"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

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
    user_id = 1
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