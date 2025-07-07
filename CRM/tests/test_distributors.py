from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_create_and_list_distributors():
    resp = client.post("/distributors/", params={"name": "MainDist"})
    assert resp.status_code == 200
    dist_id = resp.json()["id"]

    list_resp = client.get("/distributors/")
    assert any(d["id"] == dist_id for d in list_resp.json())
