# Coding Agent OACS Benchmark

| mode | task | category | success | exit | patch | tests | checks | latency_ms | cpu_ms | rss_mb | context_chars | prompt_tokens_est | acs_calls | oacs_skip | oacs_inject | oacs_tokens | hallucinated_refs |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| aider_direct | memory_seeded_001 | memory_seeded | False | 0 | False | False | True | 25303.1 | 4355.9 | 210.6 | 190 | 716 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | memory_seeded_002 | memory_seeded | False | 0 | False | False | True | 27180.5 | 4333.8 | 211.7 | 207 | 716 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_003 | memory_seeded | False | 0 | True | False | True | 39427.8 | 4328.0 | 219.4 | 218 | 722 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | memory_seeded_004 | memory_seeded | False | 0 | False | False | True | 19759.1 | 3818.7 | 219.4 | 198 | 714 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_005 | memory_seeded | False | 0 | False | False | True | 10101.1 | 4356.3 | 220.2 | 201 | 718 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_006 | memory_seeded | False | 0 | False | False | True | 34586.6 | 4199.6 | 221.8 | 198 | 724 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_007 | memory_seeded | False | 0 | False | False | True | 33264.2 | 4587.7 | 221.8 | 175 | 714 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_008 | memory_seeded | False | 0 | False | False | True | 11776.4 | 4192.3 | 221.8 | 229 | 723 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_009 | memory_seeded | False | 0 | True | True | False | 23742.1 | 4181.5 | 225.0 | 145 | 717 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_010 | memory_seeded | False | 0 | False | False | True | 43409.2 | 4192.4 | 225.0 | 190 | 717 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | memory_seeded_011 | memory_seeded | False | 0 | False | False | True | 23570.8 | 4518.9 | 225.0 | 199 | 722 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | memory_seeded_012 | memory_seeded | False | 0 | False | False | True | 30528.7 | 4234.4 | 225.0 | 181 | 721 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | memory_seeded_013 | memory_seeded | False | 0 | False | False | True | 27187.9 | 4164.6 | 225.0 | 190 | 716 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | memory_seeded_014 | memory_seeded | False | 0 | False | False | True | 34874.9 | 4512.6 | 225.0 | 196 | 716 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | memory_seeded_015 | memory_seeded | False | 0 | False | False | True | 28557.6 | 4167.0 | 225.0 | 199 | 714 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | memory_seeded_016 | memory_seeded | False | 0 | True | False | True | 32485.5 | 4049.2 | 225.0 | 173 | 720 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_017 | memory_seeded | False | 0 | False | False | True | 18300.2 | 4225.6 | 225.0 | 187 | 715 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_018 | memory_seeded | False | 0 | False | False | True | 26557.2 | 4096.9 | 225.0 | 195 | 713 | 0 | 0 | 0 | 0 | 1 |
| aider_direct | memory_seeded_019 | memory_seeded | False | 0 | False | False | True | 11053.8 | 4292.1 | 227.0 | 202 | 723 | 0 | 0 | 0 | 0 | 0 |
| aider_direct | memory_seeded_020 | memory_seeded | False | 0 | False | False | True | 39712.9 | 4442.4 | 227.0 | 239 | 724 | 0 | 0 | 0 | 0 | 0 |
| aider_oacs_fork | memory_seeded_001 | memory_seeded | True | 0 | True | True | True | 12409.4 | 5108.6 | 227.0 | 190 | 957 | 1 | 0 | 1 | 166 | 0 |
| aider_oacs_fork | memory_seeded_002 | memory_seeded | True | 0 | True | True | True | 11372.3 | 4934.2 | 227.0 | 207 | 976 | 1 | 0 | 1 | 179 | 0 |
| aider_oacs_fork | memory_seeded_003 | memory_seeded | True | 0 | True | True | True | 11986.8 | 4714.3 | 227.0 | 218 | 997 | 1 | 0 | 1 | 188 | 0 |
| aider_oacs_fork | memory_seeded_004 | memory_seeded | True | 0 | True | True | True | 11557.0 | 4984.8 | 227.0 | 198 | 958 | 1 | 0 | 1 | 164 | 0 |
| aider_oacs_fork | memory_seeded_005 | memory_seeded | True | 0 | True | True | True | 11398.7 | 5324.6 | 227.0 | 201 | 997 | 2 | 0 | 1 | 190 | 0 |
| aider_oacs_fork | memory_seeded_006 | memory_seeded | True | 0 | True | True | True | 11172.0 | 5057.4 | 227.0 | 198 | 992 | 1 | 0 | 1 | 179 | 0 |
| aider_oacs_fork | memory_seeded_007 | memory_seeded | True | 0 | True | True | True | 10587.8 | 4804.8 | 227.0 | 175 | 974 | 1 | 0 | 1 | 170 | 0 |
| aider_oacs_fork | memory_seeded_008 | memory_seeded | True | 0 | True | True | True | 11449.2 | 5179.6 | 227.0 | 229 | 1000 | 2 | 0 | 1 | 193 | 0 |
| aider_oacs_fork | memory_seeded_009 | memory_seeded | True | 0 | True | True | True | 10950.6 | 4686.2 | 227.0 | 145 | 991 | 1 | 0 | 1 | 187 | 0 |
| aider_oacs_fork | memory_seeded_010 | memory_seeded | True | 0 | True | True | True | 10650.9 | 4996.1 | 227.0 | 190 | 982 | 1 | 0 | 1 | 182 | 0 |
| aider_oacs_fork | memory_seeded_011 | memory_seeded | True | 0 | True | True | True | 11945.8 | 4986.7 | 227.0 | 199 | 1000 | 1 | 0 | 1 | 187 | 0 |
| aider_oacs_fork | memory_seeded_012 | memory_seeded | True | 0 | True | True | True | 11528.1 | 5030.8 | 227.0 | 181 | 986 | 1 | 0 | 1 | 170 | 0 |
| aider_oacs_fork | memory_seeded_013 | memory_seeded | True | 0 | True | True | True | 13286.6 | 4455.9 | 227.0 | 190 | 978 | 1 | 0 | 1 | 179 | 0 |
| aider_oacs_fork | memory_seeded_014 | memory_seeded | True | 0 | True | True | True | 12428.8 | 4942.2 | 227.0 | 196 | 976 | 1 | 0 | 1 | 170 | 0 |
| aider_oacs_fork | memory_seeded_015 | memory_seeded | True | 0 | True | True | True | 11298.3 | 4757.7 | 227.0 | 199 | 974 | 1 | 0 | 1 | 170 | 1 |
| aider_oacs_fork | memory_seeded_016 | memory_seeded | True | 0 | True | True | True | 10571.6 | 4910.6 | 227.0 | 173 | 978 | 1 | 0 | 1 | 170 | 0 |
| aider_oacs_fork | memory_seeded_017 | memory_seeded | True | 0 | True | True | True | 11340.1 | 5483.9 | 227.0 | 187 | 995 | 2 | 0 | 1 | 190 | 0 |
| aider_oacs_fork | memory_seeded_018 | memory_seeded | True | 0 | True | True | True | 11026.9 | 5354.5 | 227.0 | 195 | 979 | 2 | 0 | 1 | 179 | 0 |
| aider_oacs_fork | memory_seeded_019 | memory_seeded | True | 0 | True | True | True | 10913.9 | 5084.1 | 227.0 | 202 | 990 | 1 | 0 | 1 | 173 | 0 |
| aider_oacs_fork | memory_seeded_020 | memory_seeded | True | 0 | True | True | True | 11668.9 | 5046.2 | 227.0 | 239 | 998 | 1 | 0 | 1 | 179 | 0 |

## Summary

- `aider_direct`: success 0/20, avg latency 27069.0 ms, avg cpu 4262.5 ms, avg context chars 195.6, acs calls 0, OACS skip/inject 0/0
- `aider_oacs_fork`: success 20/20, avg latency 11477.2 ms, avg cpu 4992.2 ms, avg context chars 195.6, acs calls 24, OACS skip/inject 0/20
