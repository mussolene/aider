from types import SimpleNamespace

import pytest

from aider.cursor_provider import (
    _messages_to_prompt,
    cursor_agent_completion,
    cursor_model_id,
    is_cursor_model,
)


def test_cursor_model_helpers():
    assert is_cursor_model("cursor/composer-2.5")
    assert not is_cursor_model("openai/gpt-5")
    assert cursor_model_id("cursor/composer-2.5") == "composer-2.5"


def test_cursor_model_id_rejects_invalid_names():
    with pytest.raises(ValueError):
        cursor_model_id("openai/gpt-5")

    with pytest.raises(ValueError):
        cursor_model_id("cursor/")


def test_messages_to_prompt_preserves_roles_and_content():
    prompt = _messages_to_prompt(
        [
            {"role": "system", "content": "Use Aider format."},
            {"role": "user", "content": "Edit file.py"},
        ]
    )

    assert "Do not edit files directly" in prompt
    assert "[SYSTEM]\nUse Aider format." in prompt
    assert "[USER]\nEdit file.py" in prompt
    assert prompt.endswith("[ASSISTANT]")


def test_messages_to_prompt_handles_structured_content():
    prompt = _messages_to_prompt(
        [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Edit file.py"},
                    {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}},
                ],
            },
        ]
    )

    assert "Edit file.py" in prompt
    assert "[image_url]" in prompt


def test_cursor_agent_completion_requires_api_key(monkeypatch):
    monkeypatch.delenv("CURSOR_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="CURSOR_API_KEY"):
        cursor_agent_completion(model="cursor/composer-2.5", messages=[], timeout=1)


def test_cursor_agent_completion_invokes_cursor_agent(monkeypatch):
    calls = []
    monkeypatch.setenv("CURSOR_API_KEY", "test-key")
    monkeypatch.setenv("AIDER_CURSOR_AGENT_BIN", "cursor-agent-test")

    def fake_run(cmd, **kwargs):
        calls.append((cmd, kwargs))
        return SimpleNamespace(returncode=0, stdout="assistant response\n", stderr="")

    monkeypatch.setattr("subprocess.run", fake_run)

    res = cursor_agent_completion(
        model="cursor/composer-2.5",
        messages=[{"role": "user", "content": "Hello"}],
        timeout=30,
    )

    cmd, kwargs = calls[0]
    assert cmd[:7] == [
        "cursor-agent-test",
        "--print",
        "--output-format",
        "text",
        "--trust",
        "--mode",
        "ask",
    ]
    assert "--model" in cmd
    assert "composer-2.5" in cmd
    assert "test-key" not in cmd
    assert kwargs["timeout"] == 30
    assert kwargs["env"]["CURSOR_API_KEY"] == "test-key"
    assert res.choices[0].message.content == "assistant response"
    assert res.usage.total_tokens >= res.usage.prompt_tokens


def test_cursor_agent_completion_sanitizes_stderr(monkeypatch):
    monkeypatch.setenv("CURSOR_API_KEY", "secret-key")

    def fake_run(cmd, **kwargs):
        return SimpleNamespace(returncode=1, stdout="", stderr="failed secret-key")

    monkeypatch.setattr("subprocess.run", fake_run)

    with pytest.raises(RuntimeError) as exc:
        cursor_agent_completion(model="cursor/composer-2.5", messages=[], timeout=30)

    assert "secret-key" not in str(exc.value)
    assert "[REDACTED_CURSOR_API_KEY]" in str(exc.value)
