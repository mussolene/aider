# Selective OACS Final Recommendation

Date: 2026-05-19

## Executive Result

The fluent/selective OACS hypothesis is partially confirmed.

The useful product direction is not an always-on OACS prepend and not a new
coding agent. The useful direction is a thin Aider fork/plugin layer that uses
OACS only when the task needs external project memory, policy grounding, or
non-visible decisions.

## Implementation

The Aider v0.86.2 fork remains minimal:

- no replacement of Aider's chat loop;
- no changes to diff/apply/git behavior;
- no model provider changes;
- OACS hook only in context assembly;
- upstream Aider and fork are benchmarked as separate agents.

Patch artifact:

- `oacs-impl branch`

The fork adds:

- `aider/oacs_context.py`
- `--oacs-context`
- `--oacs-actor`
- `--oacs-scope`
- `--oacs-budget`
- `--oacs-command`
- `--oacs-log-file`
- `--oacs-memory-limit`
- `--oacs-max-injected-chars`
- `--oacs-max-injected-tokens-estimate`
- `--oacs-evidence-strict`
- `--oacs-strict`

There are no experimental user-facing retrieval modes inside the fork. The fork
has one behavior: selective OACS context.

Update: the fork now uses OACS as a Python library through `oacs.app.services()`
instead of spawning `acs` subprocesses for `status`, `context.build`, and
`memory.query`. The benchmark runner installs the dependency into the isolated
Aider environment with `uvx --with oacs`.

## Selective Gate

The fork skips OACS when:

- the task is a simple local edit;
- the exact referenced context file is already visible to Aider;
- the task references a local memory note file already in Aider context;
- there is no external memory, policy, or project-decision signal.

The fork uses OACS when:

- the task explicitly references OACS/project memory, remembered decisions, or
  previous project decisions;
- the task is policy/security sensitive;
- OACS can provide actual memory text or evidence-bound constraints.

Generic `acs context build` output containing only rule/permission metadata is
not injected for ordinary context tasks.

## Evidence

Primary artifacts:

- `benchmark_results/aider_oacs_selective_full/coding_agent_oacs_1779175111.json`
- `benchmark_results/aider_oacs_selective_full/coding_agent_oacs_1779175111.md`
- `benchmark_results/aider_oacs_selective_memory/coding_agent_oacs_1779175906.json`
- `benchmark_results/aider_oacs_selective_memory/coding_agent_oacs_1779175906.md`
- `benchmark_results/aider_oacs_library_smoke/coding_agent_oacs_1779178014.md`
- `benchmark_results/aider_oacs_library_memory_smoke/coding_agent_oacs_1779178218.md`
- `benchmark_results/aider_oacs_library_full/coding_agent_oacs_1779179216.md`
- `benchmark_results/aider_oacs_library_memory_full/coding_agent_oacs_1779180031.md`

Environment:

- Aider upstream: v0.86.2 via `uvx --from aider-chat`
- Aider fork: `/Users/maxon/git/aider` via `PYTHONPATH`
- Model: Ollama `gemma4:e2b`
- Endpoint: `http://127.0.0.1:11434/v1`
- Execution: sequential, no concurrent model calls

## Original 20 Tasks

These are ordinary coding-agent tasks where most context is already visible in
files.

| metric | upstream Aider | Aider OACS fork |
| --- | ---: | ---: |
| success | 15/20 | 16/20 |
| avg latency | 21733.8 ms | 21609.6 ms |
| avg CPU | 4262.4 ms | 4667.5 ms |
| avg prompt tokens | 797.0 | 862.0 |
| avg completion tokens | 555.0 | 485.2 |
| total ACS calls | 0 | 10 |
| OACS skip/inject | 0/0 | 15/5 |
| total estimated OACS tokens | 0 | 831 |

Interpretation:

- simple/local context was skipped in 15/20 tasks;
- prompt token overhead dropped from the old always-on `~1200` average to
  `862`, which is `+8.1%` over upstream Aider;
- success improved by one task;
- latency was effectively flat/slightly better;
- CPU remained higher by about `9.5%` in the pre-library run; the library
  adapter smoke suggests OACS call overhead is lower, but a full library run is
  still needed for a final CPU claim;
