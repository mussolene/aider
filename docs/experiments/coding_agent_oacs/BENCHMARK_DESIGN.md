# Benchmark Design

## Goal

Measure whether OACS/acs improves existing coding agents without writing a new
agent loop.

## Task Set

Start with 20 tasks:

- 5 simple code edits
- 5 bug/debug tasks
- 5 project-context tasks
- 3 memory-dependent tasks
- 2 policy/context-constraint tasks

Expand to 50 only after the runner is stable.

## Modes

- A: agent + base local model, no OACS
- B: agent + base local model + strong OACS prompt/rules + `acs` shell
- C: agent + OACS backend as OpenAI-compatible provider
- D: agent + OACS context wrapper file from `acs context build`
- E: optional trained acs-LoRA model
- F: optional validator/repair loop

## Metrics

Quality:

- task_success
- patch_applies
- tests_pass
- final_groundedness
- hallucinated_file_refs
- user_intervention_needed

Efficiency:

- turns_to_success
- model_calls_count
- tool_calls_count
- prompt_tokens_est
- completion_tokens_est
- context_chars
- latency_total
- acs_calls_count
- acs_latency_total

Behavior:

- unnecessary_tool_calls
- `acs` command correctness
- JSON parse success
- policy refusal correctness
- evidence citation/use

## Measurement Strategy

For agents that expose token/cost telemetry, record native numbers.

For agents that do not:

- estimate prompt/completion tokens by chars / 4;
- count model calls from logs;
- count `acs` calls by wrapping `acs` with a small logging shim only inside the
  experiment environment;
- measure wall time per task.

## Acceptance Gates

OACS integration is supported if:

- project-context or memory-dependent success improves by >=20 percentage points;
- average context size drops versus baseline or standard RAG-style context;
- no more than +25% latency on tasks that still need model generation;
- deterministic memory/policy tasks skip model calls or reduce latency by >=5x;
- no unsafe context export or secret leakage.

OACS integration is rejected if:

- success does not improve;
- token/context use increases materially;
- agent calls `acs` unnecessarily;
- automation is too brittle to benchmark;
- integration requires rewriting the agent loop.
