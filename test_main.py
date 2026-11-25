from unittest.mock import patch
from openai import APITimeoutError
import httpx2

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

def test_ask_timeout():
    with patch("main.OpenAI") as mock_openai:
        fake_client = mock_openai.return_value.__enter__.return_value
        fake_client.chat.completions.create.side_effect = APITimeoutError(
            request=httpx2.Request(
                "POST",
                "https://api.deepseek.com/chat/completions",
            )
        )

        client = TestClient(app)
        response = client.post("/ask", json={"question": "HTTP 是什么？"})

    assert response.status_code == 504
    assert response.json() == {"detail": "模型响应超时，请稍后重试"}