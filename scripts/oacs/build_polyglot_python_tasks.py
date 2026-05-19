from __future__ import annotations

import json
from pathlib import Path


DEFAULT_EXERCISES = [
    "proverb",
    "list-ops",
    "robot-name",
    "variable-length-quantity",
    "phone-number",
    "pig-latin",
    "wordy",
    "scale-generator",
    "beer-song",
    "grade-school",
    "two-bucket",
    "transpose",
    "simple-linked-list",
    "binary-search-tree",
    "book-store",
    "bowling",
    "forth",
    "grep",
    "poker",
    "zebra-puzzle",
]


def main() -> None:
    repo = Path("experiments/vendors/polyglot-benchmark/python/exercises/practice")
    out = Path("benchmarks/coding_agent_polyglot_python_tasks.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for slug in DEFAULT_EXERCISES:
        exercise = repo / slug
        if not exercise.exists():
            continue
        docs = _read_docs(exercise)
        files = _exercise_files(exercise)
        agent_files = [
            rel
            for rel in files
            if rel.endswith(".py") and not rel.endswith("_test.py") and not rel.startswith(".meta/")
        ]
        if not docs or not agent_files:
            continue
        rows.append(
            {
                "id": f"polyglot_python_{slug}",
                "category": "polyglot_python_repair",
                "source": "polyglot-benchmark/python",
                "prompt": (
                    "Edit only the listed implementation file(s). Do not browse URLs. "
                    "Do not ask follow-up questions. Return the full updated file content "
                    "in Aider's required file listing format so the pytest suite passes.\n\n"
                    f"{_sanitize_docs(docs).strip()}"
                ),
                "files": files,
                "agent_files": sorted(agent_files),
                "test_command": "python3 -m pytest -q",
                "checks": {"file_not_contains": [{"path": path, "text": "pass"} for path in sorted(agent_files)]},
            }
        )
    with out.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")
    print(f"Wrote {out} rows={len(rows)}")


def _read_docs(exercise: Path) -> str:
    parts: list[str] = []
    for name in ("instructions.md", "instructions.append.md", "hints.md"):
        path = exercise / ".docs" / name
        if path.exists():
            parts.append(path.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def _sanitize_docs(text: str) -> str:
    text = re_sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re_sub(r"^\[[^\]]+\]:\s*\S+.*$", "", text, multiline=True)
    text = re_sub(r"https?://\S+", "", text)
    return text[:5000]


def re_sub(pattern: str, repl: str, text: str, *, multiline: bool = False) -> str:
    import re

    flags = re.MULTILINE if multiline else 0
    return re.sub(pattern, repl, text, flags=flags)


def _exercise_files(exercise: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(exercise.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(exercise).as_posix()
        if any(part.startswith(".") for part in Path(rel).parts):
            continue
        if path.suffix not in {".py", ".md", ".toml", ".json", ".txt"}:
            continue
        files[rel] = path.read_text(encoding="utf-8")
    return files


if __name__ == "__main__":
    main()
