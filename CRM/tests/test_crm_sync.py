from fastapi.testclient import TestClient
from backend.main import app
from backend.services import crm_sync
from unittest import mock

client = TestClient(app)


def test_import_from_external(monkeypatch):
    def fake_get(url, timeout):
        if url.endswith('/tenants'):
            class R:
                def json(self):
                    return [{'id': 5, 'name': 'Ext', 'contact_email': 'e@x'}]
                def raise_for_status(self):
                    pass
            return R()
        else:
            class R:
                def json(self):
                    return [{'username': 'extuser'}]
                def raise_for_status(self):
                    pass
            return R()

    monkeypatch.setattr(crm_sync, 'requests', mock.Mock(get=fake_get))
    resp = client.post('/api/crm/sync/import', params={'source_url': 'http://api'})
    assert resp.status_code == 200
    assert resp.json()['imported'] >= 1
