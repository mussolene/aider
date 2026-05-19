# OACS Hook Audit

Date: 2026-05-19

## Scope

This audit covers the Aider v0.86.2 OACS fork patch stored at
`oacs-impl branch` and the
working vendor tree under `/Users/maxon/git/aider`.

The fork must be evaluated as a separate Aider variant against real upstream
Aider. It should not expose multiple experimental retrieval modes inside the
fork. The fork behavior is now a single selective OACS context layer.

## Previous Hook Behavior

The first hook was injected in `aider/coders/base_coder.py::get_repo_messages`.
For every request with `--oacs-context`, it called:

- `acs status --json`
- `acs context build --intent <intent> --actor aider-oacs --scope project --budget 800 --json`
- `acs memory query --query <task> --actor aider-oacs --scope project --json`

It then prepended an OACS message before Aider's repo map message.

## Prompt Injection Shape

The previous hook injected a JSON block with:

- capsule id/type/purpose
- actor/scope/budget
- included memories/rules/skills/tools/evidence
- forbidden assumptions
- permissions
- checksum
- rendered memory records
- status counts

This was safe enough for provenance, but too verbose for normal coding tasks.
Most fields were metadata rather than task-solving context.

## Duplication With Aider

Aider already supplies:

- user-selected files as editable context;
- read-only files when provided;
- optional repo map for project navigation;
- the current user task.

The previous OACS hook duplicated broad project context by adding:

- capsule metadata even when no OACS memory existed;
- status counts that do not help code edits;
- rules/permissions on simple file edits;
- an assistant acknowledgement message for every capsule.

It did not know which files Aider already had visible, so it could not avoid
injecting file-related context that Aider had already selected.

## Why Prompt Tokens Grew

The 20-task run showed prompt tokens rising from about `797` to `1200`, roughly
`+51%`. The main causes were:

- OACS ran on every request, including simple local edits.
- The hook always performed both context build and memory query.
- Empty or generic capsule metadata was still injected.
- Raw JSON formatting adds structural tokens.
- The extra assistant acknowledgement also consumed prompt budget.
- The memory database was empty, so most injected context was not high-value
  retrieval.

## Where OACS Helped

In the previous full run:

- direct Aider: `15/20`
- Aider OACS fork: `17/20`

The fork fixed:

- `edit_slugify_001`
- `edit_readme_004`
- `project_context_014`

The quality gain likely came from stronger task discipline and project-level
constraints, not from real memory retrieval, because OACS memory had zero
records.

## Where OACS Did Not Help

The hook was not useful for:

- simple single-file edits with exact files already in Aider context;
- tasks where all needed facts were already in the task fixture;
- empty-memory tasks;
- tasks where failure came from model weakness rather than context selection.

It also regressed `project_context_011`, which is consistent with extra prompt
entropy hurting a small local model.

## Updated Design

The fork now uses one selective gate:

- skip OACS for simple local edits with exact visible files;
- use memory query only when the task references memory/history/decision/policy
  or project conventions;
- use context build only for architecture/refactor/debug/multi-file uncertainty;
- use status only for policy/security validation or strict paths;
- cache status in-process for 60 seconds;
- inject compact text, not raw JSON.

Target capsule:

```text
[OACS_CONTEXT_CAPSULE]
mode: selective
intent: ...
reason: ...
constraints:
- ...
relevant_memory:
- ...
evidence:
- ...
related_files:
- ...
[/OACS_CONTEXT_CAPSULE]
```

The fork still fails open by default: if `acs` is unavailable or returns invalid
JSON, Aider continues as vanilla Aider and the event is logged.

Implementation update: the hook no longer calls `acs` in the hot path. It uses
the installed OACS Python package directly via `oacs.app.services()` for
`status`, `context.build`, and `memory.query`. The benchmark harness starts the
forked Aider with `uvx --with oacs` so the library is present in Aider's
isolated runtime. The old `--oacs-command` option remains only for patch
compatibility and should be removed when this becomes a maintained fork branch.

## Open Limitation

Aider does not provide a clean pre-model deterministic bypass point for direct
answers such as exact memory lookup. The fork can inject an ultra-short capsule,
but it should not bypass Aider's chat/edit loop without a deeper integration.
