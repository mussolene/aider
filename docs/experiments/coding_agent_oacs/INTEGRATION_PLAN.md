# Integration Plan

## Principle

Do not build a new coding agent loop. First integrate OACS/acs into existing
agents as context, memory, policy, and validation support.

## Phase 1: No-Fork Integration

Target agents:

1. Aider
2. OpenCode

Setup:

- Expose current backend as OpenAI-compatible endpoint:
  `http://127.0.0.1:8080/v1`
- Keep `acs` available in PATH.
- Add an OACS prompt/rules file per agent:
  - when to call `acs status`;
  - when to call `acs memory query`;
  - when to call `acs context build`;
  - how to interpret JSON;
  - no secret/context export unless policy allows.

No-fork test modes:

- A. agent + local model, no OACS
- B. agent + local model + OACS prompt/rules + `acs` shell available
- C. agent + OACS backend provider

## Phase 2: Thin Wrapper

If no-fork is insufficient, add wrappers without touching agent internals:

- `scripts/experiment_acs_context.py`
  - calls `acs context build --intent ... --scope project --budget ... --json`
  - writes a compact context file the agent can read
- `scripts/experiment_acs_memory.py`
  - calls `acs memory query --json`
  - writes only relevant snippets
- `scripts/experiment_record.py`
  - calls `acs memory observe` and `acs checkpoint add`

## Phase 3: Thin Hook/Fork

Only if Phase 1/2 fail:

- Aider: hook repo-map/context assembly.
- OpenCode: hook custom tool/plugin/MCP or context-loading path.
- Continue: implement OACS context provider/MCP server.
- Cline: plugin/SDK/MCP hook.

Do not modify:

- model provider layer;
- file edit/diff apply;
- git logic;
- shell execution;
- UX.

## First Experiment To Run

Use Aider first because it is Python, has a stable CLI, supports local/OpenAI
compatible models, and has a repo-map/context abstraction.

Then use OpenCode because it is the strongest shell/tool loop candidate.

## Expected Early Failure Modes

- Local small models fail edit format.
- Agent calls `acs` too often, increasing latency.
- Agent reads `acs` JSON but ignores evidence.
- Context capsule is too generic to help coding tasks.
- No-fork prompt works but consumes too many tokens.

## Success Signal

OACS integration is worth continuing if it shows any of:

- fewer model calls;
- lower prompt context size;
- fewer irrelevant files included;
- fewer hallucinated file references;
- higher task success on project-memory/context tasks;
- successful deterministic policy/memory handling without model generation.
