# OACS Cursor Provider Fork

This fork adds two narrow integrations for experiments:

- `cursor/<model-id>` model provider backed by the local Cursor Agent CLI.
- Optional selective OACS context injection before Aider model calls.

The goal is to keep Aider as the coding agent. Cursor is only used as the model
backend, and OACS is only used as a selective context layer.

## Cursor Provider

Set a Cursor API key in the environment:

```sh
export CURSOR_API_KEY="..."
```

Run Aider with a Cursor model:

```sh
python -m aider --model cursor/composer-2.5 --edit-format whole path/to/file.py
```

The provider calls:

```sh
agent --print --output-format text --trust --mode ask --model composer-2.5
```

This is not an OpenAI-compatible proxy. It is a direct Aider provider shim.

## OACS Context

Enable selective OACS context:

```sh
python -m aider \
  --model cursor/composer-2.5 \
  --oacs-context \
  --oacs-actor aider-oacs \
  --oacs-scope project \
  --oacs-budget 800 \
  path/to/file.py
```

OACS is fail-open by default. If OACS is unavailable, Aider continues without
the capsule.

## Experiment Modes

Use these modes in the `oacs-backend-llm` benchmark harness:

- `aider_cursor_provider`: Cursor provider only, no OACS.
- `aider_cursor_oacs`: same provider plus selective OACS.

This keeps the comparison fair: same Aider loop, same Cursor model, only the
context layer changes.

## Current Status

Composer 2.5 smoke tests:

- Cursor provider works inside Aider and applies patches normally.
- OACS skips ordinary single-file tasks.
- OACS injects explicit memory/policy context when gated.
- Existing synthetic memory tasks are too easy for Composer 2.5 and should not
  be treated as proof of OACS advantage.

Next required work:

- Add harder delayed-recall multi-turn benchmarks.
- Add unit tests for `cursor_provider.py`.
- Consider upstream PR only for the Cursor provider if it is useful without
  OACS-specific code.
