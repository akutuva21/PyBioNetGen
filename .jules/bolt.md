## 2026-04-09 - [Optimize list comprehension membership tests]
**Learning:** [Generator expressions within `any()` save significant peak memory over list comprehensions during membership tests.]
**Action:** [Prefer `not any(x == target for x in iterable)` or explicit loops over `target not in [x for x in iterable]` to avoid full list materialization overhead.]
