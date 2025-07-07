from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_create_and_list_assets():
    resp = client.post("/assets/", params={"hostname": "server1", "status": "ok"})
    assert resp.status_code == 200
    asset_id = resp.json()["id"]

    list_resp = client.get("/assets/")
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert any(a["id"] == asset_id for a in data)


def test_add_and_list_vulnerabilities():
    resp = client.post("/assets/", params={"hostname": "server2"})
    asset_id = resp.json()["id"]

    add_resp = client.post(
        f"/assets/{asset_id}/vulnerabilities",
        params={"description": "CVE-1234", "severity": "high"},
    )
    assert add_resp.status_code == 200

    list_resp = client.get(f"/assets/{asset_id}/vulnerabilities")
    assert list_resp.status_code == 200
    assert any(v["description"] == "CVE-1234" for v in list_resp.json())


def test_asset_sync():
    resp = client.post("/assets/sync", params={"source": "all"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "synced"
    assert data["new_assets"] >= 4
    list_resp = client.get("/assets/")
    names = [a["hostname"] for a in list_resp.json()]
    for host in ["sophos1", "sophos2", "tenable1", "tenable2"]:
        assert host in names


def test_asset_sync_invalid_source():
    resp = client.post("/assets/sync", params={"source": "bogus"})
    assert resp.status_code == 400

