# Current Hypothesis Check

Date: 2026-05-19

## Scope

This check validates the current Aider fork direction:

- keep Cursor provider as a model backend shim;
- keep OACS as a selective context/memory layer;
- do not put OACS tool loops inside the Cursor provider;
- do not expose hidden tests or benchmark fixtures to the agent before model call.

## Harness Fixes

The benchmark harness now writes only `agent_files` before invoking Aider. Files
not listed in `agent_files`, such as hidden tests, are written after the model
call and before test execution. This prevents a CLI-backed agent from finding
expected answers by reading local test files.

For OACS modes, the harness sets `OACS_DB` to the repo-local database:

```text
.agent/oacs/oacs.db
```

This is required because benchmark workdirs live outside the git checkout.

The adversarial task JSON was loaded from `/tmp` and unlinked immediately after
loading, so the direct Cursor Agent run could not read the fixture from disk.

## Invalidated Run

An earlier adversarial run was stopped and discarded because Cursor Agent
searched the filesystem with `rg` even under `--mode ask`. It found task-related
strings outside the task sandbox. This confirms that Cursor Agent CLI is not a
pure inference provider and must be treated carefully in benchmarks.

## Result: Adversarial Memory

Tasks: 2 opaque memory tasks. Required values existed in ACS memory and were not
present in visible files or hidden tests before the model call.

Result file:

```text
benchmark_results/oacs_experiments/current_hypothesis_check/adversarial_memory/coding_agent_oacs_1779202527.md
```

| mode | success | avg latency | avg CPU | avg prompt tokens | avg completion tokens | ACS calls | OACS skip/inject |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `aider_cursor_provider` | 0/2 | 94193.0 ms | 41493.2 ms | 865.0 | 0.0 | 0 | 0/0 |
| `aider_cursor_oacs` | 2/2 | 25336.2 ms | 6648.5 ms | 907.0 | 39.5 | 2 | 0/2 |

Interpretation:

- OACS provided the missing project memory and turned both tasks from timeout/fail
  into pass.
- Prompt tokens increased only from 865.0 to 907.0 on average.
- Latency and CPU dropped because the model stopped searching/guessing and got
  compact evidence.

## Result: Simple Edit Control

Tasks: 2 ordinary simple code edits with all relevant implementation context
visible to Aider.

Result file:

```text
benchmark_results/oacs_experiments/current_hypothesis_check/simple_control/coding_agent_oacs_1779202656.md
```

| mode | success | avg latency | avg CPU | avg prompt tokens | ACS calls | OACS skip/inject |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aider_cursor_provider` | 2/2 | 26374.6 ms | 6484.2 ms | 824.0 | 0 | 0/0 |
| `aider_cursor_oacs` | 2/2 | 28416.1 ms | 6501.8 ms | 824.0 | 0 | 2/0 |

Interpretation:

- OACS skipped both simple tasks.
- Prompt tokens stayed identical.
- Latency difference was small run noise plus hook overhead, not extra model
  context.

## Verdict

The current hypothesis is partially supported:

- Selective OACS is useful when a coding agent needs project memory that is not
  in visible files.
- It should not be always-on retrieval prepend.
- It should not live inside `cursor_provider.py`.
- The value is a thin context/memory gate before Aider's normal model call.

The Cursor Agent CLI remains a problematic measurement backend because it can
perform its own filesystem searches. It is useful for practical experiments, but
not ideal as a pure model baseline. Future strict benchmarks should use a real
synchronous model provider where tool/file access is controlled by Aider.
