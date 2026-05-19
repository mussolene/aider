# Coding Agent + OACS Experiment Log

## Session

- Date: 2026-05-19
- Workspace: `/Users/maxon/git/aider`
- Goal: determine whether OACS/acs should be integrated into existing
  open-source coding agents instead of building a new agent loop.

## OACS State

`acs status --json`:

- database: `.agent/oacs/oacs.db`
- database exists: true
- key provider: `local_passphrase`
- key unlocked: true
- memory decrypt health: PASS
- context capsules: 3
- task traces: 29 at reconnaissance start
- rules: 5

## Actual ACS Commands Observed

Top-level commands from `acs --help`:

- `init`, `status`, `doctor`, `resume`, `run`
- `actor`, `capability`, `key`
- `memory`, `context`, `capsule`, `rule`, `skill`, `tool`
- `evidence`, `mcp`, `loop`, `benchmark`, `server`
- `audit`, `checkpoint`, `policy`, `conformance`

Memory commands:

- `acs memory observe --text ... [--actor ...] [--scope ...] [--json]`
- `acs memory propose --type ... --depth ... --text ... [--scope ...] [--json]`
- `acs memory commit MEMORY_ID [--json]`
- `acs memory query`, `read`, `doctor`, `quarantine`, `export-readable`,
  `purge-unreadable`, `correct`, `deprecate`, `supersede`, `forget`, `blur`,
  `sharpen`, `audit`, `export`, `import`

Context commands:

- `acs context build`
- `acs context explain`
- `acs context reduce`
- `acs context expand`
- `acs context lock`
- `acs context export`
- `acs context import`
- `acs context validate`

Checkpoint commands:

- `acs checkpoint add`
- `acs checkpoint latest`
- `acs checkpoint list`

Evidence commands:

- `acs evidence list`
- `acs evidence inspect EVIDENCE_REF`

## Checkpoints

- `trace_eb4d7f7517b94648a5e54f2200b413b7`: started coding-agent/OACS
  reconnaissance and candidate matrix.
- `trace_d099aed603c84c638ebec0ab163fcfd9`: started implementation of a
  reproducible coding-agent benchmark harness.
- `trace_e7bd822f72784f4aa44eb44a86f2ab4a`: recorded Aider smoke results and
  the OACS backend agent-compatible contract fix.

## Reconnaissance Notes

Current repo already has an OpenAI-compatible OACS backend/runtime:

- API/server: `src/oacs_backend/backend/server.py`,
  `src/oacs_backend/backend/openai_schema.py`
- providers: `lmstudio`, `ollama`, `openai_compat`, `mlx`, `llama_cpp`, `mock`
- runtime: `pipeline`, `router`, `capsule`, `policy`, `memory`, `verifier`,
  `budget`, `cache`, `request_logging`
- training/eval: action schema, OACS tool-use data generation, ACS loop eval
- benchmarks: runtime JSONL tasks and frozen ACS action-policy tasks

Already available for integration:

- OpenAI-compatible backend that existing agents can target via `base_url`.
- Direct local providers for MLX and Ollama.
- OACS CLI available as `acs` in PATH.
- `acs context build` and `acs memory query` exist.
- `acs checkpoint add` works.
- `acs memory observe/propose/commit` exist for experiment trace memory.

Missing for agent comparison:

- No ready benchmark harness for external coding agents.
- No wrapper yet to run Aider/OpenCode/Cline/Codex with identical tasks.
- No token/latency extraction adapter for those agents.
- No no-fork prompt pack yet.
- No thin hook for replacing agent context assembly with `acs context build`.

Local agent CLI availability:

- `codex`: installed at `/opt/homebrew/bin/codex`
- `continue`: installed and available in PATH
- `aider`: available through `uvx --python 3.12 --from aider-chat aider`
  as version `0.86.2`
- `opencode`: not installed
- `cline`: not installed

OACS memory write attempt:

- Command attempted: `acs memory observe --text ... --actor codex --scope project --json`
- Result: denied by OACS policy.
- Error: `AccessDenied: operation requires capability: memory.observe`
- Handling: do not bypass. Record via `acs checkpoint add` until an actor with
  explicit memory capability is created/granted.

## Current Decision

Reconnaissance supports continuing with two near-term tracks:

1. No-fork integration against Aider and OpenCode/Cline by exposing OACS through:
   - OpenAI-compatible backend;
   - `acs` shell command;
   - strong project prompt/rules.
2. Thin hook/plugin integration where the agent supports context providers,
   rules, MCP, plugins, or custom tools.

No evidence yet that a full custom coding agent should be written.

## Aider Smoke Implementation

Added:

- `benchmarks/coding_agent_oacs_tasks.jsonl`: 20 synthetic coding-agent tasks.
- `src/oacs_backend/experiments/coding_agent_benchmark.py`: external agent
  benchmark harness.
- `oacs-backend coding-agent-benchmark`: CLI entrypoint.
- `config/ollama_agent.yaml`: OACS backend config for coding-agent protocol
  compatibility.

