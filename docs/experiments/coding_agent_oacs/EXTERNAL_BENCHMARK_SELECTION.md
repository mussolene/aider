# External Benchmark Selection For OACS Aider Fork

Date: 2026-05-19

## Question

We need to test the actual product hypothesis:

Can an OACS context/memory layer let a smaller local model solve agentic coding
tasks with fewer total tokens, fewer turns, and less unnecessary context than
standard coding-agent practice?

The current single-shot synthetic benchmark is not enough. It tests whether one
model call improves when OACS injects a small capsule. It does not test the
long-distance agent behavior we care about:

- repeated repair turns;
- test-output reflection;
- context accumulation;
- repo navigation;
- hidden facts;
- total tokens across the whole task.

## External Benchmarks Reviewed

### Aider Polyglot

Source:

- https://aider.chat/2024/12/21/polyglot.html
- https://github.com/Aider-AI/polyglot-benchmark
- https://epoch.ai/benchmarks/aider-polyglot

Fit:

- High.
- Same host agent family as our fork.
- Multi-language tasks from Exercism.
- 225 hard tasks across C++, Go, Java, JavaScript, Python, and Rust.
- Evaluation includes repair behavior: models get a second attempt with unit
  test output after a failed first attempt.

Why it matters:

- This directly tests whether OACS reduces repeated mistakes and test-repair
  token burn.
- It is much lighter than SWE-bench and can be sampled locally.
- It is close to our current harness because Aider already supports
  `--auto-test --test-cmd`.

Limitations:

- It is still exercise-style coding, not real repository issue fixing.
- OACS project memory may not naturally help unless we create memory/context
  variants or measure whether OACS correctly stays silent.

Verdict:

- Use first.
- Build a 30-task subset: 10 Python/JS, 10 Go/Rust, 10 Java/C++ if toolchains
  are present.
- Compare upstream Aider vs Aider OACS fork with identical local model.

### SWE-bench Lite / Verified

Source:

- https://github.com/SWE-bench/SWE-bench
- https://openai.com/index/introducing-swe-bench-verified/

Fit:

- High for product relevance.
- Real GitHub issues, real repos, hidden fail-to-pass and pass-to-pass tests.
- Measures repository-level software engineering rather than toy completion.

Why it matters:

- This is the standard style for coding-agent claims.
- It tests exactly the thing OACS claims to improve: issue understanding,
  repository navigation, and avoiding hallucinated fixes.

Limitations:

- Heavy for MacBook Pro M1 Pro 16GB.
- Official SWE-bench notes Docker evaluation can need about 120GB free storage,
  16GB RAM, and 8 CPU cores; ARM support is experimental.
- Verified has known benchmark-quality issues. OpenAI later reported material
  issues in a large portion of audited remaining failures and recommended newer
  benchmarks for frontier capability measurement.

Verdict:

- Use as a small smoke subset only on this machine.
- Do not run the full benchmark locally.
- Select 5-10 easy or lite tasks first.
- If local Docker/ARM setup is too expensive, use the task format as a design
  target and run full SWE-bench remotely later.

### Vexp SWE-bench Harness

Source:

- https://github.com/Vexp-ai/vexp-swe-bench

Fit:

- Medium.
- It wraps a curated 100-task SWE-bench Verified subset and explicitly tracks
  pass@1, duration, cost, and token usage.

Why it matters:

- Their metric shape matches our question: cost, speed, token usage, resolution.
- It is agent-oriented and not just model-oriented.

Limitations:

- Default setup is tied to Claude Code plus Vexp.
- Not ideal as a neutral local-model harness.

Verdict:

- Use for metric design, not as the first execution harness.
- Borrow the reporting schema: pass@1, cost/task, duration, tokens, unique wins.

### SWE-PolyBench

Source:

- https://arxiv.org/abs/2504.08703
- https://github.com/amazon-science/SWE-PolyBench

Fit:

- Medium/high later.
- Repository-level, execution-based, multilingual coding-agent benchmark.
- Contains 2110 instances across Java, JavaScript, TypeScript, and Python.

Why it matters:

- Better fit than Python-only tasks for a general coding agent.
- Includes bug fixes, feature additions, and refactoring.

Limitations:

- Docker-heavy.
- More complex than needed for the immediate OACS fork decision.

Verdict:

- Second-stage benchmark after Aider Polyglot and SWE-bench Lite smoke.

### Multi-SWE-bench / SWE-bench Multilingual

Source:

- https://github.com/multi-swe-bench
- https://swe-agent-bench.github.io/multilingual.html

