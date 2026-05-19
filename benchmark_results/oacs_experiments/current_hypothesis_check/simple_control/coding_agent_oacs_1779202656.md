# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | turns | model_calls | repair_turns | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | completion_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_cursor_provider | edit_slugify_001 | simple_code_edit | True | 0 | True | True | True | 1 | 1 | 0 | 29222.2 | 6581.3 | 311.8 | 319 | 831 | 82 | 0 | 0 | 0 | 0 | 0 |
| aider_cursor_provider | edit_math_002 | simple_code_edit | True | 0 | True | True | True | 1 | 1 | 0 | 23527.0 | 6387.1 | 311.8 | 273 | 817 | 49 | 0 | 0 | 0 | 0 | 0 |
| aider_cursor_oacs | edit_slugify_001 | simple_code_edit | True | 0 | True | True | True | 1 | 1 | 0 | 32030.8 | 6438.6 | 311.8 | 319 | 831 | 119 | 0 | 1 | 0 | 0 | 0 |
| aider_cursor_oacs | edit_math_002 | simple_code_edit | True | 0 | True | True | True | 1 | 1 | 0 | 24801.3 | 6565.0 | 311.8 | 273 | 817 | 46 | 0 | 1 | 0 | 0 | 0 |

## Summary

- `aider_cursor_oacs`: success 2/2, avg latency 28416.1 ms, avg cpu 6501.8 ms, avg context chars 296.0, avg prompt tokens 824.0, avg completion tokens 82.5, avg model calls 1.0, acs calls 0, OACS skip/inject 2/0
- `aider_cursor_provider`: success 2/2, avg latency 26374.6 ms, avg cpu 6484.2 ms, avg context chars 296.0, avg prompt tokens 824.0, avg completion tokens 65.5, avg model calls 1.0, acs calls 0, OACS skip/inject 0/0
