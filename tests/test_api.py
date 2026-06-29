import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_endpoint_returns_answer(monkeypatch):
    class DummyAgent:
        def invoke(self, state):
            return {"messages": [{"content": "mock answer"}]}

    monkeypatch.setattr("main.get_agent", lambda: DummyAgent())

    response = client.post("/ask", json={"message": "hello"})

    assert response.status_code == 200