Important implementation detail:

- Chat/user-facing OACS backend keeps `runtime.response_contract: final_answer`.
- Coding-agent endpoint uses `runtime.response_contract: agent_compatible`,
  disables verifier/cache/writeback, and raises `agent_max_output_tokens` to
  2048. This is not a fallback. It is an explicit API contract mode because
  Aider expects diff/protocol output, not a polished final answer.

## Aider Smoke Runs

Local provider:

- Ollama `gemma4:e2b`
- OpenAI-compatible direct URL: `http://127.0.0.1:11434/v1`
- OACS backend URL: `http://127.0.0.1:8080/v1`
- Agent: Aider `0.86.2`
- Execution: sequential, no concurrent model processes from the harness.

Artifact:

- `benchmark_results/coding_agent_oacs/coding_agent_oacs_1779167867.md`
- `benchmark_results/coding_agent_oacs/coding_agent_oacs_1779168232.md`

Results on first two tasks:

| mode | success | avg latency | avg CPU | avg context chars |
| --- | ---: | ---: | ---: | ---: |
| `aider_direct` | 1/2 | 25476.0 ms | 4157.2 ms | 296.0 |
| `aider_oacs_prompt` | 2/2 | 31874.7 ms | 4409.7 ms | 541.0 |
| `aider_oacs_context` | 2/2 | 36365.4 ms | 4263.5 ms | 866.0 |

OACS backend mode:

- Before `agent_compatible`, Aider repeatedly received 502
  `provider_contract_error` because the backend enforced final-answer cleanup
  against Aider's diff protocol.
- After `agent_compatible`, backend returned 200 and Aider applied a patch.
- Smoke result on `edit_slugify_001`: 0/1, 40711.0 ms, 4460.7 ms CPU,
  prompt 614 tokens, completion 1300 tokens. The patch failed the behavioral
  test for leading/trailing hyphen handling, same failure class as the direct
  baseline.

## Current Evidence Reading

- No-fork OACS prompt is the strongest smoke result so far.
- OACS context injection improves success on the two-task smoke, but adds more
  prompt/context than prompt-only.
- OACS backend is now protocol-compatible with Aider, but not yet better than
  prompt-only. Its value will depend on deterministic memory/policy/context
  routes, not merely proxying the same model call.
- Aider + small local Gemma is slow enough that full 20-task runs should be
  scheduled deliberately; the smoke already shows tens of seconds per task.

## Aider Fork/Hook Smoke

Decision tested:

- Stop using OACS backend as the integration point.
- Fork/hook Aider only at context assembly.
- Keep Aider's provider, edit loop, diff apply, shell, git, and UX unchanged.

Vendor:

- Source: `/Users/maxon/git/aider`
- Upstream tag: `v0.86.2`
- Commit: `253f036`
- Patch artifact: `oacs-impl branch`

Patch:

- Adds `--oacs-context`, `--oacs-actor`, `--oacs-scope`, `--oacs-budget`,
  `--oacs-command`, `--oacs-log-file`.
- Adds `aider/oacs_context.py`.
- Injects one OACS context capsule message in
  `aider/coders/base_coder.py::get_repo_messages()`.
- Uses real `acs context build --intent <intent> --actor aider-oacs --scope project --budget 800 --json`.
- Fails closed if `acs context build` fails; there is no silent fallback.

OACS permissions:

- Created actor `aider-oacs`.
- Granted `context.build` and `memory.query` for scope `project`.

Artifact:

- `benchmark_results/coding_agent_oacs/coding_agent_oacs_1779169094.md`

Results on first two tasks:

| mode | success | avg latency | avg CPU | prompt tokens | completion tokens | acs calls |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aider_oacs_fork` | 2/2 | 29682.5 ms | 5136.5 ms | 1200.0 | 540.5 | 1/task |

ACS hook measurements:

- `edit_slugify_001`: `acs context build`, intent `code`, 879.5 ms, 752 chars.
- `edit_math_002`: `acs context build`, intent `code`, 1169.6 ms, 752 chars.

Comparison with previous 2-task smoke:

- `aider_direct`: 1/2, 25476.0 ms avg latency.
- `aider_oacs_prompt`: 2/2, 31874.7 ms avg latency.
- `aider_oacs_context`: 2/2, 36365.4 ms avg latency.
- `aider_oacs_backend`: 0/1 after compatibility fix on slugify, 40711.0 ms.
- `aider_oacs_fork`: 2/2, 29682.5 ms avg latency.

Current reading:

- The fork/hook is cleaner than backend proxying for coding agents.
- It is slightly faster than prompt-only OACS on the two-task smoke, but uses
  more prompt tokens because the OACS capsule is now injected as real context.
- The OACS capsule currently contains little project memory, so quality gains
  are likely from policy/context framing more than retrieval.
- The next real test must use project-context and memory-dependent tasks, where
  `acs context build` should have actual useful content to select.
