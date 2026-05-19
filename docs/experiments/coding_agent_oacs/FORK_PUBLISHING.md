# Aider OACS Cursor Fork Publishing

Local fork path:

- `/Users/maxon/git/aider`

Published branches:

- `cursor-provider`: Cursor model provider only.
- `oacs-impl`: OACS implementation on top of `cursor-provider`.

Published commits:

- `cursor-provider`: see branch HEAD.
- `oacs-impl`: see branch HEAD.

Remote fork:

- `https://github.com/mussolene/aider`

## What The Fork Adds

- `cursor/<model-id>` Aider model provider backed by local Cursor Agent CLI.
- `--oacs-context` selective context hook.
- OACS context capsule logging and gate metrics.
- Docs: `docs/cursor-provider.md`.
- Unit tests: `tests/basic/test_cursor_provider.py`.

## Publish Safely

The standalone checkout remotes are:

- `origin`: `https://github.com/mussolene/aider.git`
- `upstream`: `https://github.com/Aider-AI/aider.git`

The fork branches are already pushed:

```sh
cd /Users/maxon/git/aider
git remote -v
git push origin cursor-provider
git push origin oacs-impl
```

## PR Strategy

Do not propose the full OACS hook upstream first.

Potential upstreamable PR:

- Cursor provider only.
- Minimal docs.
- Unit tests.

Use branch:

- `cursor-provider`

Keep OACS integration in the dedicated fork until the benchmark evidence is
stronger and the context API is stable.

## Current Evidence

- Composer 2.5 provider works inside Aider.
- `aider_cursor_provider` and `aider_cursor_oacs` both pass smoke tests.
- OACS skips ordinary single-file tasks.
- Existing memory benchmarks are too easy for Composer 2.5.
- Multi-turn harness works, but current scenarios are still too easy to prove
  OACS advantage.
