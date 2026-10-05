from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Local AI Agent API is running"
    )


def test_chat_success(monkeypatch):
    def fake_run_agent(message: str) -> str:
        return f"Test answer for: {message}"

    monkeypatch.setattr(
        "app.main.run_agent",
        fake_run_agent
    )

    response = client.post(
        "/agent/chat",
        json={"message": "Show my tasks"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Test answer for: Show my tasks"
    }


def test_chat_rejects_empty_message():
    response = client.post(
        "/agent/chat",
        json={"message": ""}
    )

    assert response.status_code == 422


def test_chat_rejects_missing_message():
    response = client.post(
        "/agent/chat",
        json={}
    )

    assert response.status_code == 422


def test_health(monkeypatch):
    def fake_show(model):
        return {"model": model}

    monkeypatch.setattr(
        "app.main.ollama.show",
        fake_show
    )

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "UP"