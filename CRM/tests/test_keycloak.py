from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_set_and_get_keycloak():
    resp = client.post(
        "/keycloak/",
        params={
            "url": "https://kc.example.com",
            "realm": "nucleus",
            "client_id": "crm",
            "client_secret": "secret",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["url"] == "https://kc.example.com"

    get_resp = client.get("/keycloak/")
    assert get_resp.status_code == 200
    assert get_resp.json()["client_id"] == "crm"


def test_get_keycloak_empty():
    resp = client.get("/keycloak/")
    assert resp.status_code == 200
    assert resp.json() == {}


def test_overwrite_keycloak():
    client.post(
        "/keycloak/",
        params={
            "url": "https://kc.example.com",
            "realm": "nucleus",
            "client_id": "crm",
            "client_secret": "secret",
        },
    )

    resp = client.post(
        "/keycloak/",
        params={
            "url": "https://new.example.com",
            "realm": "newrealm",
            "client_id": "crm2",
            "client_secret": "s2",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["url"] == "https://new.example.com"
    get_resp = client.get("/keycloak/")
    assert get_resp.json()["realm"] == "newrealm"
