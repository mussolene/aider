from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


MEMORY_TERMS = (
    "remember",
    "history",
    "decision",
    "convention",
    "previous",
    "agreed",
    "policy",
    "why",
    "context",
    "memory",
    "deprecated",
)
CONTEXT_TERMS = (
    "architecture",
    "refactor",
    "debug",
    "root cause",
    "multi-file",
    "multiple files",
    "large project",
    "project-level",
    "where is",
    "find where",
    "integration",
)
SIMPLE_EDIT_TERMS = (
    "edit",
    "update",
    "implement",
    "fix",
    "add",
    "change",
)
POLICY_TERMS = ("policy", "permission", "secret", "export", "private", "passphrase")
STATUS_CACHE_TTL_SECONDS = 60.0


@dataclass(slots=True)
class OACSContextConfig:
    enabled: bool = False
    actor: str = "aider-oacs"
    scope: str = "project"
    budget: int = 800
    command: str = "acs"
    log_file: str | None = None
    memory_limit: int = 3
    strict: bool = False
    max_injected_chars: int = 1800
    max_injected_tokens_estimate: int = 450
    evidence_strict: bool = False
    status_cache_ttl: float = STATUS_CACHE_TTL_SECONDS


@dataclass(slots=True)
class GateDecision:
    action: str
    reason: str
    use_status: bool = False
    use_memory: bool = False
    use_context: bool = False


