# Results Summary

## Current Status

This phase now has a runnable coding-agent benchmark harness and first Aider
smoke evidence.

The evidence is not enough for a final product claim. It is enough to decide
that no-fork prompt/context integration is worth testing further, and that the
OACS backend needs an explicit agent-compatible contract when used as a coding
agent provider.

## Aider + Ollama Gemma Smoke

Artifact:

- `benchmark_results/coding_agent_oacs/coding_agent_oacs_1779167867.md`
- `benchmark_results/coding_agent_oacs/coding_agent_oacs_1779168232.md`

Environment:

- Agent: Aider `0.86.2`
- Provider: Ollama `gemma4:e2b`
- Direct endpoint: `http://127.0.0.1:11434/v1`
- OACS endpoint: `http://127.0.0.1:8080/v1`
- Task count: 2 for prompt/context/direct; 1 for backend smoke.
- Execution: sequential.

| mode | success | avg latency | avg CPU | prompt tokens | completion tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| `aider_direct` | 1/2 | 25476.0 ms | 4157.2 ms | 789.5 | 522.0 |
| `aider_oacs_prompt` | 2/2 | 31874.7 ms | 4409.7 ms | 838.5 | 892.5 |
| `aider_oacs_context` | 2/2 | 36365.4 ms | 4263.5 ms | 927.5 | 1084.0 |
| `aider_oacs_backend` | 0/1 | 40711.0 ms | 4460.7 ms | 614.0 | 1300.0 |
| `aider_oacs_fork` | 2/2 | 29682.5 ms | 5136.5 ms | 1200.0 | 540.5 |

Interpretation:

- `aider_oacs_prompt` improved smoke success from 1/2 to 2/2 with modestly
  higher prompt tokens and latency.
- `aider_oacs_context` also reached 2/2, but used more context and was slower
  than prompt-only.
- `aider_oacs_backend` is now protocol-compatible after the
  `agent_compatible` contract fix, but it did not improve quality on the first
  slugify task. It applied a patch that failed the same behavioral edge case
  as direct baseline.
- `aider_oacs_fork` is the cleanest integration so far: Aider stays the agent,
  OACS only replaces/adds context assembly via `acs context build`, and the
  two-task smoke reached 2/2 without routing through the OACS backend.
- The smoke supports "OACS skill/prompt helps small local model agent behavior"
  more than "OACS backend proxy alone helps coding agents."

## Aider Fork/Hook Details

Implementation:

- `oacs-impl` branch in `/Users/maxon/git/aider`

OACS calls:

- `acs context build --intent code --actor aider-oacs --scope project --budget 800 --json`
- `edit_slugify_001`: 879.5 ms, 752 output chars
- `edit_math_002`: 1169.6 ms, 752 output chars

Practical read:

- Fork/hook avoids the response-contract mismatch that hit backend mode.
- The hook has predictable overhead of about 0.9-1.2 seconds per task for the
  current empty-memory capsule.
- Prompt tokens rise to about 1.2k because the capsule is now real context.
- This is acceptable only if the capsule improves task success on
  context-heavy tasks or reduces broader repo-map/file scanning later.

## Existing Project Evidence To Carry Forward

Qwen3 4B OACS runtime benchmark:

- raw: 5/10, avg latency 5252.6 ms
- standard prompt: 4/10, avg latency 4547.2 ms
- standard RAG: 7/10, avg latency 4900.0 ms
- OACS memory runtime: 8/10, avg latency 2857.5 ms

Ollama Gemma E2B OACS runtime benchmark:

- raw: 0/10
- standard prompt: 1/10
- standard RAG: 2/10
- OACS memory runtime: 4/10

Action-policy evidence:

- Qwen3 4B minimal prompt: validator 0/12, command 0/12
- Qwen3 4B + OACS prompt: validator 12/12, command/tool 11/12
- Qwen3 4B LoRA adapter: validator 6/12, command/tool 6/12
- Qwen3 8B + OACS prompt: validator 1/12, command/tool 1/12

Carry-forward conclusion:

- Runtime/selective execution is promising.
- Prompt-only OACS is useful.
- LoRA-only and bigger-model-only are not sufficient.
- Next evidence must compare this against existing coding agents.

## Open Items

- Run memory-seeded Aider benchmark where required facts exist only in OACS
  memory, not in local task files.
- Add OpenCode or Codex CLI second candidate run.
- Add an `acs` command wrapper to count real `acs` calls and latency.
- Replace the older `aider_oacs_context` wrapper with the fork/hook path if the
  20-task benchmark confirms the smoke.
