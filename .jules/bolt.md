## 2023-10-25 - [Optimize set operations for performance]
**Learning:** Checking for membership using `if x not in [list comprehension]` recreates the list each iteration, resulting in O(N*M) time complexity.
**Action:** Extract list comprehensions into sets precomputed outside loops (`my_set = {y for y in items}`) and then test membership in O(1) time.
