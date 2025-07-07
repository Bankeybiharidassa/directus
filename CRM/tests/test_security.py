from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_ip_cidr_and_fqdn_whitelist():
    # single IP
    client.post("/whitelisted_ips/", params={"entry": "127.0.0.1"})
    # CIDR block
    client.post("/whitelisted_ips/", params={"entry": "10.0.0.0/24"})
    # FQDN wildcard
    client.post("/whitelisted_ips/", params={"entry": "*.example.com"})

    client.post("/users/", params={"username": "ipuser", "password": "secret"})

    # exact IP match
    allowed_ip = client.get(
        "/users/me",
        auth=("ipuser", "secret"),
        headers={"X-Client-IP": "127.0.0.1"},
    )
    assert allowed_ip.status_code == 200

    # CIDR match
    allowed_cidr = client.get(
        "/users/me",
        auth=("ipuser", "secret"),
        headers={"X-Client-IP": "10.0.0.42"},
    )
    assert allowed_cidr.status_code == 200

    # FQDN wildcard match
    allowed_fqdn = client.get(
        "/users/me",
        auth=("ipuser", "secret"),
        headers={"X-Client-IP": "8.8.8.8", "X-Client-FQDN": "api.example.com"},
    )
    assert allowed_fqdn.status_code == 200

    denied = client.get(
        "/users/me",
        auth=("ipuser", "secret"),
        headers={"X-Client-IP": "8.8.8.8", "X-Client-FQDN": "bad.com"},
    )
    assert denied.status_code == 401

