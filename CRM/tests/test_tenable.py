from fastapi.testclient import TestClient
from backend.main import app
from backend.services import tenable

client = TestClient(app)


def test_fetch_assets_from_api(monkeypatch):
    def fake_get(url, headers, timeout):
        assert url == "http://api" and headers["Authorization"] == "Bearer tok"

        class R:
            def json(self):
                return [{"hostname": "host1"}]

            def raise_for_status(self):
                pass

        return R()

    monkeypatch.setenv("TENABLE_URL", "http://api")
    monkeypatch.setenv("TENABLE_TOKEN", "tok")
    monkeypatch.setattr(tenable.requests, "get", fake_get)
    assets = tenable.fetch_assets()
    assert assets == [{"hostname": "host1"}]


def test_tenable_endpoint(monkeypatch):
    monkeypatch.setattr(tenable, "fetch_assets", lambda: [{"hostname": "h"}])
    resp = client.get("/tenable/assets")
    assert resp.status_code == 200
    assert resp.json() == [{"hostname": "h"}]
