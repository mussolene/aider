# Final Recommendation

Status: preliminary after reconnaissance plus Aider smoke.

## Preliminary Recommendation

Path B is the best near-term direction:

> Build an OACS/acs plugin-layer for existing coding agents before investing in
> a custom coding agent loop.

After the first Aider smoke and the first Aider fork/hook smoke, this
recommendation is stronger, not weaker.

## Why

- Current OACS backend already proves deterministic memory/policy paths can save
  compute.
- Existing coding agents already solve file editing, shell execution, git, UX,
  and provider handling.
- A thin OACS layer can test the actual product hypothesis faster:
  better context, less token waste, fewer model calls, better groundedness.
- The first smoke shows prompt/context OACS can improve Aider success on a
  tiny local model, while backend-only proxying is not automatically useful.
- The fork/hook smoke shows the cleaner integration point: Aider should remain
  the coding agent, while OACS supplies policy-checked context capsules before
  model calls.

## What Changed After Smoke

Confirmed:

- Aider can be run reproducibly against local Ollama through OpenAI-compatible
  API.
- Strong OACS prompt improved the first two tasks from 1/2 to 2/2.
- OACS context injection also reached 2/2, but cost more context and latency.
- OACS backend can be made agent-compatible, but only with an explicit response
  contract that preserves diff/protocol output.
- A minimal Aider fork at `get_repo_messages()` reached 2/2 on the same smoke
  tasks without using OACS backend.
- On the full 20-task local run, the fork improved success from `15/20` to
  `17/20`.

Not confirmed:

- OACS backend as a transparent coding-agent provider is not yet better than
  prompt-only.
- `acs context build` has not yet proven value on memory/project-context-heavy
  tasks; current fork smoke only proves the hook is viable and not obviously
  worse than prompt-only.
- Compute reduction is not confirmed. The full local run showed higher prompt
  tokens, CPU, and latency for the fork.

## What To Do Next 7 Days

1. Install and run Aider in `experiments/vendors` or isolated env.
2. Run a memory-seeded benchmark where required facts exist only in OACS
   memory, not in local files.
3. Keep `aider_oacs_backend` as a separate backend-compatibility track, not as
   the main ROI claim.
4. Add an `acs` wrapper that logs `acs` invocations, latency, exit code, and
   JSON validity.
5. Grant or configure an OACS actor that can write experiment memories without
   bypassing policy.
6. Repeat the strongest subset on OpenCode or Codex CLI.
7. Only then decide whether a thin hook/fork is justified.

## What To Do Next 30 Days

1. Build a stable agent benchmark harness.
2. Add an `acs` logging wrapper for command counts/latency.
3. Implement one thin integration:
   - Aider repo-map hook, or
   - Continue context provider/MCP, or
   - OpenCode custom tool/plugin.
4. Compare no-fork vs thin hook.
5. Decide whether current backend should become:
   - standalone backend product;
   - provider for coding agents;
   - OACS plugin/context layer.

## What Not To Do

- Do not build a new coding agent loop now.
- Do not continue LoRA as the main path.
- Do not fork a large TS agent before no-fork evidence exists.
- Do not claim compute reduction on open-ended coding tasks until measured.
- Do not bypass OACS policy/context discipline for convenience.
- Do not route coding-agent protocol output through a final-answer sanitizer.
- Do not call backend-only proxying a win unless it reduces model calls,
  context size, or improves task success.
- Do not fork more of Aider than context assembly until the 20-task benchmark
  proves this hook has real ROI.
- Do not claim token or latency savings from the current Aider hook. The
  measured win is success rate, not compute.
