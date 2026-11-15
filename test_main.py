from fastapi.testclient import TestClient
from main import app


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_case_requires_error():
    client = TestClient(app)
    response = client.post("/cases", json={"title": "接口连不上"})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "error"]