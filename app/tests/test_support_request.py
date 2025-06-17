from httpx import AsyncClient,ASGITransport
from app.main import app
from app.auth.auth import get_current_user
from app.models.user import User
import pytest

# Step 1: Override the dependency
def override_get_current_user():

    return User(
        id=1,
        name="Test User",
        email="test@example.com",
        is_admin=False,
        is_active=True
    )

@pytest.mark.asyncio
async def test_create_get_update_delete_support_request():
    app.dependency_overrides[get_current_user] = override_get_current_user

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # CREATE
        payload = {
            "user_id": 1,
            "ngo_id": 3,
            "comment": "need shelter"
        }
        create_response = await ac.post("/support-request/", json=payload)
        assert create_response.status_code == 200
        data = create_response.json()
        support_id = data["id"]

        #GET
        get_response = await ac.get(f"/support-request/{support_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == support_id

        # UPDATE
        update_payload = {"status": "accepted"}
        update_response = await ac.patch(
            f"/support-request/{support_id}", json=update_payload
        )
        assert update_response.status_code == 200


        # DELETE
        delete_response = await ac.delete(f"/support-request/{support_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "Request deleted successfully"

    # Clean up override
    app.dependency_overrides.clear()
    app.dependency_overrides[get_current_user] = override_get_current_user