- this meets the `prompt <= direct +10%` target on the original task set.

## Memory-Seeded 20 Tasks

These tasks hide required facts from Aider. The source file is visible, but the
expected value exists only in committed OACS memory. Hidden tests are not passed
to Aider.

Fixture:

- `benchmarks/coding_agent_oacs_memory_seeded_tasks.jsonl`

| metric | upstream Aider | Aider OACS fork |
| --- | ---: | ---: |
| success | 0/20 | 20/20 |
| avg latency | 27069.0 ms | 11477.2 ms |
| avg CPU | 4262.5 ms | 4992.2 ms |
| avg prompt tokens | 718.3 | 983.9 |
| avg completion tokens | 787.4 | 209.7 |
| total ACS calls | 0 | 24 |
| OACS skip/inject | 0/0 | 0/20 |
| avg estimated OACS tokens | 0 | 178.3 |
| avg hallucinated refs | 0.45 | 0.05 |

Interpretation:

- direct Aider failed all hidden-memory tasks;
- OACS fork solved all hidden-memory tasks;
- prompt tokens increased because memory was required;
- completion tokens and latency dropped sharply because the model stopped
  guessing and received the exact remembered fact;
- this confirms OACS memory as a strong deterministic context layer when the
  needed fact is not already in files.

## Library Adapter Smoke

After switching from `acs` subprocesses to the OACS Python library:

Simple-edit 5-task smoke:

| mode | success | avg latency | avg prompt tokens | OACS calls |
| --- | ---: | ---: | ---: | ---: |
| `aider_direct` | 3/5 | 23064.6 ms | 777.4 | 0 |
| `aider_oacs_fork` | 3/5 | 27619.7 ms | 777.4 | 0 |

Memory-seeded 5-task smoke:

| mode | success | avg latency | avg prompt tokens | OACS calls | total OACS library latency |
| --- | ---: | ---: | ---: | ---: | ---: |
| `aider_direct` | 0/5 | 26099.2 ms | 717.2 | 0 | 0 ms |
| `aider_oacs_fork` | 5/5 | 13433.2 ms | 977.0 | 6 | 1127.2 ms |

The library path preserves the useful behavior and removes shell process
spawning from the hook. The measured OACS library calls are around `188 ms`
each on this smoke, materially lower than the earlier subprocess-based path.

## Library Adapter Full Runs

Original 20-task library run:

| metric | upstream Aider | Aider OACS fork |
| --- | ---: | ---: |
| success | 16/20 | 15/20 |
| avg latency | 21622.3 ms | 17595.9 ms |
| avg CPU | 4189.0 ms | 4349.4 ms |
| avg prompt tokens | 797.0 | 862.0 |
| avg completion tokens | 544.4 | 456.3 |
| total OACS/library calls | 0 | 10 |
| OACS skip/inject | 0/0 | 15/5 |
| avg OACS library latency | 0 ms | 65.9 ms |

Memory-seeded 20-task library run:

| metric | upstream Aider | Aider OACS fork |
| --- | ---: | ---: |
| success | 0/20 | 20/20 |
| avg latency | 26733.6 ms | 11628.3 ms |
| avg CPU | 4219.5 ms | 4558.9 ms |
| avg prompt tokens | 718.3 | 983.9 |
| avg completion tokens | 787.4 | 209.3 |
| total OACS/library calls | 0 | 24 |
| OACS skip/inject | 0/0 | 0/20 |
| avg OACS library latency | 0 ms | 211.9 ms |

Updated reading after the full library run:

- Removing subprocess calls materially reduced OACS overhead.
- On ordinary tasks, selective OACS stayed within the prompt budget target
  (`862` vs `797`, `+8.1%`) and reduced average latency, but this particular
  run lost one success relative to upstream (`15/20` vs `16/20`).
- On hidden-memory tasks, OACS remained decisive (`20/20` vs `0/20`) and cut
  latency by more than half because the model no longer guessed.
- CPU is still higher for the fork, but the overhead is now much smaller than
  the old subprocess path: about `+3.8%` on ordinary tasks and `+8.0%` on
  memory-seeded tasks.

## What Confirmed

