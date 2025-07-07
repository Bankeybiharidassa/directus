import pytest
import base64
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_admin_login_page():
    resp = client.get("/core/login")
    assert resp.status_code == 200
    assert "Login" in resp.text


def test_login_uses_request_host():
    resp = client.get("/core/login", headers={"host": "myhost:8000"})
    assert "action='http://myhost:3001/login'" in resp.text


def test_login_falls_back_to_local_ip(monkeypatch):
    monkeypatch.setattr("backend.routes.core.get_local_ip", lambda: "192.0.2.5")
    resp = client.get("/core/login", headers={"host": "0.0.0.0:8000"})
    assert "action='http://192.0.2.5:3001/login'" in resp.text


def test_login_with_role_customizes_heading():
    resp = client.get("/core/login", params={"role": "distributor"})
    assert "Distributor Login" in resp.text
    assert "name='role' value='distributor'" in resp.text


def create_user_with_role(username: str, role: str):
    u = client.post("/users/", params={"username": username, "password": "pw"})
    uid = u.json()["id"]
    r = client.post("/roles/", params={"name": role})
    rid = r.json()["id"]
    client.post(f"/roles/{rid}/assign/{uid}")


def test_admin_page_exists():
    create_user_with_role("adm", "admin")
    resp = client.get("/core/admin", auth=("adm", "pw"))
    assert resp.status_code == 200
    assert "Admin Dashboard" in resp.text
    assert "Profile" in resp.text


def test_role_dashboards_exist():
    for path, title, role in [
        ("/core/support", "Support Dashboard", "support"),
        ("/core/distributor", "Distributor Dashboard", "distributor"),
        ("/core/partner", "Partner Dashboard", "partner"),
        ("/core/company", "Company Dashboard", "company"),
        ("/core/enduser", "End User Dashboard", "enduser"),
    ]:
        create_user_with_role(role, role)
        resp = client.get(path, auth=(role, "pw"))
        assert resp.status_code == 200
        assert title in resp.text


def test_cookie_authentication():
    create_user_with_role("cookieuser", "admin")
    # simulate node login setting cookie
    token = base64.b64encode(b"cookieuser:pw").decode()
    resp = client.get("/core/admin", cookies={"auth": token})
    assert resp.status_code == 200


@pytest.mark.parametrize(
    "path,allowed",
    [
        ("/core/admin", "admin"),
        ("/core/support", "support"),
        ("/core/distributor", "distributor"),
        ("/core/partner", "partner"),
        ("/core/company", "company"),
        ("/core/enduser", "enduser"),
    ],
)
def test_forbidden_for_other_roles(path: str, allowed: str):
    roles = ["admin", "support", "distributor", "partner", "company", "enduser"]
    for role in roles:
        create_user_with_role(role, role)

    for role in roles:
        resp = client.get(path, auth=(role, "pw"))
        if role == allowed:
            assert resp.status_code == 200
        else:
            assert resp.status_code == 403