- Run OpenCode baseline if install is clean.
- Decide whether thin hook/fork is justified.

## Full Local Aider Run

Artifact:

- `benchmark_results/aider_oacs_full/coding_agent_oacs_1779170477.md`

| mode | success | avg latency | avg CPU | avg prompt tokens | avg completion tokens | hallucinated refs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aider_direct` | 15/20 | 21648.8 ms | 4232.2 ms | 797.0 | 562.4 | 1 |
| `aider_oacs_fork` | 17/20 | 23376.2 ms | 5850.2 ms | 1200.0 | 547.0 | 1 |

This supports a quality gain, not a compute gain:

- success improved by 2 tasks;
- latency increased by about 8%;
- prompt tokens increased by about 51%;
- CPU increased by about 38%;
- hallucinated refs did not improve.

The next benchmark must isolate actual OACS memory value. Current
memory-dependent tasks include memory files inside the task workspace, so
vanilla Aider can solve them without OACS memory.

## Selective Aider OACS Update

Artifacts:

- `benchmark_results/aider_oacs_selective_full/coding_agent_oacs_1779175111.md`
- `benchmark_results/aider_oacs_selective_memory/coding_agent_oacs_1779175906.md`
- `docs/experiments/coding_agent_oacs/OACS_HOOK_AUDIT.md`
- `docs/experiments/coding_agent_oacs/SELECTIVE_OACS_FINAL_RECOMMENDATION.md`

The Aider fork was changed from always-on retrieval prepend to one selective
context layer. Upstream Aider and the fork are now treated as separate agents;
there are no user-facing retrieval modes inside the fork.

Original 20-task result:

| mode | success | avg latency | avg CPU | avg prompt tokens | avg completion tokens | acs calls | OACS skip/inject |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `aider_direct` | 15/20 | 21733.8 ms | 4262.4 ms | 797.0 | 555.0 | 0 | 0/0 |
| `aider_oacs_fork` | 16/20 | 21609.6 ms | 4667.5 ms | 862.0 | 485.2 | 10 | 15/5 |

Memory-seeded 20-task result with hidden tests and facts only in OACS memory:

| mode | success | avg latency | avg CPU | avg prompt tokens | avg completion tokens | acs calls | OACS skip/inject |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `aider_direct` | 0/20 | 27069.0 ms | 4262.5 ms | 718.3 | 787.4 | 0 | 0/0 |
| `aider_oacs_fork` | 20/20 | 11477.2 ms | 4992.2 ms | 983.9 | 209.7 | 24 | 0/20 |

Updated verdict:

- Selective OACS met the original-task token target: `862` prompt tokens is
  `+8.1%` over direct, not the old `+50.6%`.
- It preserved or improved quality on ordinary tasks: `16/20` vs `15/20`.
- It strongly improved hidden-memory tasks: `20/20` vs `0/20`.
- It did not prove CPU reduction in the pre-library full run. The later library
  adapter removes `acs` subprocess calls, but full-run CPU needs a fresh
  measurement.
- The practical path is Aider plugin/fork context assembly, not backend proxy
  and not model training as the primary mechanism.

Library adapter update:

- The fork now calls OACS as a Python library through `oacs.app.services()`
  instead of spawning `acs` subprocesses.
- The Aider fork runner uses `uvx --with oacs` so the isolated Aider process has
  the OACS package installed.
- Smoke evidence:
  - `benchmark_results/aider_oacs_library_smoke/coding_agent_oacs_1779178014.md`
  - `benchmark_results/aider_oacs_library_memory_smoke/coding_agent_oacs_1779178218.md`
- Memory-seeded 5-task smoke stayed at `5/5` for the fork vs `0/5` direct.
- Total measured OACS library latency on that 5-task memory smoke was
  `1127.2 ms` across 6 calls, about `188 ms/call`.

Full library-path results:

| task set | mode | success | avg latency | avg CPU | avg prompt tokens | avg completion tokens | OACS calls | skip/inject |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| original 20 | `aider_direct` | 16/20 | 21622.3 ms | 4189.0 ms | 797.0 | 544.4 | 0 | 0/0 |
| original 20 | `aider_oacs_fork` | 15/20 | 17595.9 ms | 4349.4 ms | 862.0 | 456.3 | 10 | 15/5 |
| memory-seeded 20 | `aider_direct` | 0/20 | 26733.6 ms | 4219.5 ms | 718.3 | 787.4 | 0 | 0/0 |
| memory-seeded 20 | `aider_oacs_fork` | 20/20 | 11628.3 ms | 4558.9 ms | 983.9 | 209.3 | 24 | 0/20 |

Full library artifacts:

- `benchmark_results/aider_oacs_library_full/coding_agent_oacs_1779179216.md`
- `benchmark_results/aider_oacs_library_memory_full/coding_agent_oacs_1779180031.md`

Full library verdict:

- Library integration removes the main subprocess tax; OACS library latency was
  about `65.9 ms/request` on original tasks and `211.9 ms/request` on
  memory-seeded tasks.
- On ordinary tasks, the fork did not improve quality in this run (`15/20` vs
  `16/20`), but stayed within token budget and reduced average latency.
- On hidden-memory tasks, the fork remained decisive (`20/20` vs `0/20`) and
  reduced average latency by more than half.
- CPU is still higher for the fork, so the claim should be "selective
  inference/context reduction", not general CPU reduction.

## External Benchmark Selection

Added:

- `docs/experiments/coding_agent_oacs/EXTERNAL_BENCHMARK_SELECTION.md`

Decision:

- Use Aider Polyglot first because it already matches our host agent and tests
  repair behavior with unit-test feedback.
- Use SWE-bench Lite/Verified only as a small smoke subset on this Mac because
  the official Docker evaluation is resource-heavy and ARM support is
  experimental.
- Use Vexp SWE-bench mainly as a metric-shape reference for pass@1, duration,
  token usage, and cost/task.
- Defer SWE-PolyBench and Multi-SWE-bench until the Aider fork proves value on
  smaller benchmarks.

Current falsification status:

- The long-distance claim is not yet proven.
- Hidden-memory value is proven in synthetic tasks.
- Ordinary coding-task quality is not improved consistently.
- Next required experiment is a repair-loop benchmark with total model calls and
  total tokens across the whole task.

## External Polyglot Repair-loop Smoke

Added:

- `scripts/build_polyglot_python_tasks.py`
- `benchmarks/coding_agent_polyglot_python_tasks.jsonl`

Harness changes:

- `oacs-backend coding-agent-benchmark --repair-loop` now runs Aider with
  `--auto-test --test-cmd`.
- The harness records `model_calls_count`, `repair_turns_est`,
  `completion_tokens_est`, OACS skip/inject counts, and cumulative token lines
  from Aider.
- Aider receives an absolute Python path for pytest because `uvx aider`
  otherwise resolves `python3` to an isolated environment without pytest.

Methodological fixes found during smoke:

- Raw Exercism/Polyglot docs contain URLs. Aider tried to scrape Python docs,
  which polluted the first smoke. The Polyglot task generator now strips URLs
  and asks the model to edit only implementation files.
- The OACS gate previously treated ordinary words like `previous` as memory
  signals. This caused irrelevant hidden-memory injection on a normal coding
  task. The fork now requires explicit OACS/project-memory phrasing for memory
  retrieval.

Repair-loop smoke result on local `gemma4:e2b`:

| task set | mode | success | avg latency | avg CPU | avg prompt tokens | avg completion tokens | avg model calls | OACS skip/inject |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Polyglot Python 2-task | `aider_direct` | 0/2 | 113287.1 ms | 5028.9 ms | 3100.0 | 2200.0 | 2.5 | 0/0 |
| Polyglot Python 2-task | `aider_oacs_fork` | 0/2 | 112278.6 ms | 4877.3 ms | 3100.0 | 2160.0 | 2.5 | 5/0 |

Artifacts:

- `benchmark_results/aider_oacs_polyglot_python_repair_fixed/coding_agent_oacs_1779182945.md`
- `benchmark_results/aider_oacs_polyglot_python_repair_fixed/coding_agent_oacs_1779182945.json`

Interpretation:

- On ordinary single-file Polyglot tasks, selective OACS behaved correctly: it
  skipped all 5 Aider model-call contexts and injected zero extra tokens.
- The local `gemma4:e2b` model failed both Polyglot tasks in both modes despite
  repair loops. It produced patches, but did not converge from pytest failures.
- Therefore this smoke does not support a claim that OACS improves ordinary
  coding benchmark success. It supports the narrower claim that selective OACS
  avoids unnecessary context cost on tasks where OACS should not participate.
- A full 19-task Polyglot run on this model is not practical as an interactive
  check: the 2-task x 2-mode run took about 7.5 minutes.

Gate regression after tightening memory detection:

| task set | mode | success | latency | prompt tokens | completion tokens | OACS skip/inject |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| memory-seeded 1-task | `aider_direct` | 0/1 | 19104.3 ms | 716 | 689 | 0/0 |
| memory-seeded 1-task | `aider_oacs_fork` | 1/1 | 9985.1 ms | 957 | 244 | 0/1 |

Regression artifact:

- `benchmark_results/aider_oacs_memory_gate_regression/coding_agent_oacs_1779183102.md`

The stricter gate still injects memory for explicit OACS-memory tasks while
skipping ordinary Polyglot tasks.

## Cursor Composer 2.5 Provider Fork Check

Added a direct provider inside the Aider fork:

- `cursor/<model-id>` models call local Cursor Agent CLI directly through
  `agent --print --mode ask --model <model-id>`.
- No OpenAI-compatible proxy is required.
- Cursor is used only as the model backend; Aider still owns prompt assembly,
  file editing, patch apply, and test/repair loop.

Benchmark modes:

- `aider_cursor_provider`: Aider fork with Cursor provider only, no OACS.
- `aider_cursor_oacs`: same provider plus selective OACS context hook.

Composer 2.5 memory-seeded 5-task smoke:

| mode | success | avg latency | avg CPU | avg prompt tokens | avg completion tokens | OACS skip/inject |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aider_cursor_provider` | 5/5 | 54996.4 ms | 7960.2 ms | 778.6 | 35.6 | 0/0 |
| `aider_cursor_oacs` | 5/5 | 19928.2 ms | 6740.2 ms | 962.8 | 32.8 | 0/5 |

