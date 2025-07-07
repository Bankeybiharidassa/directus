from fastapi.testclient import TestClient
from backend.main import app
from backend.services import acme

client = TestClient(app)


def test_request_certificate(monkeypatch):
    called = {}

    def fake_request(hostnames, email, staging=False):
        called['args'] = (hostnames, email, staging)
        return {'status': 'ok'}

    monkeypatch.setattr(acme, 'request_certificate', fake_request)
    resp = client.post('/certificates/request', json={
        'hostnames': ['example.com'],
        'email': 'admin@example.com'
    })
    assert resp.status_code == 200
    assert called['args'][0] == ['example.com']
    assert called['args'][1] == 'admin@example.com'