- OACS is useful when it suppresses search/guessing with exact memory.
- Always-on retrieval prepend is wrong.
- Selective gating restores prompt-token economics on ordinary tasks.
- The best integration point is Aider context assembly, not a standalone
  backend proxy for coding agents.
- A tiny local model benefits when OACS gives exact facts and constraints.
- Direct library integration is the right implementation shape; CLI subprocess
  calls should stay out of the model-call hot path.

## What Did Not Confirm

- OACS does not magically improve all coding tasks.
- OACS has not proven CPU reduction on ordinary tasks. The library adapter
  reduces overhead, but fork CPU remains slightly higher.
- Selective OACS does not guarantee better ordinary-task success; it needs
  stricter relevance thresholds to avoid marginal context hurting small models.
- Context-only `acs context build` is not yet useful enough unless it returns
  actual evidence/files/tool facts, not just generic policy metadata.
- The fork should not inject context simply because a task is "project-level" if
  Aider already has the referenced files.

## External Benchmark Update

A Polyglot Python repair-loop smoke was added after the library-path results.
It used real Aider `--auto-test --test-cmd` repair turns on local `gemma4:e2b`.

| mode | success | avg latency | avg prompt tokens | avg completion tokens | avg model calls | OACS skip/inject |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aider_direct` | 0/2 | 113287.1 ms | 3100.0 | 2200.0 | 2.5 | 0/0 |
| `aider_oacs_fork` | 0/2 | 112278.6 ms | 3100.0 | 2160.0 | 2.5 | 5/0 |

This does not prove ordinary coding-task improvement. It proves the corrected
selective behavior: OACS did not inject context on single-file tasks where the
visible file and test feedback were already sufficient.

The weak point is the base model. `gemma4:e2b` did not converge on simple
Polyglot tasks even with repair output. For external coding benchmarks, the next
valid test must use a stronger local coding model or a frontier model through
the same Aider harness. Otherwise the experiment mostly measures base-model
failure, not OACS value.

Memory-gate regression after tightening:

| mode | success | latency | prompt tokens | completion tokens | OACS skip/inject |
| --- | ---: | ---: | ---: | ---: | ---: |
| `aider_direct` | 0/1 | 19104.3 ms | 716 | 689 | 0/0 |
| `aider_oacs_fork` | 1/1 | 9985.1 ms | 957 | 244 | 0/1 |

The tightened gate still handles explicit OACS-memory tasks correctly.

## Recommendation

Choose Path B:

Build OACS/acs as a plugin/context layer for existing coding agents, with Aider
as the first host.

Do not make the standalone OACS backend the primary coding-agent product. Keep
it for chat/runtime experiments, but coding agents should integrate at context
assembly.

Do not train a model as the primary path yet. The main gain came from exact
deterministic memory retrieval and selective injection, not learned behavior.

## Next 7 Days

- Keep the Python library adapter and remove the obsolete `--oacs-command`
  option once the fork branch is no longer patch-only.
- Add relevance thresholds to `acs memory query` so irrelevant global benchmark
  memories do not leak into unrelated tasks.
- Tighten policy/context gates so ordinary project-context tasks do not inject
  OACS unless there is exact evidence text, not just metadata.
- Add a small stable Aider plugin/fork test suite for gate decisions.
- Run the same benchmark with Qwen3 4B/8B and one stronger coding model.
- Add per-task final prompt token extraction from Aider history instead of
  relying only on rounded Aider console token lines.

## Next 30 Days

- Turn the fork patch into a maintainable minimal plugin/fork branch.
- Implement an OACS context provider API that returns scored memory/evidence
  snippets, not only raw `acs` CLI output.
- Add project-local memory namespaces for benchmark isolation.
- Test OpenCode or Codex CLI as a second host.
- Evaluate whether exact-memory tasks remain strong on real repositories, not
  only synthetic fixtures.

## Do Not Do

- Do not return to always-on OACS prepend.
- Do not build a new coding agent loop.
- Do not use the OACS backend proxy as the primary Aider path.
- Do not claim compute reduction generally; claim selective inference reduction
  only where OACS prevents guessing or broad context search.
- Do not train LoRA before the deterministic memory/context layer is stable.
