from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_service_status():
    resp = client.get('/core/status')
    assert resp.status_code == 200
    body = resp.json()
    assert 'database' in body
    assert 'node_auth' in body
