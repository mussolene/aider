# Candidate Matrix: Coding Agents + OACS/acs

Scores: 1 = poor, 2 = weak, 3 = workable, 4 = good, 5 = excellent.

Sources were limited to official repositories/docs where possible.

## Summary Ranking

| Rank | Project | Score | Primary OACS path | Verdict |
| ---: | --- | ---: | --- | --- |
| 1 | Aider | 57/75 | no-fork via OpenAI-compatible backend + read-only OACS context files; thin fork in repo map | Best first research host |
| 2 | OpenCode | 56/75 | no-fork via rules/agents/shell; plugin/custom tool/MCP path | Best agent-loop host if installed cleanly |
| 3 | Cline | 55/75 | no-fork via CLI + `.clinerules`; plugin/SDK/MCP path | Strong, but heavier UI/permission surface |
| 4 | Continue | 51/75 | context provider or MCP integration | Best context-provider experiment, weaker autonomous CLI fit |
| 5 | Codex CLI | 43/75 | OpenAI-compatible/Ollama path where supported; rules/AGENTS.md | Good baseline, less obvious fork/plugin target |

## Matrix

| Project | Repo URL | License | Language | Install difficulty | Local model support | OpenAI-compatible endpoint support | Shell/tool loop available | File edit/apply available | Context assembly hook | Memory/retrieval hook | Benchmarkability | Fork complexity | OACS integration path | Expected ROI | Risk | Verdict |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | --- |
| Aider | https://github.com/aider-ai/aider | Apache-2.0 | Python | 4 | 4 | 4 | 3 | 5 | 4 | 3 | 5 | 4 | Use `--openai-api-base` / OpenAI-compatible OACS backend; add `acs` output as read-only files; thin fork around repo map/context selection | 4 | Local weak models may fail edit format; shell tool is not the main loop | Primary first candidate |
| OpenCode | https://github.com/sst/opencode redirects to https://github.com/anomalyco/opencode | MIT | TypeScript | 4 | 4 | 4 | 5 | 5 | 4 | 4 | 4 | 3 | No-fork: AGENTS/rules + shell `acs`; thin plugin/custom tool/MCP for context/memory | 5 | Very fast-moving project; API churn; large TS codebase | Primary second candidate |
| Continue | https://github.com/continuedev/continue | Apache-2.0 | TypeScript | 3 | 4 | 4 | 3 | 4 | 5 | 5 | 3 | 3 | Custom context provider or MCP server wrapping `acs context build` / `acs memory query` | 4 | IDE-centric; less direct full agent benchmark; context is user-selected | Best context-provider path |
| Cline | https://github.com/cline/cline | Apache-2.0 | TypeScript | 3 | 5 | 5 | 5 | 5 | 4 | 4 | 3 | 3 | No-fork CLI with `.clinerules` and `acs`; SDK/plugin/MCP for hooks | 4 | Heavy UI/approval model; benchmark automation may be harder | Strong but not first |
| Codex CLI | https://github.com/openai/codex | Apache-2.0 | Rust | 3 | 3 | 3 | 5 | 5 | 3 | 2 | 4 | 2 | Use as baseline with rules/AGENTS.md and OpenAI-compatible/local OSS path where configured | 3 | Rust internals; OpenAI product coupling; extension hooks less obvious | Baseline, not first fork target |

## Notes By Candidate

### Aider

Official repo says Aider is terminal AI pair programming, supports cloud and
local LLMs, builds a repository map, has git integration, lint/test loops, and
is Apache-2.0. Official docs state local models are supported through Ollama and
OpenAI-compatible APIs.

OACS fit:

- Easy no-fork baseline because current OACS backend is OpenAI-compatible.
- Repo-map is the likely thin-fork point for replacing or supplementing context.
- Can inject `acs context build` output via generated read-only files first.
- Good benchmarkability because Aider already has benchmark assets and CLI mode.

Risk:

- Local small models often fail Aider edit formats.
- Aider is not primarily a shell-tool agent, so direct `acs` command use by the
  model is less natural than in OpenCode/Cline.

### OpenCode

Important correction: `opencode-ai/opencode` is archived. The current project is
`anomalyco/opencode` via `sst/opencode`. Official repo is MIT, TypeScript, and
documents build/plan agents, shell permissions, and terminal-first operation.

OACS fit:

- Best no-fork shell integration candidate: model can be instructed to call
  `acs`.
- Agent/rules model should support OACS skill prompt.
- Plugin/custom tool/MCP docs suggest a thin integration path.

Risk:

- Very fast-moving codebase, many releases and issues.
- Hook stability needs local inspection before forking.

### Continue

Continue has explicit context providers and MCP support. Official docs include
repo-map, search, terminal, tree, and MCP context providers.

OACS fit:

- Cleanest way to expose `acs context build` as a context provider.
- Good for testing context relevance and token reduction.

Risk:

- More IDE/context-provider than autonomous terminal agent.
- Benchmarking end-to-end code edits is less direct.

### Cline

Cline official repo/docs describe CLI, IDE, SDK, terminal command execution,
rules/skills, local providers, OpenAI-compatible APIs, plugins, and MCP.

OACS fit:

- Strong no-fork route: `.clinerules` + CLI + `acs` command.
- Strong plugin route: SDK/plugin lifecycle hooks may support policy/audit/tool
  integration.

Risk:

- Human-in-the-loop approval and UI surfaces can complicate automated benchmark.
- Larger product surface than needed for a minimal research host.

### Codex CLI

Codex is Apache-2.0, mostly Rust, terminal coding agent. Good baseline because it
is the current environment’s coding-agent style.

OACS fit:

- Good baseline for prompt/rules + `acs`.
- Less attractive as first fork target because hook points are less obvious and
  internals are Rust-heavy.

Risk:

- Product coupling to OpenAI auth/models.
- Local/OpenAI-compatible behavior must be verified in the exact installed CLI.

## Source Links

- Aider repo: https://github.com/aider-ai/aider
- Aider LLM docs: https://aider.chat/docs/llms.html
- Aider config docs: https://aider.chat/docs/config/aider_conf.html
- OpenCode repo: https://github.com/sst/opencode
- OpenCode docs: https://opencode.ai/docs
- Continue context provider docs: https://docs.continue.dev/customize/custom-providers
- Cline repo: https://github.com/cline/cline
- Cline install/provider docs: https://docs.cline.bot/getting-started/installing-cline
- Codex repo: https://github.com/openai/codex
