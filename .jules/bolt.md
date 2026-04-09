## 2024-05-15 - Optimize Loop Lookups
**Learning:** Checking for membership in a list generated via comprehension inside a tight loop creates an $O(N^2)$ bottleneck because the list is reallocated and populated every single time. Converting it to a set comprehension mapped *outside* of the loop reduces lookup to $O(1)$ and eliminates reallocation.
**Action:** When evaluating inner loop conditions, extract sequence comprehensions used for `in` checks to a pre-computed set outside the loop. Be mindful of updating the set dynamically if loop iterations modify the contents being queried.
