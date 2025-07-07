from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_crm_dmarc_report_json():
    client.post("/customers/", params={"name": "Acme", "contact_email": "a@b.c"})
    resp = client.get("/api/crm/dmarc/1/example.com")
    assert resp.status_code == 200
    data = resp.json()
    assert data["tenant_id"] == 1
    assert data["domain"] == "example.com"


def test_crm_dmarc_report_csv():
    client.post("/customers/", params={"name": "Beta", "contact_email": "b@c.d"})
    resp = client.get("/api/crm/dmarc/2/example.com?fmt=csv")
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]
    assert "example.com" in resp.text


def test_customer_creation_seeds_domain():
    resp = client.post("/customers/", params={"name": "Seed", "contact_email": "s@t.u"})
    assert resp.status_code == 200
    list_resp = client.get("/api/crm/domains/1")
    assert list_resp.status_code == 200
    domains = list_resp.json()
    assert any(d["domain"].startswith("seed") for d in domains)


def test_crm_dmarc_rbac():
    client.post("/customers/", params={"name": "One", "contact_email": "o@x.y"})
    client.post("/customers/", params={"name": "Two", "contact_email": "t@x.y"})
    resp = client.get(
        "/api/crm/dmarc/1/example.com",
        headers={"X-CRM-Tenant": "2"},
    )
    assert resp.status_code == 403


def test_crm_dmarc_abuse_and_update():
    client.post("/customers/", params={"name": "Foo", "contact_email": "f@e.c"})
    resp = client.post(
        "/api/crm/dmarc/abuse",
        params={"tenant_id": 1, "domain": "ex.com"},
        json={"ip": "1.2.3.4", "contact": "owner"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "sent"
    resp = client.put("/api/crm/dmarc/abuse/1", params={"status": "responded"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "responded"
