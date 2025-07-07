from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_api_root():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Nucleus CRM backend"
    assert data["docs"] == "/docs"
