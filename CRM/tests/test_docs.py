from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_generate_document():
    resp = client.post("/docsgen/generate", params={"name": "report"})
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert len(resp.content) > 0


def test_export_invoice():
    resp = client.get("/docsgen/invoice/export/123")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert len(resp.content) > 0


def test_management_report():
    resp = client.get("/docsgen/report/management")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert len(resp.content) > 0
