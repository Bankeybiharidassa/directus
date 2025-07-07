from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_create_list_and_publish_page():
    resp = client.post("/pages/", params={"slug": "welcome", "content": "hi"})
    assert resp.status_code == 200
    page_id = resp.json()["id"]

    list_resp = client.get("/pages/")
    assert any(p["id"] == page_id for p in list_resp.json())

    publish_resp = client.post(f"/pages/{page_id}/publish")
    assert publish_resp.status_code == 200
    assert publish_resp.json()["published"] is True
