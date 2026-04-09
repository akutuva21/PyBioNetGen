## 2024-05-19 - Optimize `balanceTranslator` membership testing
**Learning:** Checking membership inside a loop with a freshly-constructed list comprehension gives an O(N * M) performance impact. Pre-computing a set of keys can reduce it to O(N + M).
**Action:** When finding a list membership test `x not in [y for y in Y]` inside a loop, elevate the inner list creation out of the loop and convert it to a `set` to reduce time complexity to O(1).
