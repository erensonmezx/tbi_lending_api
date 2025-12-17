from fastapi.testclient import TestClient
from app.main import create_app

def test_health():
    client = TestClient(create_app())
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert "x-correlation-id" in r.headers

def test_create_and_get_application():
    client = TestClient(create_app())
    payload = {
        "customer_id": "c1",
        "merchant_id": "m1",
        "amount": 10000,
        "currency": "eur",
        "term_months": 12
    }
    r = client.post("/applications", json=payload, headers={"x-correlation-id": "test-cid"})
    assert r.status_code == 201
    data = r.json()
    assert data["status"] == "CREATED"
    assert r.headers["x-correlation-id"] == "test-cid"

    app_id = data["id"]
    r2 = client.get(f"/applications/{app_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == app_id

def test_get_missing_returns_404_error_shape():
    client = TestClient(create_app())
    r = client.get("/applications/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
    body = r.json()
    assert body["error_code"] == "NOT_FOUND"
    assert "correlation_id" in body
