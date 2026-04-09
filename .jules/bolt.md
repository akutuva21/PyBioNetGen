## 2024-05-18 - Set-based optimization for List Comprehensions inside Loops
**Learning:** List comprehensions computed repeatedly inside a loop (`if item not in [x.name for x in collection]`) result in O(N^2) time complexity. Using a set for membership checking reduces this to O(N).
**Action:** When performing membership tests inside loops, precompute a set of keys before the loop for O(1) lookups. If the underlying collection grows during the loop, explicitly add new items to the set to maintain consistency with the original logic.
