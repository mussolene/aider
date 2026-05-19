# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | model_calls | repair_turns | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | completion_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_direct | memory_seeded_001 | memory_seeded | False | 0 | False | False | True | 1 | 0 | 19104.3 | 4406.8 | 218.9 | 190 | 716 | 689 | 0 | 0 | 0 | 0 | 1 |
| aider_oacs_fork | memory_seeded_001 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 9985.1 | 4562.5 | 235.9 | 190 | 957 | 244 | 1 | 0 | 1 | 166 | 0 |

## Summary

- `aider_direct`: success 0/1, avg latency 19104.3 ms, avg cpu 4406.8 ms, avg context chars 190.0, avg prompt tokens 716.0, avg completion tokens 689.0, avg model calls 1.0, acs calls 0, OACS skip/inject 0/0
- `aider_oacs_fork`: success 1/1, avg latency 9985.1 ms, avg cpu 4562.5 ms, avg context chars 190.0, avg prompt tokens 957.0, avg completion tokens 244.0, avg model calls 1.0, acs calls 1, OACS skip/inject 0/1
