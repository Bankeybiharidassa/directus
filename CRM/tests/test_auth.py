from fastapi.testclient import TestClient
from backend.main import app
import pyotp

client = TestClient(app)


def test_user_creation_and_authentication():
    response = client.post("/users/", params={"username": "alice", "password": "secret"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"

    auth = ("alice", "secret")
    me_resp = client.get("/users/me", auth=auth)
    assert me_resp.status_code == 200
    assert me_resp.json()["username"] == "alice"


def test_mfa_enforcement_and_login():
    # create user
    resp = client.post("/users/", params={"username": "bob", "password": "secret"})
    user_id = resp.json()["id"]

    # enable MFA
    enforce = client.post(f"/users/{user_id}/enforce_mfa")
    secret = enforce.json()["secret"]

    auth = ("bob", "secret")

    # request without TOTP should fail
    fail_resp = client.get("/users/me", auth=auth)
    assert fail_resp.status_code == 401

    totp = pyotp.TOTP(secret)
    headers = {"X-TOTP": totp.now()}
    success_resp = client.get("/users/me", auth=auth, headers=headers)
    assert success_resp.status_code == 200


def test_rbac_access_control():
    # create admin role and user
    user_resp = client.post("/users/", params={"username": "carol", "password": "pw"})
    user_id = user_resp.json()["id"]
    role_resp = client.post("/roles/", params={"name": "admin"})
    role_id = role_resp.json()["id"]
    client.post(f"/roles/{role_id}/assign/{user_id}")

    # access protected endpoint
    resp = client.get("/core/log/export", auth=("carol", "pw"))
    assert resp.status_code == 200

    # user without role
    user_resp2 = client.post("/users/", params={"username": "dave", "password": "pw"})
    resp_forbidden = client.get("/core/log/export", auth=("dave", "pw"))
    assert resp_forbidden.status_code == 403
