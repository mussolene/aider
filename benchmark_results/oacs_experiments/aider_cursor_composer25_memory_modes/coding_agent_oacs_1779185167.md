# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | model_calls | repair_turns | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | completion_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_cursor_provider | memory_seeded_001 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 33314.1 | 7390.3 | 273.6 | 190 | 778 | 31 | 0 | 0 | 0 | 0 | 0 |
| aider_cursor_oacs | memory_seeded_001 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 21122.8 | 6735.3 | 273.6 | 190 | 951 | 33 | 1 | 0 | 1 | 166 | 0 |

## Summary

- `aider_cursor_oacs`: success 1/1, avg latency 21122.8 ms, avg cpu 6735.3 ms, avg context chars 190.0, avg prompt tokens 951.0, avg completion tokens 33.0, avg model calls 1.0, acs calls 1, OACS skip/inject 0/1
- `aider_cursor_provider`: success 1/1, avg latency 33314.1 ms, avg cpu 7390.3 ms, avg context chars 190.0, avg prompt tokens 778.0, avg completion tokens 31.0, avg model calls 1.0, acs calls 0, OACS skip/inject 0/0
