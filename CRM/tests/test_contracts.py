from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_create_list_and_close_contract():
    resp = client.post("/customers/", params={"name": "Contoso", "contact_email": "c@example.com"})
    customer_id = resp.json()["id"]

    create_resp = client.post("/contracts/", params={"customer_id": customer_id, "description": "SLA"})
    assert create_resp.status_code == 200
    contract_id = create_resp.json()["id"]

    list_resp = client.get("/contracts/")
    assert any(c["id"] == contract_id for c in list_resp.json())

    close_resp = client.post(f"/contracts/{contract_id}/close")
    assert close_resp.status_code == 200
    assert close_resp.json()["status"] == "closed"
