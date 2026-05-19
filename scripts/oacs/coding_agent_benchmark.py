from __future__ import annotations

import json
import os
import re
import resource
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import argparse
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class CodingAgentRecord:
    mode: str
    task_id: str
    category: str
    agent: str
    model: str
    exit_code: int
    task_success: bool
    patch_applies: bool
    tests_pass: bool
    file_checks_pass: bool
    hallucinated_file_refs: int
    acs_calls_count: int
    model_calls_count: int
    repair_turns_est: int
    oacs_request_count: int
    oacs_skip_count: int
    oacs_inject_count: int
    oacs_injected_chars: int
    oacs_estimated_tokens: int
    oacs_status_cache_hits: int
    oacs_cli_latency_ms: float
    latency_total_ms: float
    process_cpu_ms: float
    max_rss_mb: float
    context_chars: int
    prompt_tokens_est: int
    completion_tokens_est: int
    repair_loop_enabled: bool
    turns_count: int
    stdout_preview: str
    stderr_preview: str
    workdir: str


def run_coding_agent_benchmark(
    *,
    tasks_path: str,
    output_dir: str,
    modes: list[str],
    limit: int,
    agent: str,
    model: str,
    direct_base_url: str,
    oacs_base_url: str,
    oacs_config: str,
    keep_workdirs: bool,
    timeout: int,
    repair_loop: bool = False,
) -> dict[str, str]:
    tasks = _load_tasks(Path(tasks_path))
    if limit > 0:
        tasks = tasks[:limit]
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    run_root = output / f"coding_agent_oacs_{int(time.time())}"
    run_root.mkdir(parents=True, exist_ok=True)

    server: subprocess.Popen[str] | None = None
    if any(mode == "aider_oacs_backend" for mode in modes):
        server = _start_oacs_backend(oacs_config=oacs_config, base_url=oacs_base_url, run_root=run_root)

    records: list[CodingAgentRecord] = []
    try:
        for mode in modes:
            for task in tasks:
                records.append(
                    _run_task(
                        task=task,
                        mode=mode,
                        agent=agent,
                        model=model,
                        direct_base_url=direct_base_url,
                        oacs_base_url=oacs_base_url,
                        run_root=run_root,
                        keep_workdirs=keep_workdirs,
                        timeout=timeout,
                        repair_loop=repair_loop,
                    )
                )
    finally:
        if server is not None:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=10)

    stamp = int(time.time())
    json_path = output / f"coding_agent_oacs_{stamp}.json"
    md_path = output / f"coding_agent_oacs_{stamp}.md"
    _write_evidence_json(
        json_path,
        metadata=_evidence_metadata(
            command=sys.argv,
            model=model,
            dataset_path=tasks_path,
            extra={
                "agent": agent,
                "modes": modes,
                "limit": limit,
                "direct_base_url": direct_base_url,
                "oacs_base_url": oacs_base_url,
                "oacs_config": oacs_config,
                "timeout": timeout,
                "repair_loop": repair_loop,
            },
        ),
        records=[asdict(record) for record in records],
    )
    md_path.write_text(_markdown(records), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path), "run_root": str(run_root)}


def _evidence_metadata(*, command: list[str], model: str, dataset_path: str, extra: dict[str, Any]) -> dict[str, Any]:
    return {
        "command": command,
        "model": model,
        "dataset_path": dataset_path,
        "timestamp": int(time.time()),
        "cwd": str(Path.cwd()),
        "git_commit": _git_commit(),
        "extra": extra,
    }


