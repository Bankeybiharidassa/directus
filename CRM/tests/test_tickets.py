from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_create_and_list_tickets():
    resp = client.post("/tickets/", params={"title": "Issue", "description": "broken"})
    assert resp.status_code == 200
    ticket_id = resp.json()["id"]

    list_resp = client.get("/tickets/")
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert any(t["id"] == ticket_id for t in data)


def test_close_ticket():
    resp = client.post("/tickets/", params={"title": "CloseMe", "description": "x"})
    assert resp.status_code == 200
    ticket_id = resp.json()["id"]

    close_resp = client.post(f"/tickets/{ticket_id}/close")
    assert close_resp.status_code == 200
    assert close_resp.json()["status"] == "closed"
