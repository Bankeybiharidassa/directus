from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def _make_admin():
    user_resp = client.post("/users/", params={"username": "admin", "password": "pw"})
    user_id = user_resp.json()["id"]
    role_resp = client.post("/roles/", params={"name": "admin"})
    role_id = role_resp.json()["id"]
    client.post(f"/roles/{role_id}/assign/{user_id}")
    return ("admin", "pw")


def test_log_export():
    auth = _make_admin()
    resp = client.get("/core/log/export", auth=auth)
    assert resp.status_code == 200
    assert resp.json()["status"] == "exported"

def test_config_reload():
    auth = _make_admin()
    resp = client.post("/core/config/reload", auth=auth)
    assert resp.status_code == 200
    assert resp.json()["status"] == "reloaded"

def test_bs_check():
    resp = client.get("/core/check/bs")
    assert resp.status_code == 200
    assert resp.json()["bs"] == "0%"


def test_security_scan_endpoint(monkeypatch):
    auth = _make_admin()

    def fake_scan():
        return {"packages": {"pkg": {"version": "1", "vulns": []}}, "binaries": {}, "whitebox": {}, "blackbox": {}}

    monkeypatch.setattr("scripts.security_scan.scan_system", fake_scan)
    resp = client.get("/core/security/scan", auth=auth)
    assert resp.status_code == 200
    assert resp.json()["packages"]["pkg"]["version"] == "1"
