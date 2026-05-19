# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_direct | memory_seeded_001 | memory_seeded | False | 0 | False | False | True | 26718.8 | 4432.5 | 214.9 | 190 | 716 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | memory_seeded_002 | memory_seeded | False | 0 | False | False | True | 29176.6 | 4053.4 | 221.0 | 207 | 716 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_003 | memory_seeded | False | 0 | True | False | True | 41898.9 | 4024.0 | 221.3 | 218 | 722 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | memory_seeded_004 | memory_seeded | False | 0 | False | False | True | 20495.0 | 4083.5 | 221.3 | 198 | 714 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_005 | memory_seeded | False | 0 | False | False | True | 11747.4 | 4000.0 | 221.3 | 201 | 718 | 0 | 0 | 0 | 0 | 0 |
| aider_oacs_fork | memory_seeded_001 | memory_seeded | True | 0 | True | True | True | 14189.2 | 4755.3 | 221.3 | 190 | 971 | 1 | 0 | 1 | 166 | 0 |
| aider_oacs_fork | memory_seeded_002 | memory_seeded | True | 0 | True | True | True | 12957.4 | 4902.7 | 221.3 | 207 | 990 | 1 | 0 | 1 | 179 | 0 |
| aider_oacs_fork | memory_seeded_003 | memory_seeded | True | 0 | True | True | True | 14373.9 | 5198.5 | 221.3 | 218 | 1000 | 1 | 0 | 1 | 188 | 0 |
| aider_oacs_fork | memory_seeded_004 | memory_seeded | True | 0 | True | True | True | 12422.6 | 4732.3 | 221.3 | 198 | 972 | 1 | 0 | 1 | 164 | 0 |
| aider_oacs_fork | memory_seeded_005 | memory_seeded | True | 0 | True | True | True | 13047.0 | 5235.9 | 221.3 | 201 | 1000 | 2 | 0 | 1 | 190 | 0 |

## Summary

- `aider_direct`: success 0/5, avg latency 26007.3 ms, avg cpu 4118.7 ms, avg context chars 202.8, acs calls 0, OACS skip/inject 0/0
- `aider_oacs_fork`: success 5/5, avg latency 13398.0 ms, avg cpu 4964.9 ms, avg context chars 202.8, acs calls 6, OACS skip/inject 0/5
