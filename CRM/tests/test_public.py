from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_public_frontpage():
    resp = client.get("/core/frontpage")
    assert resp.status_code == 200
    assert "Welcome to Nucleus CRM" in resp.text
