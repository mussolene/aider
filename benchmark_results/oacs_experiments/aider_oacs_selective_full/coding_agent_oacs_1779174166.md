# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_direct | edit_slugify_001 | simple_code_edit | False | 0 | True | False | True | 42002.7 | 4320.8 | 205.3 | 319 | 795 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | edit_math_002 | simple_code_edit | True | 0 | True | True | True | 21152.2 | 4314.2 | 210.7 | 273 | 784 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | edit_config_003 | simple_code_edit | True | 0 | True | True | True | 28599.9 | 4335.8 | 210.7 | 329 | 806 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | edit_readme_004 | simple_code_edit | False | 0 | True | True | False | 9409.0 | 4231.5 | 219.3 | 144 | 719 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | edit_parser_005 | simple_code_edit | True | 0 | True | True | True | 19244.5 | 4270.7 | 222.7 | 312 | 783 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_cache_006 | bug_debug | True | 0 | True | True | True | 21032.2 | 4152.3 | 222.7 | 323 | 797 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_policy_007 | bug_debug | True | 0 | True | True | True | 33321.7 | 3993.9 | 222.7 | 407 | 808 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_json_008 | bug_debug | True | 0 | True | True | True | 20621.5 | 4552.4 | 222.7 | 329 | 816 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_budget_009 | bug_debug | False | 0 | True | False | True | 30704.1 | 4455.3 | 222.7 | 429 | 838 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | bug_router_010 | bug_debug | True | 0 | True | True | True | 15272.1 | 4049.4 | 222.7 | 363 | 790 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_011 | project_context | True | 0 | True | True | True | 20040.3 | 4082.5 | 222.7 | 402 | 805 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_012 | project_context | True | 0 | True | True | True | 26236.6 | 4326.6 | 222.7 | 419 | 808 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_013 | project_context | True | 0 | True | True | True | 29954.1 | 4287.3 | 222.7 | 417 | 807 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_014 | project_context | True | 0 | True | True | True | 20095.1 | 4191.8 | 222.7 | 523 | 853 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_015 | project_context | True | 0 | True | True | True | 14064.6 | 4387.4 | 222.7 | 308 | 794 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_task_016 | memory_dependent | True | 0 | True | True | True | 13771.0 | 4432.7 | 222.7 | 290 | 776 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_task_017 | memory_dependent | True | 0 | True | True | True | 13068.0 | 3795.0 | 222.7 | 287 | 779 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_task_018 | memory_dependent | True | 0 | True | True | True | 12725.1 | 4250.0 | 222.7 | 272 | 772 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | policy_task_019 | policy_context_constraint | True | 0 | True | True | True | 12366.8 | 4311.9 | 222.7 | 431 | 798 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | policy_task_020 | policy_context_constraint | False | 0 | True | True | False | 31339.7 | 3857.0 | 222.7 | 432 | 812 | 0 | 0 | 0 | 0 | 0 |
| aider_oacs_fork | edit_slugify_001 | simple_code_edit | False | 0 | True | False | True | 20952.0 | 4040.4 | 222.7 | 319 | 795 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | edit_math_002 | simple_code_edit | True | 0 | True | True | True | 21043.2 | 4168.6 | 222.7 | 273 | 784 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | edit_config_003 | simple_code_edit | True | 0 | True | True | True | 28615.8 | 4202.1 | 222.7 | 329 | 806 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | edit_readme_004 | simple_code_edit | False | 0 | True | True | False | 8963.1 | 4101.0 | 222.7 | 144 | 719 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | edit_parser_005 | simple_code_edit | True | 0 | True | True | True | 17507.8 | 4316.0 | 222.7 | 312 | 783 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | bug_cache_006 | bug_debug | True | 0 | True | True | True | 19249.7 | 3944.9 | 222.7 | 323 | 797 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | bug_policy_007 | bug_debug | True | 0 | True | True | True | 29175.7 | 5337.0 | 222.7 | 407 | 1100 | 2 | 0 | 1 | 189 | 0 |
| aider_oacs_fork | bug_json_008 | bug_debug | True | 0 | True | True | True | 29662.7 | 4010.7 | 223.0 | 329 | 816 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | bug_budget_009 | bug_debug | False | 0 | True | False | True | 27353.0 | 4635.3 | 223.0 | 429 | 838 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | bug_router_010 | bug_debug | True | 0 | True | True | True | 12603.1 | 4132.5 | 223.0 | 363 | 790 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | project_context_011 | project_context | True | 0 | True | True | True | 21089.3 | 4969.4 | 223.0 | 402 | 1100 | 1 | 0 | 1 | 171 | 0 |
| aider_oacs_fork | project_context_012 | project_context | True | 0 | True | True | True | 18613.2 | 5475.9 | 232.4 | 419 | 1100 | 2 | 0 | 1 | 183 | 0 |
| aider_oacs_fork | project_context_013 | project_context | True | 0 | True | True | True | 29517.9 | 5358.2 | 232.4 | 417 | 1100 | 2 | 0 | 1 | 187 | 0 |
| aider_oacs_fork | project_context_014 | project_context | True | 0 | True | True | True | 18990.0 | 4287.7 | 232.4 | 523 | 853 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | project_context_015 | project_context | True | 0 | True | True | True | 13431.1 | 5007.6 | 232.4 | 308 | 1100 | 1 | 0 | 1 | 171 | 0 |
| aider_oacs_fork | memory_task_016 | memory_dependent | True | 0 | True | True | True | 15632.2 | 4836.5 | 232.4 | 290 | 1000 | 1 | 0 | 1 | 173 | 0 |
| aider_oacs_fork | memory_task_017 | memory_dependent | True | 0 | True | True | True | 12527.6 | 4850.9 | 232.4 | 287 | 1000 | 1 | 0 | 1 | 176 | 0 |
| aider_oacs_fork | memory_task_018 | memory_dependent | True | 0 | True | True | True | 11840.9 | 5079.0 | 232.4 | 272 | 1000 | 1 | 0 | 1 | 176 | 0 |
| aider_oacs_fork | policy_task_019 | policy_context_constraint | True | 0 | True | True | True | 20708.7 | 5359.4 | 232.4 | 431 | 1100 | 2 | 0 | 1 | 187 | 0 |
| aider_oacs_fork | policy_task_020 | policy_context_constraint | True | 0 | True | True | True | 29557.8 | 5468.4 | 232.4 | 432 | 932 | 2 | 0 | 1 | 85 | 0 |

## Summary

- `aider_direct`: success 16/20, avg latency 21751.1 ms, avg cpu 4229.9 ms, avg context chars 350.4, acs calls 0, OACS skip/inject 0/0
- `aider_oacs_fork`: success 17/20, avg latency 20351.7 ms, avg cpu 4679.1 ms, avg context chars 350.4, acs calls 15, OACS skip/inject 10/10
