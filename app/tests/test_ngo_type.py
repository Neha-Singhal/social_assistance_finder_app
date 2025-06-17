import uuid
from .conftest import client

def test_create_ngo():
    unique_email = f"ngo_{uuid.uuid4().hex}@gmail.com"

    payload = {
        "name": "Helping Hands",
        "email": unique_email,
        "password": "securepassword123",
        "location": "Delhi",
        "user_type": "ngo",
        "phone_number": "2345678"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == unique_email
    assert data["user_type"] == "ngo"
    assert "id" in data