Artifact:

- `benchmark_results/aider_cursor_composer25_memory5/coding_agent_oacs_1779185564.md`

Reading:

- The Cursor provider works inside Aider.
- The OACS mode injects memory correctly.
- This old memory-seeded dataset is no longer a strong discriminator for
  Composer 2.5: provider-only solved all first five tasks too. Treat this as a
  fork/provider correctness check, not proof of memory advantage.

Composer 2.5 Polyglot repair-loop smoke:

| mode | success | avg latency | avg prompt tokens | avg completion tokens | model calls | OACS skip/inject |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aider_cursor_provider` | 1/1 | 28583.8 ms | 1100.0 | 100.0 | 1.0 | 0/0 |
| `aider_cursor_oacs` | 1/1 | 30921.3 ms | 1100.0 | 107.0 | 1.0 | 1/0 |

Artifact:

- `benchmark_results/aider_cursor_composer25_polyglot_smoke/coding_agent_oacs_1779185638.md`

Reading:

- OACS correctly skipped ordinary single-file Polyglot context.
- Provider-only and OACS both passed. OACS added no prompt context, no ACS
  calls, and only a small gate overhead.

Next required dataset:

- Build adversarial hidden-memory tasks for strong models where values cannot be
  inferred from naming or common benchmark patterns.
- Keep comparing `aider_cursor_provider` vs `aider_cursor_oacs` on Composer 2.5.

## Composer 2.5 Multi-turn Scenario

Added:

- `benchmarks/coding_agent_multiturn_oacs_tasks.jsonl`

Shape:

- 2 tasks.
- 4 sequential user turns per task.
- Same working directory across turns.
- Final test is added only after all turns, so the agent must preserve and
  combine prior decisions.

Result:

| mode | success | avg latency | avg CPU | avg prompt tokens | avg model calls | OACS skip/inject |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `aider_cursor_provider` | 2/2 | 77354.9 ms | 26993.3 ms | 3854.0 | 4.0 | 0/0 |
| `aider_cursor_oacs` | 2/2 | 81780.7 ms | 26045.9 ms | 4061.0 | 4.0 | 4/4 |

Artifact:

- `benchmark_results/aider_cursor_composer25_multiturn/coding_agent_oacs_1779186192.md`

Reading:

- The multi-turn harness works and is closer to the real question than
  single-shot tasks.
- Both provider-only and OACS solved the current tasks. Composer 2.5 retains
  short-horizon state well enough through visible files and Aider history.
- OACS added about `+5.4%` prompt tokens on this run and did not improve
  success.
- The OACS gate behaved selectively: 4 skips and 4 injections across 8 turns.
- This still does not prove OACS advantage on long tasks. The next dataset must
  force delayed recall of facts that are no longer visible in the edited file or
  must span more turns/files than Aider's normal context makes cheap.
