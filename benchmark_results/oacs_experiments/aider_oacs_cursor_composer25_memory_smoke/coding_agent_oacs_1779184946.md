# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | model_calls | repair_turns | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | completion_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_direct | memory_seeded_001 | memory_seeded | False | 0 | False | False | True | 1 | 0 | 5548.1 | 3542.0 | 223.7 | 190 | 853 | 0 | 0 | 0 | 0 | 0 | 0 |
| aider_oacs_fork | memory_seeded_001 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 21709.0 | 6841.6 | 269.3 | 190 | 951 | 34 | 1 | 0 | 1 | 166 | 0 |

## Summary

- `aider_direct`: success 0/1, avg latency 5548.1 ms, avg cpu 3542.0 ms, avg context chars 190.0, avg prompt tokens 853.0, avg completion tokens 0.0, avg model calls 1.0, acs calls 0, OACS skip/inject 0/0
- `aider_oacs_fork`: success 1/1, avg latency 21709.0 ms, avg cpu 6841.6 ms, avg context chars 190.0, avg prompt tokens 951.0, avg completion tokens 34.0, avg model calls 1.0, acs calls 1, OACS skip/inject 0/1
