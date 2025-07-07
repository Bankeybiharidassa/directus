from backend.services import sophos_partner, sophos_customer
from unittest import mock


def test_partner_list_tenants_caches_token(monkeypatch):
    calls = []

    def fake_post(url, data, auth, timeout):
        calls.append("token")
        assert data == {"grant_type": "client_credentials"}

        class R:
            def json(self):
                return {"access_token": "p-token"}

            def raise_for_status(self):
                pass

        return R()

    def fake_get(url, headers, timeout):
        calls.append("tenants")
        assert headers["Authorization"] == "Bearer p-token"

        class R:
            def json(self):
                return {"items": [{"id": "t1"}]}

            def raise_for_status(self):
                pass

        return R()

    monkeypatch.setattr(sophos_partner.requests, "post", fake_post)
    monkeypatch.setattr(sophos_partner.requests, "get", fake_get)

    api = sophos_partner.PartnerAPI("id", "secret", base_url="http://x")
    assert api.list_tenants() == [{"id": "t1"}]
    # second call should reuse token
    assert api.list_tenants() == [{"id": "t1"}]
    assert calls == ["token", "tenants", "tenants"]


def test_customer_token_and_alerts(monkeypatch):
    calls = []

    def fake_post(url, data, timeout):
        calls.append("token")
        assert data == {"grant_type": "refresh_token", "refresh_token": "r1"}

        class R:
            def json(self):
                return {"access_token": "c-token"}

            def raise_for_status(self):
                pass

        return R()

    def fake_get(url, headers, timeout):
        calls.append("alerts")
        assert headers["Authorization"] == "Bearer c-token"
        assert headers["X-Tenant-ID"] == "t1"

        class R:
            def json(self):
                return {"items": [{"id": "a1"}]}

            def raise_for_status(self):
                pass

        return R()

    monkeypatch.setattr(sophos_customer.requests, "post", fake_post)
    monkeypatch.setattr(sophos_customer.requests, "get", fake_get)

    api = sophos_customer.CustomerAPI("http://x")
    token = api.get_tenant_token("t1", "r1")
    assert token == "c-token"
    alerts = api.fetch_alerts("t1", token)
    assert alerts == [{"id": "a1"}]
    # requesting token again should hit cache
    assert api.get_tenant_token("t1", "r1") == "c-token"
    assert calls == ["token", "alerts"]