class OACSContextProvider:
    def __init__(self, config: OACSContextConfig) -> None:
        self.config = config
        self._status_cache: dict[str, Any] | None = None
        self._status_cache_expires_at = 0.0
        self._services_cache: dict[bool, Any] = {}

    def build_message(
        self,
        *,
        intent: str,
        task_text: str,
        git_root: str | None,
        visible_files: set[str] | None = None,
        repo_map_chars: int = 0,
    ) -> dict[str, str] | None:
        request_id = f"oacs_{int(time.time() * 1000)}"
        visible_files = visible_files or set()
        if not self.config.enabled:
            self._log_request(
                request_id=request_id,
                intent=intent,
                decision=GateDecision("skip", "disabled"),
                status_cache_hit=False,
            )
            return None

        decision = self._gate(intent=intent, task_text=task_text, visible_files=visible_files, repo_map_chars=repo_map_chars)
        if decision.action == "skip":
            self._log_request(
                request_id=request_id,
                intent=intent,
                decision=decision,
                status_cache_hit=False,
            )
            return None

        status: dict[str, Any] = {}
        status_cache_hit = False
        if decision.use_status:
            status, status_cache_hit = self._status(git_root=git_root, request_id=request_id)

        capsule: dict[str, Any] | None = None
        if decision.use_context:
            capsule = self._context_build(
                intent=intent,
                git_root=git_root,
                request_id=request_id,
            )
            if capsule is not None and not self._has_substantive_capsule(capsule) and not decision.use_status:
                capsule = None

        memories: list[dict[str, Any]] = []
        if decision.use_memory and self.config.memory_limit > 0:
            memories = self._memory_query(
                query=task_text[:1000],
                git_root=git_root,
                request_id=request_id,
            )

        if capsule is None and not memories and not status:
            self._log_request(
                request_id=request_id,
                intent=intent,
                decision=GateDecision("skip", f"{decision.reason}; no_oacs_payload"),
                status_cache_hit=status_cache_hit,
            )
            return None

        content = self._format_capsule(
            capsule or {},
            intent=intent,
            decision=decision,
            status=status,
            memories=memories[: max(0, self.config.memory_limit)],
            visible_files=visible_files,
        )
        original_chars = len(content)
        content = self._limit_text(content)
        injected_chars = len(content)
        self._log_request(
            request_id=request_id,
            intent=intent,
            decision=decision,
            status_cache_hit=status_cache_hit,
            original_oacs_chars=original_chars,
            injected_oacs_chars=injected_chars,
            estimated_oacs_tokens=max(1, injected_chars // 4),
            memory_entries_used=len(memories[: max(0, self.config.memory_limit)]),
            context_entries_used=1 if capsule else 0,
            dedup_removed_chars=max(0, original_chars - injected_chars),
        )
        return {
            "role": "user",
            "content": content,
        }

    def _gate(self, *, intent: str, task_text: str, visible_files: set[str], repo_map_chars: int) -> GateDecision:
        text = task_text.lower()
        visible_count = len(visible_files)
        memory_hit = _external_memory_signal(text) or intent == "project_memory"
        policy_hit = _contains_any(text, POLICY_TERMS) or intent == "policy"
        context_hit = _contains_any(text, CONTEXT_TERMS) or intent in {"debug", "architecture", "refactor"}
        file_refs = _file_refs(task_text)
        exact_visible_file = bool(file_refs) and file_refs.issubset(visible_files)
        if exact_visible_file and not policy_hit and ("memory note" in text or not _external_memory_signal(text)):
            return GateDecision("skip", "exact_visible_file_context_already_in_aider")
        simple_local = (
            _contains_any(text, SIMPLE_EDIT_TERMS)
            and visible_count <= 2
            and (exact_visible_file or bool(file_refs))
            and not memory_hit
            and not policy_hit
            and not context_hit
        )
        if simple_local:
            return GateDecision("skip", "simple_local_edit_exact_file_visible")
        if visible_count == 1 and not memory_hit and not policy_hit and not context_hit and repo_map_chars == 0:
            return GateDecision("skip", "single_file_task_no_project_memory_signal")
        if memory_hit and context_hit:
            return GateDecision("inject", "memory_and_project_context_indicators", use_memory=True, use_context=True)
        if memory_hit:
            return GateDecision("inject", "memory_indicator", use_memory=True, use_status=policy_hit)
        if policy_hit:
            return GateDecision("inject", "policy_or_security_indicator", use_status=True, use_context=True)
        if context_hit or visible_count > 3 or repo_map_chars > 6000:
            return GateDecision("inject", "project_context_or_multifile_uncertainty", use_context=True)
        return GateDecision("skip", "no_oacs_signal")

    def _status(self, *, git_root: str | None, request_id: str | None) -> tuple[dict[str, Any], bool]:
        now = time.monotonic()
        if self._status_cache is not None and now < self._status_cache_expires_at:
            return self._status_cache, True
        def build_status(svc: Any) -> dict[str, Any]:
            key_status = svc.key_provider.status()
            tables = (
                "memory_records",
                "context_capsules",
                "evidence_refs",
                "audit_events",
                "task_traces",
                "rules",
            )
            return {
                "db": str(svc.config.db_path),
                "db_exists": svc.config.db_path.exists(),
                "base_dir": str(svc.config.base_dir),
                "key": key_status.__dict__,
                "counts": {table: len(svc.store.list(table, limit=None)) for table in tables},
            }

        status = self._library_call(
            event="oacs_status",
            git_root=git_root,
            request_id=request_id,
            fn=build_status,
            require_key=False,
        )
        if status:
            self._status_cache = status
            self._status_cache_expires_at = now + max(0.0, self.config.status_cache_ttl)
            return status, False
        return {}, False

    def _context_build(self, *, intent: str, git_root: str | None, request_id: str) -> dict[str, Any] | None:
        def build(svc: Any) -> dict[str, Any]:
            capsule = svc.context.build(intent, self.config.actor, None, [self.config.scope], self.config.budget)
            svc.audit.record("context.build", self.config.actor, capsule.id)
            return capsule.model_dump()

        return self._library_call(
            event="oacs_context_build",
            git_root=git_root,
            request_id=request_id,
            fn=build,
            require_key=True,
        )

    def _memory_query(self, *, query: str, git_root: str | None, request_id: str) -> list[dict[str, Any]]:
        def query_memory(svc: Any) -> list[dict[str, Any]]:
            memories = svc.memory.query(query, self.config.actor, [self.config.scope])
            svc.audit.record("memory.query", self.config.actor, None, {"query_hash": str(hash(query))})
            return [memory.model_dump() for memory in memories]

        result = self._library_call(
            event="oacs_memory_query",
            git_root=git_root,
            request_id=request_id,
            fn=query_memory,
            require_key=True,
        )
        if not isinstance(result, list):
            return []
        return [item for item in result if isinstance(item, dict)]

    def _library_call(
        self,
        *,
        event: str,
        git_root: str | None,
        request_id: str | None,
        fn: Any,
        require_key: bool,
    ) -> Any:
        started = time.perf_counter()
        try:
            svc = self._get_services(git_root=git_root, require_key=require_key)
            result = fn(svc)
        except Exception as exc:
            latency_ms = (time.perf_counter() - started) * 1000
            self._log(
                {
                    "event": event,
                    "request_id": request_id,
                    "backend": "oacs_library",
                    "exit_code": -1,
                    "latency_ms": round(latency_ms, 3),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "fail_open": not self.config.strict,
                }
            )
            if self.config.strict:
                raise RuntimeError(f"OACS command failed: {exc}") from exc
            return None
        latency_ms = (time.perf_counter() - started) * 1000
        self._log(
            {
                "event": event,
                "request_id": request_id,
                "backend": "oacs_library",
                "exit_code": 0,
                "latency_ms": round(latency_ms, 3),
                "result_type": type(result).__name__,
                "fail_open": not self.config.strict,
            }
        )
        return result

    def _get_services(self, *, git_root: str | None, require_key: bool) -> Any:
        if require_key in self._services_cache:
            return self._services_cache[require_key]
        from oacs.app import services

        original_cwd: str | None = None
        if git_root:
            import os

            original_cwd = os.getcwd()
            os.chdir(git_root)
        try:
            svc = services(require_key=require_key)
            self._services_cache[require_key] = svc
            return svc
        finally:
            if original_cwd:
                os.chdir(original_cwd)

    def _format_capsule(
        self,
        capsule: dict[str, Any],
        *,
        intent: str,
        decision: GateDecision,
        status: dict[str, Any],
        memories: list,
        visible_files: set[str],
    ) -> str:
        lines = [
            "[OACS_CONTEXT_CAPSULE]",
            "mode: selective",
            f"intent: {intent}",
            f"reason: {decision.reason}",
        ]
        constraints = self._constraints(capsule)
        if self.config.evidence_strict:
            constraints.append(
                "Do not invent files, project decisions, memory entries, conventions, or architecture facts not supported by the capsule or visible repository context."
            )
        if constraints:
            lines.append("constraints:")
            lines.extend(f"- {item}" for item in _dedup_texts(constraints, limit=6))

        memory_lines = self._render_memories(memories)
        if memory_lines:
            lines.append("relevant_memory:")
            lines.extend(f"- {item}" for item in memory_lines)

        evidence = _dedup_texts([str(item) for item in capsule.get("evidence_refs", []) if item], limit=6)
        if evidence:
            lines.append("evidence:")
            lines.extend(f"- {item}" for item in evidence)

        related_files = self._related_files(capsule=capsule, memories=memories)
        if related_files:
            lines.append("related_files:")
            for file_name in related_files[:8]:
                suffix = " (already visible)" if file_name in visible_files else ""
                lines.append(f"- {file_name}{suffix}")

        status_counts = status.get("counts") if isinstance(status, dict) else None
        if isinstance(status_counts, dict):
            lines.append("status:")
            lines.append(f"- memory_records: {status_counts.get('memory_records')}")
            lines.append(f"- context_capsules: {status_counts.get('context_capsules')}")

        lines.append("[/OACS_CONTEXT_CAPSULE]")
        return "\n".join(lines)

    def _constraints(self, capsule: dict[str, Any]) -> list[str]:
        constraints: list[str] = []
        for item in capsule.get("forbidden_assumptions", []) or []:
            if item:
                constraints.append(f"Forbidden assumption: {item}")
        permissions = capsule.get("permissions") or {}
        if isinstance(permissions, dict):
            denied = [key for key, value in permissions.items() if value is False]
            if denied:
                constraints.append("Denied permissions: " + ", ".join(sorted(denied)[:6]))
        rules = capsule.get("included_rules") or []
        if rules:
            constraints.append("Applicable rules: " + ", ".join(str(rule) for rule in rules[:4]))
        return constraints

    def _has_substantive_capsule(self, capsule: dict[str, Any]) -> bool:
        for key in ("included_skills", "included_tools", "evidence_refs", "related_files", "files", "included_files"):
            value = capsule.get(key)
            if isinstance(value, list) and value:
                return True
        return False

    def _render_memories(self, memories: list) -> list[str]:
        rendered = []
        for item in memories[: max(0, self.config.memory_limit)]:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            content_text = content.get("text") if isinstance(content, dict) else content
            text = item.get("summary") or item.get("text") or content_text
            if not text:
                continue
            memory_id = str(item.get("id") or "memory")
            evidence = item.get("evidence_refs") or []
            evidence_text = f" evidence={','.join(str(ref) for ref in evidence[:3])}" if evidence else ""
            rendered.append(f"{memory_id}: {_single_line(str(text), 280)}{evidence_text}")
        return rendered

    def _related_files(self, *, capsule: dict[str, Any], memories: list) -> list[str]:
        candidates: list[str] = []
        for key in ("related_files", "files", "included_files"):
            value = capsule.get(key)
            if isinstance(value, list):
                candidates.extend(str(item) for item in value if item)
        for item in memories:
            if not isinstance(item, dict):
                continue
            for key in ("path", "file", "files", "related_files"):
                value = item.get(key)
                if isinstance(value, str):
                    candidates.append(value)
                elif isinstance(value, list):
                    candidates.extend(str(entry) for entry in value if entry)
        return _dedup_texts([candidate for candidate in candidates if _looks_like_file(candidate)], limit=12)

    def _limit_text(self, text: str) -> str:
        max_chars = max(0, self.config.max_injected_chars)
        max_token_chars = max(0, self.config.max_injected_tokens_estimate) * 4
        limit = min(value for value in (max_chars, max_token_chars) if value > 0) if max_chars or max_token_chars else 0
        if not limit or len(text) <= limit:
            return text
        marker = "\n- truncated: true\n[/OACS_CONTEXT_CAPSULE]"
        return text[: max(0, limit - len(marker))].rstrip() + marker

    def _log_request(
        self,
        *,
        request_id: str,
        intent: str,
        decision: GateDecision,
        status_cache_hit: bool,
        original_oacs_chars: int = 0,
        injected_oacs_chars: int = 0,
        estimated_oacs_tokens: int = 0,
        dedup_removed_chars: int = 0,
        memory_entries_used: int = 0,
        context_entries_used: int = 0,
    ) -> None:
        self._log(
            {
                "event": "oacs_request",
                "request_id": request_id,
                "mode": "selective",
                "gate_decision": decision.action,
                "gate_reason": decision.reason,
                "acs_calls": int(decision.use_status) + int(decision.use_memory) + int(decision.use_context),
                "status_cache_hit": status_cache_hit,
                "original_oacs_chars": original_oacs_chars,
                "injected_oacs_chars": injected_oacs_chars,
                "estimated_oacs_tokens": estimated_oacs_tokens,
                "skipped_oacs_reason": decision.reason if decision.action == "skip" else None,
                "dedup_removed_chars": dedup_removed_chars,
                "memory_entries_used": memory_entries_used,
                "context_entries_used": context_entries_used,
                "strict_evidence_enabled": self.config.evidence_strict,
                "intent": intent,
                "final_prompt_tokens": None,
                "completion_tokens": None,
                "success": None,
            }
        )

    def _log(self, payload: dict) -> None:
        if not self.config.log_file:
            return
        path = Path(self.config.log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=True, sort_keys=True) + "\n")


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _file_refs(text: str) -> set[str]:
    return {
        token.strip("`'\".,:;()[]{}")
        for token in re.findall(r"[\w./-]+\.(?:py|md|toml|yaml|yml|json|txt|rs|go|ts|tsx|js|jsx)", text)
    }


def _looks_like_file(text: str) -> bool:
    return bool(re.search(r"\.(py|md|toml|yaml|yml|json|txt|rs|go|ts|tsx|js|jsx)$", text))


def _external_memory_signal(text: str) -> bool:
    return any(
        term in text
        for term in (
            "previous oacs memory",
            "oacs memory",
            "project memory",
            "from memory",
            "decision from memory",
            "remembered",
            "agreed",
            "historical",
        )
    )


def _single_line(text: str, limit: int) -> str:
    value = " ".join(text.split())
    if len(value) <= limit:
        return value
    return value[: max(0, limit - 3)].rstrip() + "..."


def _dedup_texts(items: list[str], *, limit: int) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        value = _single_line(str(item), 500)
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
        if len(result) >= limit:
            break
    return result
