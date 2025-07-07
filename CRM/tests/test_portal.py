from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_portal_revoke():
    user_resp = client.post("/users/", params={"username": "bob", "password": "p"})
    assert user_resp.status_code == 200
    user_id = user_resp.json()["id"]

    revoke = client.post(f"/pages/portal/revoke/{user_id}")
    assert revoke.status_code == 200
    assert revoke.json()["portal_access"] is False
