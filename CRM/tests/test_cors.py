from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_cors_headers():
    resp = client.get("/health", headers={"Origin": "http://example.com"})
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") == "*"
