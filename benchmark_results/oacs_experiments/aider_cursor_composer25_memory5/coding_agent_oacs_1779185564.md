# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | model_calls | repair_turns | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | completion_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_cursor_provider | memory_seeded_001 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 43779.6 | 6970.8 | 280.7 | 190 | 778 | 31 | 0 | 0 | 0 | 0 | 0 |
| aider_cursor_provider | memory_seeded_002 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 26040.1 | 7130.6 | 280.7 | 207 | 779 | 36 | 0 | 0 | 0 | 0 | 0 |
| aider_cursor_provider | memory_seeded_003 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 66258.1 | 8477.6 | 280.7 | 218 | 780 | 41 | 0 | 0 | 0 | 0 | 0 |
| aider_cursor_provider | memory_seeded_004 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 50745.7 | 8854.5 | 280.7 | 198 | 778 | 33 | 0 | 0 | 0 | 0 | 0 |
| aider_cursor_provider | memory_seeded_005 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 88158.2 | 8367.5 | 280.7 | 201 | 778 | 37 | 0 | 0 | 0 | 0 | 0 |
| aider_cursor_oacs | memory_seeded_001 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 19436.0 | 7059.1 | 280.7 | 190 | 951 | 27 | 1 | 0 | 1 | 166 | 0 |
| aider_cursor_oacs | memory_seeded_002 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 19201.0 | 6686.6 | 280.7 | 207 | 965 | 39 | 1 | 0 | 1 | 179 | 0 |
| aider_cursor_oacs | memory_seeded_003 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 18322.6 | 6638.0 | 280.7 | 218 | 975 | 35 | 1 | 0 | 1 | 188 | 0 |
| aider_cursor_oacs | memory_seeded_004 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 25842.4 | 6727.2 | 280.7 | 198 | 948 | 29 | 1 | 0 | 1 | 164 | 0 |
| aider_cursor_oacs | memory_seeded_005 | memory_seeded | True | 0 | True | True | True | 1 | 0 | 16839.1 | 6590.2 | 280.7 | 201 | 975 | 34 | 2 | 0 | 1 | 190 | 0 |

## Summary

- `aider_cursor_oacs`: success 5/5, avg latency 19928.2 ms, avg cpu 6740.2 ms, avg context chars 202.8, avg prompt tokens 962.8, avg completion tokens 32.8, avg model calls 1.0, acs calls 6, OACS skip/inject 0/5
- `aider_cursor_provider`: success 5/5, avg latency 54996.4 ms, avg cpu 7960.2 ms, avg context chars 202.8, avg prompt tokens 778.6, avg completion tokens 35.6, avg model calls 1.0, acs calls 0, OACS skip/inject 0/0
