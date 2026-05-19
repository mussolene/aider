# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | turns | model_calls | repair_turns | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | completion_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_cursor_provider | multiturn_recipe_policy_001 | multiturn_memory_policy | True | 0 | True | True | True | 4 | 4 | 0 | 74459.7 | 26608.9 | 274.2 | 706 | 3844 | 0 | 0 | 0 | 0 | 0 | 0 |
| aider_cursor_provider | multiturn_router_contract_002 | multiturn_architecture | True | 0 | True | True | True | 4 | 4 | 0 | 80250.2 | 27377.6 | 274.2 | 609 | 3864 | 0 | 0 | 0 | 0 | 0 | 0 |
| aider_cursor_oacs | multiturn_recipe_policy_001 | multiturn_memory_policy | True | 0 | True | True | True | 4 | 4 | 0 | 92435.5 | 26586.5 | 274.2 | 706 | 4060 | 0 | 4 | 2 | 2 | 170 | 0 |
| aider_cursor_oacs | multiturn_router_contract_002 | multiturn_architecture | True | 0 | True | True | True | 4 | 4 | 0 | 71126.0 | 25505.3 | 274.2 | 609 | 4062 | 0 | 4 | 2 | 2 | 170 | 0 |

## Summary

- `aider_cursor_oacs`: success 2/2, avg latency 81780.7 ms, avg cpu 26045.9 ms, avg context chars 657.5, avg prompt tokens 4061.0, avg completion tokens 0.0, avg model calls 4.0, acs calls 8, OACS skip/inject 4/4
- `aider_cursor_provider`: success 2/2, avg latency 77354.9 ms, avg cpu 26993.3 ms, avg context chars 657.5, avg prompt tokens 3854.0, avg completion tokens 0.0, avg model calls 4.0, acs calls 0, OACS skip/inject 0/0
