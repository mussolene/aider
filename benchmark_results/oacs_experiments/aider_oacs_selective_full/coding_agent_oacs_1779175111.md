# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_direct | edit_slugify_001 | simple_code_edit | False | 0 | True | False | True | 39803.9 | 4458.9 | 205.1 | 319 | 795 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | edit_math_002 | simple_code_edit | True | 0 | True | True | True | 19791.3 | 4262.5 | 212.0 | 273 | 784 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | edit_config_003 | simple_code_edit | True | 0 | True | True | True | 26740.9 | 4524.9 | 212.0 | 329 | 806 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | edit_readme_004 | simple_code_edit | False | 0 | True | True | False | 9166.8 | 3916.0 | 218.3 | 144 | 719 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | edit_parser_005 | simple_code_edit | True | 0 | True | True | True | 28858.4 | 4298.3 | 218.3 | 312 | 783 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_cache_006 | bug_debug | True | 0 | True | True | True | 14670.8 | 4248.8 | 218.9 | 323 | 797 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_policy_007 | bug_debug | True | 0 | True | True | True | 27220.1 | 4504.2 | 218.9 | 407 | 808 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_json_008 | bug_debug | True | 0 | True | True | True | 30358.4 | 4366.1 | 218.9 | 329 | 816 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_budget_009 | bug_debug | False | 0 | True | False | True | 26815.5 | 3830.8 | 220.3 | 429 | 838 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_router_010 | bug_debug | True | 0 | True | True | True | 13595.0 | 4163.6 | 220.3 | 363 | 790 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_011 | project_context | False | 0 | True | False | True | 17215.8 | 4094.2 | 220.3 | 402 | 805 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_012 | project_context | True | 0 | True | True | True | 26938.0 | 4255.0 | 222.2 | 419 | 808 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_013 | project_context | True | 0 | True | True | True | 32744.6 | 4064.1 | 222.2 | 417 | 807 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_014 | project_context | True | 0 | True | True | True | 19933.8 | 4540.1 | 222.2 | 523 | 853 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_015 | project_context | True | 0 | True | True | True | 10149.8 | 4273.6 | 222.2 | 308 | 794 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_task_016 | memory_dependent | True | 0 | True | True | True | 23197.3 | 4407.2 | 222.9 | 290 | 776 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_task_017 | memory_dependent | True | 0 | True | True | True | 12375.5 | 4387.5 | 222.9 | 287 | 779 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_task_018 | memory_dependent | True | 0 | True | True | True | 12590.7 | 4362.4 | 222.9 | 272 | 772 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | policy_task_019 | policy_context_constraint | True | 0 | True | True | True | 11825.5 | 4084.8 | 222.9 | 431 | 798 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | policy_task_020 | policy_context_constraint | False | 0 | True | True | False | 30683.4 | 4205.0 | 222.9 | 432 | 812 | 0 | 0 | 0 | 0 | 0 |
| aider_oacs_fork | edit_slugify_001 | simple_code_edit | False | 0 | True | False | True | 26673.1 | 4567.2 | 222.9 | 319 | 795 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | edit_math_002 | simple_code_edit | True | 0 | True | True | True | 22838.4 | 4367.0 | 222.9 | 273 | 784 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | edit_config_003 | simple_code_edit | True | 0 | True | True | True | 28802.2 | 4353.0 | 222.9 | 329 | 806 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | edit_readme_004 | simple_code_edit | False | 0 | True | True | False | 9301.1 | 4246.6 | 222.9 | 144 | 719 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | edit_parser_005 | simple_code_edit | True | 0 | True | True | True | 19686.1 | 3922.0 | 222.9 | 312 | 783 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | bug_cache_006 | bug_debug | True | 0 | True | True | True | 17779.3 | 4528.9 | 222.9 | 323 | 797 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | bug_policy_007 | bug_debug | True | 0 | True | True | True | 33832.1 | 5581.5 | 222.9 | 407 | 1100 | 2 | 0 | 1 | 189 | 0 |
| aider_oacs_fork | bug_json_008 | bug_debug | True | 0 | True | True | True | 21130.7 | 4350.2 | 222.9 | 329 | 816 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | bug_budget_009 | bug_debug | False | 0 | True | False | True | 31793.0 | 4497.9 | 222.9 | 429 | 838 | 0 | 1 | 0 | 0 | 1 |
| aider_oacs_fork | bug_router_010 | bug_debug | True | 0 | True | True | True | 14370.8 | 4395.5 | 222.9 | 363 | 790 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | project_context_011 | project_context | False | 0 | True | False | True | 20699.7 | 4589.1 | 222.9 | 402 | 805 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | project_context_012 | project_context | True | 0 | True | True | True | 24773.4 | 5400.8 | 222.9 | 419 | 1100 | 2 | 0 | 1 | 183 | 0 |
| aider_oacs_fork | project_context_013 | project_context | True | 0 | True | True | True | 29730.5 | 5485.4 | 222.9 | 417 | 1100 | 2 | 0 | 1 | 187 | 0 |
| aider_oacs_fork | project_context_014 | project_context | True | 0 | True | True | True | 19300.9 | 4473.6 | 222.9 | 523 | 853 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | project_context_015 | project_context | True | 0 | True | True | True | 13554.6 | 4580.1 | 222.9 | 308 | 794 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | memory_task_016 | memory_dependent | True | 0 | True | True | True | 22922.3 | 4458.5 | 222.9 | 290 | 776 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | memory_task_017 | memory_dependent | True | 0 | True | True | True | 12312.7 | 4414.9 | 222.9 | 287 | 779 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | memory_task_018 | memory_dependent | True | 0 | True | True | True | 10868.9 | 4240.1 | 222.9 | 272 | 772 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | policy_task_019 | policy_context_constraint | True | 0 | True | True | True | 21918.5 | 5686.8 | 222.9 | 431 | 1100 | 2 | 0 | 1 | 187 | 0 |
| aider_oacs_fork | policy_task_020 | policy_context_constraint | True | 0 | True | True | True | 29902.9 | 5211.8 | 222.9 | 432 | 932 | 2 | 0 | 1 | 85 | 0 |

## Summary

- `aider_direct`: success 15/20, avg latency 21733.8 ms, avg cpu 4262.4 ms, avg context chars 350.4, acs calls 0, OACS skip/inject 0/0
- `aider_oacs_fork`: success 16/20, avg latency 21609.6 ms, avg cpu 4667.5 ms, avg context chars 350.4, acs calls 10, OACS skip/inject 15/5