Fit:

- Medium/high later.
- Real issue-resolution tasks across multiple languages.
- Good for testing whether OACS helps outside Python-centric repositories.

Limitations:

- Larger setup cost.
- Not the first thing to run on a constrained Mac.

Verdict:

- Use only after the OACS integration survives smaller benchmarks.

### RepoBench

Source:

- https://arxiv.org/abs/2306.03091

Fit:

- Low/medium for current question.
- Repository-level code completion, with retrieval/context-selection relevance.

Why it matters:

- It can test context selection and retrieval quality.

Limitations:

- It is code completion, not a full coding-agent patch/test/repair loop.
- It does not directly test Aider's edit and test cycle.

Verdict:

- Useful for isolated context retrieval evaluation.
- Not sufficient for product validation.

## Recommended Benchmark Plan

### Stage 1: Aider Polyglot Repair Subset

Goal:

- Test long-distance token economy with repair loops.

Setup:

- Use upstream Aider vs Aider OACS fork.
- Same model, same endpoint, same timeout.
- Enable Aider's native loop:
  - `--auto-test`
  - `--test-cmd <language-specific test command>`
  - `--yes-always`
  - `--no-auto-commits`
  - `--no-git`
- Count all model calls through `.aider.llm.history`.

Metrics:

- task_success;
- tests_pass;
- model_calls_count;
- reflection_count;
- total_prompt_tokens;
- total_completion_tokens;
- total_tokens;
- prompt_tokens_per_call;
- completion_tokens_per_call;
- latency_total;
- process_cpu_ms;
- OACS skip/inject;
- OACS library latency;
- context bytes injected;
- final patch size;
- failed first attempts;
- repaired failures.

Confirmation:

- OACS fork has equal or better success;
- total tokens are lower or not more than `+10%`;
- repair turns are fewer;
- OACS skip rate is high on tasks with no memory/context signal;
- OACS does not hurt ordinary exercise tasks.

Refutation:

- OACS fork has lower success and no token reduction;
- OACS mostly skips, meaning it adds no product value;
- OACS injects but does not reduce repair turns;
- OACS increases total tokens by more than `+10%` without success gain.

### Stage 2: Memory-Augmented Polyglot Variant

Goal:

- Test the actual OACS advantage: project memory that is not in visible files.

Setup:

- Add synthetic but benchmark-like memory to OACS:
  - naming conventions;
  - deprecated APIs;
  - hidden project decisions;
  - security constraints;
  - required implementation choices.
- Keep those facts out of the repository files shown to Aider.

Confirmation:

- direct Aider fails or uses more turns;
- OACS fork retrieves exact memory and solves with fewer total tokens than a
  prompt-only large context version.

Refutation:

- direct Aider solves equally by guessing;
- OACS memory retrieval is noisy;
- OACS context causes wrong edits or more repair loops.

### Stage 3: SWE-bench Lite / Verified Micro-Subset

Goal:

- Validate on real GitHub issue tasks.

Setup:

- Start with 5-10 easy/lite tasks.
- Use Docker only if the local M1 setup is stable.
- If local Docker is too heavy, produce patch predictions locally and evaluate
  remotely later.

Confirmation:

- OACS fork improves pass@1 or reduces total tokens/turns on issue-resolution
  tasks.

Refutation:

- no pass@1 improvement;
- no token/latency improvement;
- OACS injection degrades issue understanding.

## Immediate Implementation Tasks

1. Add a `coding-agent-repair-benchmark` mode or option to the current harness.
2. Parse `.aider.llm.history` into per-call token estimates instead of only the
   final Aider summary line.
3. Enable Aider `--auto-test` and pass the task's `test_command` as
   `--test-cmd`.
4. Track reflection count from stdout/history/test output.
5. Add a small Aider Polyglot subset under `experiments/vendors/` or
   `benchmarks/external/`.
6. Run upstream Aider vs Aider OACS fork sequentially.
7. Publish an explicit confirmation/refutation table.

## Current Position

The current evidence does not yet prove the long-distance claim.

What is proven:

- OACS as exact memory helps hidden-memory tasks.
- Selective gating prevents always-on context bloat.
- Library integration removes most subprocess overhead.

What is not proven:

- total token reduction over multi-turn coding;
- fewer repair loops;
- better success on ordinary coding tasks;
- order-of-magnitude token savings.

Therefore the next benchmark must be Aider Polyglot-style repair tasks or a
SWE-bench Lite micro-subset. Without that, we should not claim that OACS lets a
small model replace a larger one over long coding sessions.

