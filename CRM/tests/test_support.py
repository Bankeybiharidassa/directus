from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_remote_support_login():
    # create target user
    u_resp = client.post("/users/", params={"username": "eve", "password": "pw"})
    user_id = u_resp.json()["id"]

    # create support user with role
    sup_resp = client.post("/users/", params={"username": "helper", "password": "pw"})
    sup_id = sup_resp.json()["id"]
    role_resp = client.post("/roles/", params={"name": "support"})
    role_id = role_resp.json()["id"]
    client.post(f"/roles/{role_id}/assign/{sup_id}")

    # authorize remote access by target user
    client.post("/support/authorize", auth=("eve", "pw"))

    # login as target user
    resp = client.post(f"/support/login_as/{user_id}", auth=("helper", "pw"))
    assert resp.status_code == 200
    assert resp.json()["username"] == "eve"

    # revoke and ensure login fails
    client.post("/support/revoke", auth=("eve", "pw"))
    deny = client.post(f"/support/login_as/{user_id}", auth=("helper", "pw"))
    assert deny.status_code == 403