def _write_evidence_json(path: Path, *, metadata: dict[str, Any], records: list[dict[str, Any]]) -> None:
    path.write_text(
        json.dumps({"metadata": metadata, "records": records}, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def _git_commit() -> str | None:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=_repo_root(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_tasks(path: Path) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        task = json.loads(line)
        for key in ("id", "category", "files"):
            if key not in task:
                raise ValueError(f"{path}:{line_no}: missing required key {key!r}")
        if "prompt" not in task and "turns" not in task:
            raise ValueError(f"{path}:{line_no}: missing required key 'prompt' or 'turns'")
        tasks.append(task)
    return tasks


def _run_task(
    *,
    task: dict[str, Any],
    mode: str,
    agent: str,
    model: str,
    direct_base_url: str,
    oacs_base_url: str,
    run_root: Path,
    keep_workdirs: bool,
    timeout: int,
    repair_loop: bool,
) -> CodingAgentRecord:
    if "turns" in task:
        return _run_multiturn_task(
            task=task,
            mode=mode,
            agent=agent,
            model=model,
            direct_base_url=direct_base_url,
            oacs_base_url=oacs_base_url,
            run_root=run_root,
            keep_workdirs=keep_workdirs,
            timeout=timeout,
            repair_loop=repair_loop,
        )
    if agent != "aider":
        raise ValueError(f"unsupported agent: {agent}")
    task_dir = run_root / mode / str(task["id"])
    if task_dir.exists():
        shutil.rmtree(task_dir)
    task_dir.mkdir(parents=True)
    for rel_path, content in dict(task["files"]).items():
        path = task_dir / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(content), encoding="utf-8")

    prompt = _prompt_for_mode(task, mode, task_dir)
    context_chars = len(prompt) + sum(len(str(content)) for content in dict(task["files"]).values())
    base_url = oacs_base_url if mode == "aider_oacs_backend" else direct_base_url
    llm_history = (task_dir / ".aider.llm.history").resolve()
    args = _aider_command(
        mode=mode,
        model=model,
        base_url=base_url,
        timeout=timeout,
        llm_history=llm_history,
        prompt=prompt,
        task_dir=task_dir,
        run_root=run_root,
        repair_loop=repair_loop,
        test_command=str(task.get("test_command", "")).strip(),
    )
    oacs_log_file = task_dir / ".oacs_hook.jsonl"
    proc_env = {**os.environ, "AIDER_ANALYTICS_DISABLE": "true"}
    if _mode_uses_cursor_provider(mode, model) or _mode_uses_oacs(mode):
        fork_path = Path(os.environ.get("AIDER_OACS_FORK_PATH", str(_repo_root()))).resolve()
        proc_env["PYTHONPATH"] = str(fork_path)
    args.extend(_agent_files(task))

    perf_before = _perf_snapshot(children=True)
    started = time.perf_counter()
    timed_out = False
    try:
        proc = subprocess.run(
            args,
            cwd=task_dir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout + 30,
            env=proc_env,
        )
        exit_code = int(proc.returncode)
        stdout = proc.stdout
        stderr = proc.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        exit_code = -9
        stdout = _decode_timeout_output(exc.stdout)
        stderr = _decode_timeout_output(exc.stderr) + f"\nTIMEOUT after {timeout + 30}s"
    latency_ms = (time.perf_counter() - started) * 1000
    perf_after = _perf_snapshot(children=True)

    tests_pass = False if timed_out else _run_test_command(task, task_dir, timeout=timeout)
    file_checks_pass = _file_checks_pass(task, task_dir)
    patch_applies = _files_changed(task, task_dir)
    combined_output = stdout + "\n" + stderr
    hallucinated = _hallucinated_file_refs(combined_output, task)
    prompt_tokens, completion_tokens = _token_estimates(llm_history, combined_output)
    model_calls = _model_calls_count(llm_history)
    oacs_stats = _oacs_log_stats(oacs_log_file) if _mode_uses_oacs(mode) else {}
    success = exit_code == 0 and patch_applies and tests_pass and file_checks_pass

    if not keep_workdirs:
        shutil.rmtree(task_dir, ignore_errors=True)

    return CodingAgentRecord(
        mode=mode,
        task_id=str(task["id"]),
        category=str(task["category"]),
        agent=agent,
        model=model,
        exit_code=exit_code,
        task_success=success,
        patch_applies=patch_applies,
        tests_pass=tests_pass,
        file_checks_pass=file_checks_pass,
        hallucinated_file_refs=hallucinated,
        acs_calls_count=int(oacs_stats.get("acs_calls_count", 0)) if _mode_uses_oacs(mode) else prompt.count("acs "),
        model_calls_count=model_calls,
        repair_turns_est=max(0, model_calls - 1),
        oacs_request_count=int(oacs_stats.get("oacs_request_count", 0)),
        oacs_skip_count=int(oacs_stats.get("oacs_skip_count", 0)),
        oacs_inject_count=int(oacs_stats.get("oacs_inject_count", 0)),
        oacs_injected_chars=int(oacs_stats.get("oacs_injected_chars", 0)),
        oacs_estimated_tokens=int(oacs_stats.get("oacs_estimated_tokens", 0)),
        oacs_status_cache_hits=int(oacs_stats.get("oacs_status_cache_hits", 0)),
        oacs_cli_latency_ms=float(oacs_stats.get("oacs_cli_latency_ms", 0.0)),
        latency_total_ms=latency_ms,
        process_cpu_ms=max(0.0, perf_after["process_cpu_ms"] - perf_before["process_cpu_ms"]),
        max_rss_mb=perf_after["max_rss_mb"],
        context_chars=context_chars,
        prompt_tokens_est=prompt_tokens or max(1, context_chars // 4),
        completion_tokens_est=completion_tokens,
        repair_loop_enabled=repair_loop,
        turns_count=1,
        stdout_preview=stdout[-1200:],
        stderr_preview=stderr[-1200:],
        workdir=str(task_dir),
    )


def _run_multiturn_task(
    *,
    task: dict[str, Any],
    mode: str,
    agent: str,
    model: str,
    direct_base_url: str,
    oacs_base_url: str,
    run_root: Path,
    keep_workdirs: bool,
    timeout: int,
    repair_loop: bool,
) -> CodingAgentRecord:
    if agent != "aider":
        raise ValueError(f"unsupported agent: {agent}")
    task_dir = run_root / mode / str(task["id"])
    if task_dir.exists():
        shutil.rmtree(task_dir)
    task_dir.mkdir(parents=True)
    for rel_path, content in dict(task["files"]).items():
        path = task_dir / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(content), encoding="utf-8")

    base_url = oacs_base_url if mode == "aider_oacs_backend" else direct_base_url
    oacs_log_file = task_dir / ".oacs_hook.jsonl"
    proc_env = {**os.environ, "AIDER_ANALYTICS_DISABLE": "true"}
    if _mode_uses_cursor_provider(mode, model) or _mode_uses_oacs(mode):
        fork_path = Path(os.environ.get("AIDER_OACS_FORK_PATH", str(_repo_root()))).resolve()
        proc_env["PYTHONPATH"] = str(fork_path)

    total_latency_ms = 0.0
    stdout_parts: list[str] = []
    stderr_parts: list[str] = []
    exit_code = 0
    timed_out = False
    perf_before = _perf_snapshot(children=True)
    for index, turn in enumerate(list(task.get("turns", [])), start=1):
        prompt = str(turn["prompt"]).strip()
        llm_history = (task_dir / f".aider.turn{index}.llm.history").resolve()
        args = _aider_command(
            mode=mode,
            model=model,
            base_url=base_url,
            timeout=timeout,
            llm_history=llm_history,
            prompt=prompt,
            task_dir=task_dir,
            run_root=run_root,
            repair_loop=False,
            test_command="",
        )
        args.extend(_agent_files(task))
        started = time.perf_counter()
        try:
            proc = subprocess.run(
                args,
                cwd=task_dir,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout + 30,
                env=proc_env,
            )
            exit_code = int(proc.returncode)
            stdout_parts.append(proc.stdout)
            stderr_parts.append(proc.stderr)
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            exit_code = -9
            stdout_parts.append(_decode_timeout_output(exc.stdout))
            stderr_parts.append(_decode_timeout_output(exc.stderr) + f"\nTIMEOUT after {timeout + 30}s")
        total_latency_ms += (time.perf_counter() - started) * 1000
        if exit_code != 0 or timed_out:
            break
        if not _file_checks_pass({"checks": turn.get("checks", {})}, task_dir):
            break

    for rel_path, content in dict(task.get("final_files", {})).items():
        path = task_dir / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(content), encoding="utf-8")

    perf_after = _perf_snapshot(children=True)
    tests_pass = False if timed_out else _run_test_command(task, task_dir, timeout=timeout)
    file_checks_pass = _file_checks_pass(task, task_dir)
    patch_applies = _files_changed(task, task_dir)
    combined_output = "\n".join(stdout_parts) + "\n" + "\n".join(stderr_parts)
    hallucinated = _hallucinated_file_refs(combined_output, task)
    prompt_tokens = 0
    completion_tokens = 0
    model_calls = 0
    for history in sorted(task_dir.glob(".aider.turn*.llm.history")):
        turn_prompt, turn_completion = _token_estimates(history, "")
        prompt_tokens += turn_prompt
        completion_tokens += turn_completion
        model_calls += _model_calls_count(history)
    context_chars = sum(len(str(content)) for content in dict(task["files"]).values()) + sum(
        len(str(turn.get("prompt", ""))) for turn in list(task.get("turns", []))
    )
    oacs_stats = _oacs_log_stats(oacs_log_file) if _mode_uses_oacs(mode) else {}
    success = exit_code == 0 and patch_applies and tests_pass and file_checks_pass

    if not keep_workdirs:
        shutil.rmtree(task_dir, ignore_errors=True)

    return CodingAgentRecord(
        mode=mode,
        task_id=str(task["id"]),
        category=str(task["category"]),
        agent=agent,
        model=model,
        exit_code=exit_code,
        task_success=success,
        patch_applies=patch_applies,
        tests_pass=tests_pass,
        file_checks_pass=file_checks_pass,
        hallucinated_file_refs=hallucinated,
        acs_calls_count=int(oacs_stats.get("acs_calls_count", 0)) if _mode_uses_oacs(mode) else 0,
        model_calls_count=model_calls,
        repair_turns_est=max(0, model_calls - len(list(task.get("turns", [])))),
        oacs_request_count=int(oacs_stats.get("oacs_request_count", 0)),
        oacs_skip_count=int(oacs_stats.get("oacs_skip_count", 0)),
        oacs_inject_count=int(oacs_stats.get("oacs_inject_count", 0)),
        oacs_injected_chars=int(oacs_stats.get("oacs_injected_chars", 0)),
        oacs_estimated_tokens=int(oacs_stats.get("oacs_estimated_tokens", 0)),
        oacs_status_cache_hits=int(oacs_stats.get("oacs_status_cache_hits", 0)),
        oacs_cli_latency_ms=float(oacs_stats.get("oacs_cli_latency_ms", 0.0)),
        latency_total_ms=total_latency_ms,
        process_cpu_ms=max(0.0, perf_after["process_cpu_ms"] - perf_before["process_cpu_ms"]),
        max_rss_mb=perf_after["max_rss_mb"],
        context_chars=context_chars,
        prompt_tokens_est=prompt_tokens or max(1, context_chars // 4),
        completion_tokens_est=completion_tokens,
        repair_loop_enabled=repair_loop,
        turns_count=len(list(task.get("turns", []))),
        stdout_preview=combined_output[-1200:],
        stderr_preview="\n".join(stderr_parts)[-1200:],
        workdir=str(task_dir),
    )


def _prompt_for_mode(task: dict[str, Any], mode: str, task_dir: Path) -> str:
    prompt = str(task["prompt"]).strip()
    if mode == "aider_direct":
        return prompt
    if mode == "aider_oacs_prompt":
        return _oacs_instruction() + "\n\nTask:\n" + prompt
    if mode == "aider_oacs_context":
        context = _build_context(task, task_dir)
        return _oacs_instruction() + "\n\nOACS context capsule:\n" + context + "\n\nTask:\n" + prompt
    if mode == "aider_oacs_backend":
        return prompt
    if mode in {"aider_oacs_fork", "aider_cursor_provider", "aider_cursor_oacs"}:
        return prompt
    raise ValueError(f"unsupported mode: {mode}")


def _aider_command(
    *,
    mode: str,
    model: str,
    base_url: str,
    timeout: int,
    llm_history: Path,
    prompt: str,
    task_dir: Path,
    run_root: Path,
    repair_loop: bool,
    test_command: str,
) -> list[str]:
    if _mode_uses_cursor_provider(mode, model) or _mode_uses_oacs(mode):
        command = [
            "uvx",
            "--python",
            "3.12",
            "--from",
            "aider-chat",
            "--with",
            "oacs",
            "python",
            "-m",
            "aider",
        ]
    else:
        command = ["uvx", "--python", "3.12", "--from", "aider-chat", "aider"]

    args = [
        *command,
        "--model",
        model if "/" in model else f"openai/{model}",
        "--edit-format",
        "whole",
        "--map-tokens",
        "0",
        "--no-show-model-warnings",
        "--no-check-model-accepts-settings",
        "--no-auto-commits",
        "--no-git",
        "--no-stream",
        "--yes-always",
        "--timeout",
        str(timeout),
        "--llm-history-file",
        str(llm_history),
    ]
    if not model.startswith("cursor/"):
        args.extend(["--openai-api-base", base_url, "--openai-api-key", "local"])
    if repair_loop:
        if test_command:
            args.extend(["--auto-test", "--test-cmd", _agent_test_command(test_command)])
    if _mode_uses_oacs(mode):
        args.extend(
            [
                "--oacs-context",
                "--oacs-actor",
                "aider-oacs",
                "--oacs-scope",
                "project",
                "--oacs-budget",
                "800",
                "--oacs-log-file",
                str((task_dir / ".oacs_hook.jsonl").resolve()),
                "--oacs-memory-limit",
                "3",
                "--oacs-max-injected-chars",
                "1800",
                "--oacs-max-injected-tokens-estimate",
                "450",
            ]
        )
    args.extend(["--message", prompt])
    return args


def _mode_uses_cursor_provider(mode: str, model: str) -> bool:
    return model.startswith("cursor/") or mode in {"aider_cursor_provider", "aider_cursor_oacs"}


def _mode_uses_oacs(mode: str) -> bool:
    return mode in {"aider_oacs_fork", "aider_cursor_oacs"}


def _oacs_instruction() -> str:
    return (
        "Use OACS discipline: first use only relevant project context, keep policy constraints before context, "
        "avoid broad file scanning, preserve evidence in the changed files/tests, and do not expose hidden "
        "runtime traces in user-facing output."
    )


def _build_context(task: dict[str, Any], task_dir: Path) -> str:
    acs_bin = shutil.which("acs")
    if not acs_bin:
        return json.dumps({"status": "acs_missing"}, ensure_ascii=True)
    try:
        proc = subprocess.run(
            [acs_bin, "context", "build", "--help"],
            cwd=task_dir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return json.dumps({"status": "acs_error", "error": str(exc)}, ensure_ascii=True)
    return json.dumps(
        {
            "status": "thin_wrapper",
            "note": "Current harness records the available acs context interface and injects task-local relevant facts.",
            "acs_context_build_help_available": proc.returncode == 0,
            "category": task.get("category"),
            "expected_files": sorted(dict(task["files"]).keys()),
            "relevant_memory": task.get("memory", []),
            "policy": task.get("policy", []),
        },
        ensure_ascii=True,
        sort_keys=True,
    )


def _run_test_command(task: dict[str, Any], task_dir: Path, *, timeout: int) -> bool:
    command = str(task.get("test_command", "")).strip()
    if not command:
        return True
    proc = subprocess.run(command, cwd=task_dir, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    return proc.returncode == 0


def _agent_test_command(command: str) -> str:
    stripped = command.strip()
    if stripped.startswith("python3 -m pytest"):
        return stripped.replace("python3", sys.executable, 1)
    if stripped.startswith("python -m pytest"):
        return stripped.replace("python", sys.executable, 1)
    return stripped


def _agent_files(task: dict[str, Any]) -> list[str]:
    files = task.get("agent_files")
    if files is None:
        return sorted(dict(task["files"]).keys())
    return sorted(str(item) for item in files)


def _file_checks_pass(task: dict[str, Any], task_dir: Path) -> bool:
    checks = task.get("checks", {})
    for item in checks.get("file_contains", []):
        path = task_dir / str(item["path"])
        if not path.exists() or str(item["text"]) not in path.read_text(encoding="utf-8"):
            return False
    for item in checks.get("file_not_contains", []):
        path = task_dir / str(item["path"])
        if path.exists() and str(item["text"]) in path.read_text(encoding="utf-8"):
            return False
    return True


def _files_changed(task: dict[str, Any], task_dir: Path) -> bool:
    for rel_path, original in dict(task["files"]).items():
        path = task_dir / rel_path
        if path.exists() and path.read_text(encoding="utf-8") != str(original):
            return True
    return False


def _hallucinated_file_refs(output: str, task: dict[str, Any]) -> int:
    known = set(dict(task["files"]).keys())
    refs = set()
    for token in output.replace("`", " ").replace("'", " ").replace('"', " ").split():
        if any(token.endswith(suffix) for suffix in (".py", ".md", ".toml", ".yaml", ".json")):
            refs.add(token.strip(".,:;()[]{}"))
    return len([ref for ref in refs if ref not in known and not Path(ref).is_absolute()])


def _token_estimates(llm_history: Path, output: str) -> tuple[int, int]:
    token_matches = list(
        re.finditer(r"Tokens:\s*([0-9.]+k?)\s+sent,\s*([0-9.]+k?)\s+received", output, flags=re.IGNORECASE)
    )
    if token_matches:
        token_match = token_matches[-1]
        return _parse_token_count(token_match.group(1)), _parse_token_count(token_match.group(2))
    if not llm_history.exists():
        return 0, 0
    text = llm_history.read_text(encoding="utf-8", errors="ignore")
    return max(1, len(text) // 4), 0


def _model_calls_count(llm_history: Path) -> int:
    if not llm_history.exists():
        return 0
    text = llm_history.read_text(encoding="utf-8", errors="ignore")
    return text.count("TO LLM")


def _parse_token_count(value: str) -> int:
    value = value.strip().lower()
    if value.endswith("k"):
        return int(float(value[:-1]) * 1000)
    return int(float(value))


def _decode_timeout_output(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _oacs_log_stats(path: Path) -> dict[str, float | int]:
    if not path.exists():
        return {}
    stats = {
        "acs_calls_count": 0,
        "oacs_request_count": 0,
        "oacs_skip_count": 0,
        "oacs_inject_count": 0,
        "oacs_injected_chars": 0,
        "oacs_estimated_tokens": 0,
        "oacs_status_cache_hits": 0,
        "oacs_cli_latency_ms": 0.0,
    }
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        event = item.get("event")
        if event == "oacs_request":
            stats["oacs_request_count"] += 1
            if item.get("gate_decision") == "skip":
                stats["oacs_skip_count"] += 1
            if item.get("gate_decision") == "inject":
                stats["oacs_inject_count"] += 1
            stats["oacs_injected_chars"] += int(item.get("injected_oacs_chars") or 0)
            stats["oacs_estimated_tokens"] += int(item.get("estimated_oacs_tokens") or 0)
            if item.get("status_cache_hit"):
                stats["oacs_status_cache_hits"] += 1
        elif event in {"oacs_status", "oacs_context_build", "oacs_memory_query"}:
            stats["acs_calls_count"] += 1
            stats["oacs_cli_latency_ms"] += float(item.get("latency_ms") or 0.0)
    return stats


def _start_oacs_backend(*, oacs_config: str, base_url: str, run_root: Path) -> subprocess.Popen[str]:
    log_path = run_root / "oacs_backend.log"
    proc = subprocess.Popen(
        ["oacs-backend", "serve", "--config", oacs_config],
        cwd=Path.cwd(),
        text=True,
        stdout=log_path.open("w", encoding="utf-8"),
        stderr=subprocess.STDOUT,
    )
    deadline = time.time() + 30
    root_url = base_url[:-3] if base_url.endswith("/v1") else base_url.rstrip("/")
    health_url = root_url + "/health"
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"OACS backend exited early; see {log_path}")
        try:
            with urllib.request.urlopen(health_url, timeout=1) as response:
                if response.status == 200:
                    return proc
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.5)
    proc.terminate()
    raise RuntimeError(f"OACS backend did not become healthy at {health_url}; see {log_path}")


def _perf_snapshot(*, children: bool) -> dict[str, float]:
    who = resource.RUSAGE_CHILDREN if children else resource.RUSAGE_SELF
    usage = resource.getrusage(who)
    max_rss = float(usage.ru_maxrss)
    if os.uname().sysname == "Darwin":
        max_rss_mb = max_rss / (1024 * 1024)
    else:
        max_rss_mb = max_rss / 1024
    return {
        "process_cpu_ms": (usage.ru_utime + usage.ru_stime) * 1000,
        "max_rss_mb": max_rss_mb,
    }


def _markdown(records: list[CodingAgentRecord]) -> str:
    lines = [
        "# Coding Agent OACS Benchmark",
        "",
        "| mode | task | category | success | exit | patch | tests | checks | turns | model_calls | repair_turns | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | completion_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |",
        "| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for record in records:
        lines.append(
            f"| {record.mode} | {record.task_id} | {record.category} | {record.task_success} | {record.exit_code} | "
            f"{record.patch_applies} | {record.tests_pass} | {record.file_checks_pass} | "
            f"{record.turns_count} | {record.model_calls_count} | {record.repair_turns_est} | "
            f"{record.latency_total_ms:.1f} | {record.process_cpu_ms:.1f} | {record.max_rss_mb:.1f} | "
            f"{record.context_chars} | {record.prompt_tokens_est} | {record.completion_tokens_est} | {record.acs_calls_count} | "
            f"{record.oacs_skip_count} | {record.oacs_inject_count} | {record.oacs_estimated_tokens} | "
            f"{record.hallucinated_file_refs} |"
        )
    lines.extend(["", "## Summary", ""])
    for mode in sorted({record.mode for record in records}):
        subset = [record for record in records if record.mode == mode]
        success = sum(1 for record in subset if record.task_success)
        latency = sum(record.latency_total_ms for record in subset) / max(1, len(subset))
        cpu = sum(record.process_cpu_ms for record in subset) / max(1, len(subset))
        context = sum(record.context_chars for record in subset) / max(1, len(subset))
        prompt_tokens = sum(record.prompt_tokens_est for record in subset) / max(1, len(subset))
        completion_tokens = sum(record.completion_tokens_est for record in subset) / max(1, len(subset))
        model_calls = sum(record.model_calls_count for record in subset) / max(1, len(subset))
        acs_calls = sum(record.acs_calls_count for record in subset)
        skip = sum(record.oacs_skip_count for record in subset)
        inject = sum(record.oacs_inject_count for record in subset)
        lines.append(
            f"- `{mode}`: success {success}/{len(subset)}, avg latency {latency:.1f} ms, "
            f"avg cpu {cpu:.1f} ms, avg context chars {context:.1f}, "
            f"avg prompt tokens {prompt_tokens:.1f}, avg completion tokens {completion_tokens:.1f}, "
            f"avg model calls {model_calls:.1f}, "
            f"acs calls {acs_calls}, OACS skip/inject {skip}/{inject}"
        )
    return "\n".join(lines) + "\n"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Aider OACS coding-agent benchmark fixtures.")
    parser.add_argument("--tasks-path", default="benchmarks/oacs/coding_agent_oacs_tasks.jsonl")
    parser.add_argument("--output-dir", default="benchmark_results/oacs_experiments")
    parser.add_argument(
        "--modes",
        default="aider_direct,aider_oacs_fork",
        help="Comma-separated modes, for example aider_direct,aider_oacs_fork.",
    )
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--agent", default="aider")
    parser.add_argument("--model", default="cursor/composer-2.5")
    parser.add_argument("--direct-base-url", default="http://127.0.0.1:11434/v1")
    parser.add_argument("--oacs-base-url", default="http://127.0.0.1:8080/v1")
    parser.add_argument("--oacs-config", default="config/ollama_agent.yaml")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--keep-workdirs", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--repair-loop", action=argparse.BooleanOptionalAction, default=False)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    paths = run_coding_agent_benchmark(
        tasks_path=args.tasks_path,
        output_dir=args.output_dir,
        modes=[item.strip() for item in args.modes.split(",") if item.strip()],
        limit=args.limit,
        agent=args.agent,
        model=args.model,
        direct_base_url=args.direct_base_url,
        oacs_base_url=args.oacs_base_url,
        oacs_config=args.oacs_config,
        keep_workdirs=args.keep_workdirs,
        timeout=args.timeout,
        repair_loop=args.repair_loop,
    )
    print(f"Wrote {paths['json']} and {paths['markdown']}")
    print(f"Workdirs: {paths['run_root']}")


if __name__ == "__main__":
    main()
