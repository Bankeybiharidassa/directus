from fastapi.testclient import TestClient
from backend.main import app
from backend.services import dmarc
from unittest import mock

client = TestClient(app)


def test_get_report():
    resp = client.get("/dmarc/example.com")
    assert resp.status_code == 200
    data = resp.json()
    assert data["domain"] == "example.com"
    assert "pass" in data
    assert "fail" in data


def test_abuse_webhook(monkeypatch):
    called = {}

    def fake_post(url, json, timeout):
        called['url'] = url
        called['json'] = json

        class Resp:
            status_code = 200

        return Resp()

    monkeypatch.setattr(dmarc, 'requests', mock.Mock(post=fake_post))
    monkeypatch.setenv('DMARC_ABUSE_WEBHOOK', 'http://webhook')
    with TestClient(app) as client:
        client.post(
            "/api/crm/dmarc/abuse",
            params={'tenant_id': 1, 'domain': 'ex.com'},
            json={'ip': '1.2.3.4', 'contact': 'owner'},
        )
    assert called['url'] == 'http://webhook'
    assert called['json']['domain'] == 'ex.com'
