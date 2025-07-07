from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_create_and_list_customers():
    response = client.post(
        "/customers/",
        params={
            "name": "ACME",
            "contact_email": "acme@example.com",
            "sophos_api_mode": "partner",
        },
    )
    assert response.status_code == 200

    list_resp = client.get("/customers/")
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert any(c["name"] == "ACME" and c["sophos_api_mode"] == "partner" for c in data)


def test_export_customers_pdf(tmp_path):
    client.post("/customers/", params={"name": "MegaCorp", "contact_email": "m@example.com"})
    resp = client.get("/customers/export")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    pdf_path = tmp_path / "customers.pdf"
    pdf_path.write_bytes(resp.content)
    assert pdf_path.exists() and pdf_path.stat().st_size > 0
