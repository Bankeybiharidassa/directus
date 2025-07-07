from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_set_and_get_api_config():
    resp = client.post("/config/api", params={"api_key": "key123", "model": "gpt-4"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["model"] == "gpt-4"

    get_resp = client.get("/config/api")
    assert get_resp.status_code == 200
    assert get_resp.json()["model"] == "gpt-4"


def test_list_models():
    resp = client.get("/config/models")
    assert resp.status_code == 200
    assert "gpt-4" in resp.json()
