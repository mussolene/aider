# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | model_calls | repair_turns | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | completion_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_cursor_provider | polyglot_python_proverb | polyglot_python_repair | True | 0 | True | True | True | 1 | 0 | 28583.8 | 7425.0 | 272.8 | 5059 | 1100 | 100 | 0 | 0 | 0 | 0 | 0 |
| aider_cursor_oacs | polyglot_python_proverb | polyglot_python_repair | True | 0 | True | True | True | 1 | 0 | 30921.3 | 7270.7 | 272.8 | 5059 | 1100 | 107 | 0 | 1 | 0 | 0 | 0 |

## Summary

- `aider_cursor_oacs`: success 1/1, avg latency 30921.3 ms, avg cpu 7270.7 ms, avg context chars 5059.0, avg prompt tokens 1100.0, avg completion tokens 107.0, avg model calls 1.0, acs calls 0, OACS skip/inject 1/0
- `aider_cursor_provider`: success 1/1, avg latency 28583.8 ms, avg cpu 7425.0 ms, avg context chars 5059.0, avg prompt tokens 1100.0, avg completion tokens 100.0, avg model calls 1.0, acs calls 0, OACS skip/inject 0/0
