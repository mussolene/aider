# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_direct | memory_seeded_001 | memory_seeded | True | 0 | True | True | True | 15358.8 | 4539.6 | 210.6 | 190 | 740 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_002 | memory_seeded | True | 0 | True | True | True | 10871.4 | 4092.0 | 221.0 | 207 | 744 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_003 | memory_seeded | True | 0 | True | True | True | 16316.8 | 4140.0 | 221.0 | 218 | 757 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | memory_seeded_004 | memory_seeded | True | 0 | True | True | True | 9848.1 | 4350.0 | 221.0 | 198 | 739 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_005 | memory_seeded | True | 0 | True | True | True | 21525.2 | 4108.5 | 221.0 | 201 | 742 | 0 | 0 | 0 | 0 | 0 |
| aider_oacs_fork | memory_seeded_001 | memory_seeded | True | 0 | True | True | True | 13780.0 | 5026.7 | 221.0 | 190 | 995 | 1 | 0 | 1 | 166 | 0 |
| aider_oacs_fork | memory_seeded_002 | memory_seeded | True | 0 | True | True | True | 14244.5 | 5046.0 | 221.2 | 207 | 1000 | 1 | 0 | 1 | 179 | 0 |
| aider_oacs_fork | memory_seeded_003 | memory_seeded | True | 0 | True | True | True | 13710.0 | 4598.2 | 221.2 | 218 | 1000 | 1 | 0 | 1 | 188 | 0 |
| aider_oacs_fork | memory_seeded_004 | memory_seeded | True | 0 | True | True | True | 11198.3 | 4929.5 | 221.2 | 198 | 997 | 1 | 0 | 1 | 164 | 0 |
| aider_oacs_fork | memory_seeded_005 | memory_seeded | True | 0 | True | True | True | 14787.1 | 5333.8 | 221.2 | 201 | 1000 | 2 | 0 | 1 | 190 | 0 |

## Summary

- `aider_direct`: success 5/5, avg latency 14784.1 ms, avg cpu 4246.0 ms, avg context chars 202.8, acs calls 0, OACS skip/inject 0/0
- `aider_oacs_fork`: success 5/5, avg latency 13544.0 ms, avg cpu 4986.8 ms, avg context chars 202.8, acs calls 6, OACS skip/inject 0/5
