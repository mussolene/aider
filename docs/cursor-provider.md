# Cursor Provider

This branch adds a narrow Aider model provider for Cursor models.

The provider is intentionally small:

- Aider still owns the chat loop, repo map, file editing, diff application, and git flow.
- Cursor is used only as the model backend through the local Cursor Agent CLI.
- No proxy server is required.
- No experimental context or memory behavior is included in this branch.

## Usage

Set a Cursor API key in the environment:

```sh
export CURSOR_API_KEY="..."
```

Run Aider with a Cursor model:

```sh
python -m aider --model cursor/composer-2.5 path/to/file.py
```

The `cursor/<model-id>` prefix is stripped before calling Cursor Agent. For
example, `cursor/composer-2.5` calls:

```sh
agent --print --output-format text --trust --mode ask --model composer-2.5
```

The Cursor Agent binary defaults to `agent`. Override it with:

```sh
export AIDER_CURSOR_AGENT_BIN="cursor-agent"
```

## Architecture Notes

This is a direct provider shim, not an OpenAI-compatible endpoint and not a
LiteLLM provider. Aider routes `cursor/<model-id>` calls to
`aider.cursor_provider.cursor_agent_completion()`, which:

1. converts Aider chat messages into a text prompt for Cursor Agent;
2. runs Cursor Agent in `ask` mode;
3. wraps the text output in the response shape Aider expects.

The provider disables streaming because Cursor Agent `--print` returns a full
text response. Token counts are estimated locally for Aider accounting.

## Scope

This branch should stay provider-only. Context injection, memory retrieval, and
benchmark harness changes belong in separate branches so the Cursor provider can
be reviewed and used independently.
