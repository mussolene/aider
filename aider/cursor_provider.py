from __future__ import annotations

import os
import subprocess
import time
from types import SimpleNamespace
from typing import Any

CURSOR_MODEL_PREFIX = "cursor/"
CURSOR_API_KEY_ENV = "CURSOR_API_KEY"
CURSOR_AGENT_BIN_ENV = "AIDER_CURSOR_AGENT_BIN"
DEFAULT_CURSOR_AGENT_BIN = "agent"
CURSOR_ERROR_TAIL_CHARS = 2000
CURSOR_MAX_INPUT_TOKENS = 200000
CURSOR_MAX_OUTPUT_TOKENS = 16000


def is_cursor_model(model: str) -> bool:
    return model.startswith(CURSOR_MODEL_PREFIX)


def cursor_model_id(model: str) -> str:
    if not is_cursor_model(model):
        raise ValueError(f"Cursor models must use the {CURSOR_MODEL_PREFIX}<model> form")

    model_id = model[len(CURSOR_MODEL_PREFIX) :]
    if not model_id:
        raise ValueError(f"Cursor models must include a model id after {CURSOR_MODEL_PREFIX}")

    return model_id


def cursor_agent_completion(*, model: str, messages: list[dict[str, Any]], timeout: int) -> Any:
    model_id = cursor_model_id(model)
    if not os.environ.get(CURSOR_API_KEY_ENV):
        raise RuntimeError("CURSOR_API_KEY is required for cursor/<model> Aider provider")

    prompt = _messages_to_prompt(messages)
    started = int(time.time())
    proc = subprocess.run(
        [
            os.environ.get(CURSOR_AGENT_BIN_ENV, DEFAULT_CURSOR_AGENT_BIN),
            "--print",
            "--output-format",
            "text",
            "--trust",
            "--mode",
            "ask",
            "--model",
            model_id,
            prompt,
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        env=os.environ.copy(),
    )
    if proc.returncode != 0:
        stderr = _sanitize_cursor_error(proc.stderr[-CURSOR_ERROR_TAIL_CHARS:])
        raise RuntimeError(f"Cursor provider failed with exit {proc.returncode}: {stderr}")

    content = proc.stdout.strip()
    prompt_tokens = max(1, len(prompt) // 4)
    completion_tokens = max(1, len(content) // 4)
    return SimpleNamespace(
        id=f"cursor-{started}",
        model=model,
        choices=[
            SimpleNamespace(
                finish_reason="stop",
                message=SimpleNamespace(content=content, tool_calls=None),
            )
        ],
        usage=SimpleNamespace(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        ),
    )


def _messages_to_prompt(messages: list[dict[str, Any]]) -> str:
    parts: list[str] = [
        "You are acting as the model backend for Aider.",
        "Return only the assistant response Aider requested.",
        "Do not edit files directly and do not run shell commands.",
        "If Aider asks for a file listing or diff, output it exactly in the requested format.",
        "",
        "Conversation:",
    ]
    for message in messages:
        role = str(message.get("role", "user")).upper()
        content = _message_content_to_text(message.get("content", ""))
        parts.append(f"\n[{role}]\n{content}")
    parts.append("\n[ASSISTANT]")
    return "\n".join(parts)


def _message_content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") in (None, "text"):
                    parts.append(str(item.get("text", "")))
                else:
                    parts.append(f"[{item.get('type', 'non_text_content')}]")
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part)

    return str(content)


def _sanitize_cursor_error(stderr: str) -> str:
    api_key = os.environ.get(CURSOR_API_KEY_ENV)
    if api_key:
        stderr = stderr.replace(api_key, "[REDACTED_CURSOR_API_KEY]")
    return stderr
