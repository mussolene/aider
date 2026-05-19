# Aider OACS Handoff

This directory is the local knowledge base for continuing the OACS hypothesis
inside the Aider fork.

## Branch Split

- `cursor-provider`: provider-only branch for Cursor Agent CLI as an Aider model backend.
- `oacs-impl`: OACS selective context integration on top of the provider cleanup.

The provider branch should not contain OACS behavior. OACS context, memory,
benchmark tasks, and experiment reports belong here on `oacs-impl`.

## Useful Files

- `CANDIDATE_MATRIX.md`: comparison of coding-agent candidates.
- `OACS_HOOK_AUDIT.md`: audit of the original always-on OACS hook.
- `SELECTIVE_OACS_FINAL_RECOMMENDATION.md`: current hypothesis verdict.
- `RESULTS_SUMMARY.md`: benchmark result notes.
- `BENCHMARK_DESIGN.md`: benchmark plan and metrics.

Task fixtures were copied to:

- `benchmarks/oacs/coding_agent_oacs_tasks.jsonl`
- `benchmarks/oacs/coding_agent_multiturn_oacs_tasks.jsonl`
- `benchmarks/oacs/coding_agent_oacs_memory_seeded_tasks.jsonl`
- `benchmarks/oacs/coding_agent_polyglot_python_tasks.jsonl`

Historical benchmark outputs were copied to:

- `benchmark_results/oacs_experiments/`

## Local ACS State

The Aider fork has a local ACS project database for experiment continuity:

- database: `.agent/oacs/oacs.db`
- passphrase file: `.agent/oacs/dev_passphrase.txt`
- actor: `codex`
- granted local capabilities: `memory.observe`, `memory.query`, `checkpoint.add`

Both `.agent/oacs/` and `.oacs/` are gitignored. The passphrase and encrypted
database are local machine state, not repo artifacts. Keep this local unless a
separate throwaway test fixture is explicitly needed.

Local API tokens for experiments should be stored in:

- `.agent/secrets/local.env`

That directory is gitignored. Expected variable names:

- `CURSOR_API_KEY`
- `HF_TOKEN`
- `HUGGINGFACE_HUB_TOKEN`

Load them for a shell session with:

```sh
set -a
. .agent/secrets/local.env
set +a
```

## Running The Local Harness

The standalone harness is:

```sh
python3 scripts/oacs/coding_agent_benchmark.py \
  --tasks-path benchmarks/oacs/coding_agent_multiturn_oacs_tasks.jsonl \
  --modes aider_direct,aider_oacs_fork \
  --model cursor/composer-2.5 \
  --limit 3
```

For Cursor-backed runs, `CURSOR_API_KEY` must be set in the environment. The
key must not be committed or written into benchmark artifacts.

## Current Working Hypothesis

OACS is not useful as always-on retrieval prepend. The useful shape is selective
context orchestration:

- skip OACS on simple local edits;
- query memory only when the task needs project history or decisions;
- build context capsules only for ambiguous, multi-file, architectural, or
  memory-dependent work;
- keep injected context small, evidence-bound, and deduplicated with Aider's
  visible context.

The next benchmark should focus on long-running and memory-seeded tasks where
standard Aider has to rediscover or over-scan context.
