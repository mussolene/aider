# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | turns | model_calls | repair_turns | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | completion_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_cursor_provider | adv_memory_alpha | adversarial_memory | False | 0 | False | False | True | 1 | 1 | 0 | 94312.6 | 42491.2 | 275.5 | 179 | 863 | 0 | 0 | 0 | 0 | 0 | 1 |
| aider_cursor_provider | adv_memory_beta | adversarial_memory | False | 0 | False | False | True | 1 | 1 | 0 | 94073.3 | 40495.2 | 275.5 | 190 | 867 | 0 | 0 | 0 | 0 | 0 | 1 |
| aider_cursor_oacs | adv_memory_alpha | adversarial_memory | True | 0 | True | True | True | 1 | 1 | 0 | 22169.7 | 6699.4 | 285.6 | 179 | 904 | 37 | 1 | 0 | 1 | 109 | 0 |
| aider_cursor_oacs | adv_memory_beta | adversarial_memory | True | 0 | True | True | True | 1 | 1 | 0 | 28502.7 | 6597.5 | 287.0 | 190 | 910 | 42 | 1 | 0 | 1 | 111 | 0 |

## Summary

- `aider_cursor_oacs`: success 2/2, avg latency 25336.2 ms, avg cpu 6648.5 ms, avg context chars 184.5, avg prompt tokens 907.0, avg completion tokens 39.5, avg model calls 1.0, acs calls 2, OACS skip/inject 0/2
- `aider_cursor_provider`: success 0/2, avg latency 94193.0 ms, avg cpu 41493.2 ms, avg context chars 184.5, avg prompt tokens 865.0, avg completion tokens 0.0, avg model calls 1.0, acs calls 0, OACS skip/inject 0/0
