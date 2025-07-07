from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_case_crud_and_search():
    # create cases in separate namespaces
    r1 = client.post(
        "/cases/",
        params={"title": "Issue A", "description": "broken", "namespace": "ns1"},
    )
    assert r1.status_code == 200
    r2 = client.post(
        "/cases/",
        params={"title": "Issue B", "description": "error", "namespace": "ns2"},
    )
    assert r2.status_code == 200

    list_resp = client.get("/cases/")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 2

    search_ns1 = client.get(
        "/cases/search", params={"q": "Issue", "namespace": "ns1"}
    )
    assert search_ns1.status_code == 200
    results = search_ns1.json()
    assert all(c["namespace"] == "ns1" for c in results)

    search_all = client.get("/cases/search", params={"q": "Issue"})
    assert len(search_all.json()) == 2
