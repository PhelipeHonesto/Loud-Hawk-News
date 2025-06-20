import os
import sys
import types
import pytest
from starlette.testclient import TestClient

# Provide a stub openai module if it's not installed
openai = types.ModuleType("openai")

class ChatCompletion:
    async def acreate(*args, **kwargs):
        raise NotImplementedError

openai.ChatCompletion = ChatCompletion
openai.api_key = None
sys.modules["openai"] = openai

# Ensure API key is set before importing the app
os.environ.setdefault("OPENAI_API_KEY", "test-key")

from app.main import app
import openai  # type: ignore  # noqa: E402


def test_edit_returns_formatted(monkeypatch):
    async def fake_acreate(*args, **kwargs):
        class DummyMessage:
            content = "Mocked body"

        class DummyChoice:
            message = DummyMessage()

        class DummyResp:
            choices = [DummyChoice()]

        return DummyResp()

    monkeypatch.setattr(openai.ChatCompletion, "acreate", fake_acreate)

    payload = {
        "title": "Breaking News",
        "date": "2023-08-01",
        "body": "Some news body.",
        "link": "https://example.com",
    }

    expected = (
        "\U0001F985 Loud Hawk News\n"
        "\U0001F4E2 *Breaking News*\n"
        "\U0001F4C5 2023-08-01\n"
        "Mocked body\n"
        "\U0001F517 [Read more](https://example.com)"
    )

    with TestClient(app) as client:
        response = client.post("/edit", json=payload)

    assert response.status_code == 200
    assert response.json() == {"text": expected}
