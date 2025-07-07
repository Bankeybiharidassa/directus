from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_add_and_list_domains():
    client.post("/customers/", params={"name": "Gamma", "contact_email": "g@h.i"})
    resp = client.post(
        "/api/crm/domains/",
        params={"tenant_id": 1},
        json={
            "domain": "gamma.com",
            "imap_host": "imap.example.com",
            "imap_user": "u",
            "smtp_host": "smtp.example.com",
            "smtp_user": "s",
        },
    )
    assert resp.status_code == 200
    domain_id = resp.json()["id"]

    list_resp = client.get("/api/crm/domains/1")
    assert list_resp.status_code == 200
    domains = list_resp.json()
    assert any(
        d["id"] == domain_id
        and d["imap_host"] == "imap.example.com"
        and d["smtp_host"] == "smtp.example.com"
        for d in domains
    )
