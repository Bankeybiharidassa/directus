from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_create_list_and_reassign_partner():
    dist = client.post("/distributors/", params={"name": "Dist"})
    dist_id = dist.json()["id"]
    resp = client.post("/partners/", params={"name": "PartnerA", "distributor_id": dist_id})
    assert resp.status_code == 200
    partner_id = resp.json()["id"]

    list_resp = client.get("/partners/")
    assert any(p["id"] == partner_id for p in list_resp.json())

    reassign_resp = client.post(f"/partners/{partner_id}/reassign", params={"distributor_id": dist_id})
    assert reassign_resp.status_code == 200
    assert reassign_resp.json()["distributor_id"] == dist_id
