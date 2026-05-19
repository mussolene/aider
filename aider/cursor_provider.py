from __future__ import annotations

import os
import subprocess
import time
from types import SimpleNamespace
from typing import Any


def is_cursor_model(model: str) -> bool:
    return model.startswith("cursor/")


def cursor_model_id(model: str) -> str:
    return model.split("/", 1)[1]


def cursor_completion(*, model: str, messages: list[dict[str, Any]], timeout: int) -> Any:
    model_id = cursor_model_id(model)
    if not os.environ.get("CURSOR_API_KEY"):
        raise RuntimeError("CURSOR_API_KEY is required for cursor/<model> Aider provider")

    prompt = _messages_to_prompt(messages)
    started = int(time.time())
    proc = subprocess.run(
        [
            os.environ.get("AIDER_CURSOR_AGENT_BIN", "agent"),
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
        raise RuntimeError(f"Cursor provider failed with exit {proc.returncode}: {proc.stderr[-2000:]}")

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
        content = message.get("content", "")
        if isinstance(content, list):
            content = "\n".join(str(item.get("text", item)) for item in content)
        parts.append(f"\n[{role}]\n{content}")
    parts.append("\n[ASSISTANT]")
    return "\n".join(parts)
