import uuid

import pytest
from .conftest import client



def test_create_new_ngo():
    unique_email = f"user_{uuid.uuid4()}@example.com"
    new_ngo = {
        "name": "NGO Love and Sons",
        "email": unique_email,
        "location": "Mumbai",
        "password": "password123",
        "user_type": "ngo",
        "phone_number": "0676543"
    }
    response = client.post(
        "/users",
        json=new_ngo,
    )
    assert response.status_code == 200


def login_for_access_token():
    login_credential = {
        "username": "charity@gmail.com",
        "password": "123",
    }

    response = client.post(
        "/users/token",
        data=login_credential,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response

def get_auth_header():
    response = login_for_access_token()
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_login_ngo():
    response = login_for_access_token() #try to get response
    assert response.status_code == 200


def get_current_ngo_id(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me/", headers=headers)
    print("DEBUG /users/me response:", response.json())
    return response.json()["id"]


def test_patch_user():
    login_data = login_for_access_token()
    assert login_data.status_code == 200
    token = login_data.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    ngo_id = get_current_ngo_id(token)

    new_service = {
        "service_id": 1,
        "ngo_id": ngo_id,

    }

    create_response = client.post("/ngo_service/", json=new_service, headers=headers)
    assert create_response.status_code == 200
    entry_id = create_response.json()["id"]

    update_data = {
        "service_id" : 1
    }



    response = client.patch(f"/ngo_service/{entry_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["service_id"] == 1
