from aider.cursor_provider import _messages_to_prompt, cursor_model_id, is_cursor_model


def test_cursor_model_helpers():
    assert is_cursor_model("cursor/composer-2.5")
    assert not is_cursor_model("openai/gpt-5")
    assert cursor_model_id("cursor/composer-2.5") == "composer-2.5"


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
