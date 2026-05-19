# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_direct | edit_slugify_001 | simple_code_edit | False | 0 | True | False | True | 22780.5 | 4264.7 | 213.5 | 319 | 795 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | edit_math_002 | simple_code_edit | True | 0 | True | True | True | 20579.0 | 4185.1 | 213.5 | 273 | 784 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | edit_config_003 | simple_code_edit | True | 0 | True | True | True | 28524.9 | 4073.1 | 218.2 | 329 | 806 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | edit_readme_004 | simple_code_edit | False | 0 | True | True | False | 8794.2 | 4358.8 | 218.5 | 144 | 719 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | edit_parser_005 | simple_code_edit | True | 0 | True | True | True | 18466.6 | 4190.4 | 218.5 | 312 | 783 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_cache_006 | bug_debug | True | 0 | True | True | True | 14900.8 | 3977.4 | 218.5 | 323 | 797 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_policy_007 | bug_debug | True | 0 | True | True | True | 31785.3 | 4065.7 | 218.8 | 407 | 808 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_json_008 | bug_debug | True | 0 | True | True | True | 31654.6 | 4364.0 | 218.8 | 329 | 816 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_budget_009 | bug_debug | False | 0 | True | False | True | 28228.2 | 4427.3 | 218.8 | 429 | 838 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | bug_router_010 | bug_debug | True | 0 | True | True | True | 14238.2 | 4132.2 | 218.8 | 363 | 790 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_011 | project_context | True | 0 | True | True | True | 18674.6 | 4485.6 | 218.8 | 402 | 805 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_012 | project_context | True | 0 | True | True | True | 26278.7 | 4171.5 | 219.9 | 419 | 808 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_013 | project_context | True | 0 | True | True | True | 32966.1 | 4543.6 | 219.9 | 417 | 807 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_014 | project_context | True | 0 | True | True | True | 21022.8 | 4195.2 | 219.9 | 523 | 853 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | project_context_015 | project_context | True | 0 | True | True | True | 17715.7 | 3836.2 | 219.9 | 308 | 794 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_task_016 | memory_dependent | True | 0 | True | True | True | 10232.5 | 4060.8 | 219.9 | 290 | 776 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_task_017 | memory_dependent | True | 0 | True | True | True | 11662.6 | 4370.1 | 219.9 | 287 | 779 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_task_018 | memory_dependent | True | 0 | True | True | True | 10908.9 | 4410.1 | 219.9 | 272 | 772 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | policy_task_019 | policy_context_constraint | True | 0 | True | True | True | 11510.5 | 4465.0 | 223.5 | 431 | 798 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | policy_task_020 | policy_context_constraint | False | 0 | True | True | False | 31208.6 | 4079.6 | 223.5 | 432 | 812 | 0 | 0 | 0 | 0 | 0 |
| aider_oacs_fork | edit_slugify_001 | simple_code_edit | False | 0 | True | False | True | 22052.9 | 4153.5 | 223.5 | 319 | 795 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | edit_math_002 | simple_code_edit | True | 0 | True | True | True | 21989.9 | 4489.0 | 223.5 | 273 | 784 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | edit_config_003 | simple_code_edit | True | 0 | True | True | True | 27193.4 | 4435.7 | 223.5 | 329 | 806 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | edit_readme_004 | simple_code_edit | False | 0 | True | True | False | 9022.5 | 4253.9 | 223.5 | 144 | 719 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | edit_parser_005 | simple_code_edit | True | 0 | True | True | True | 27968.4 | 3909.5 | 223.5 | 312 | 783 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | bug_cache_006 | bug_debug | True | 0 | True | True | True | 14790.8 | 4446.9 | 223.5 | 323 | 797 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | bug_policy_007 | bug_debug | True | 0 | True | True | True | 26646.6 | 5496.0 | 223.5 | 407 | 1100 | 2 | 0 | 1 | 189 | 0 |
| aider_oacs_fork | bug_json_008 | bug_debug | True | 0 | True | True | True | 29929.3 | 4090.0 | 223.5 | 329 | 816 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | bug_budget_009 | bug_debug | False | 0 | True | False | True | 26768.7 | 4375.6 | 223.5 | 429 | 838 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | bug_router_010 | bug_debug | True | 0 | True | True | True | 12064.2 | 4226.1 | 226.0 | 363 | 790 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | project_context_011 | project_context | False | 0 | False | False | False | 33268.1 | 4911.2 | 226.0 | 402 | 1100 | 1 | 0 | 1 | 171 | 1 |
| aider_oacs_fork | project_context_012 | project_context | True | 0 | True | True | True | 25828.9 | 5717.1 | 226.0 | 419 | 1100 | 2 | 0 | 1 | 183 | 0 |
| aider_oacs_fork | project_context_013 | project_context | True | 0 | True | True | True | 18666.0 | 5478.7 | 226.0 | 417 | 1100 | 2 | 0 | 1 | 231 | 0 |
| aider_oacs_fork | project_context_014 | project_context | True | 0 | True | True | True | 27081.4 | 4391.8 | 226.0 | 523 | 853 | 0 | 1 | 0 | 0 | 0 |
| aider_oacs_fork | project_context_015 | project_context | True | 0 | True | True | True | 15124.9 | 4951.1 | 226.0 | 308 | 1100 | 1 | 0 | 1 | 171 | 0 |
| aider_oacs_fork | memory_task_016 | memory_dependent | True | 0 | True | True | True | 13900.7 | 4677.9 | 226.0 | 290 | 1100 | 1 | 0 | 1 | 173 | 0 |
| aider_oacs_fork | memory_task_017 | memory_dependent | True | 0 | True | True | True | 11817.4 | 5054.1 | 226.0 | 287 | 1100 | 1 | 0 | 1 | 176 | 0 |
| aider_oacs_fork | memory_task_018 | memory_dependent | True | 0 | True | True | True | 10912.6 | 4869.3 | 226.0 | 272 | 1100 | 1 | 0 | 1 | 176 | 0 |
| aider_oacs_fork | policy_task_019 | policy_context_constraint | True | 0 | True | True | True | 12577.3 | 5242.2 | 226.0 | 431 | 1100 | 2 | 0 | 1 | 187 | 0 |
| aider_oacs_fork | policy_task_020 | policy_context_constraint | True | 0 | True | True | True | 47072.9 | 5666.9 | 226.0 | 432 | 946 | 2 | 0 | 1 | 85 | 0 |

## Summary

- `aider_direct`: success 16/20, avg latency 20606.7 ms, avg cpu 4232.8 ms, avg context chars 350.4, acs calls 0, OACS skip/inject 0/0
- `aider_oacs_fork`: success 16/20, avg latency 21733.8 ms, avg cpu 4741.8 ms, avg context chars 350.4, acs calls 15, OACS skip/inject 10/10
