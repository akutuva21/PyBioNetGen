## 2025-02-28 - Optimize List Comprehension in Loops
**Learning:** Instantiating a list comprehension on every iteration of an enclosing loop to perform `x not in [...]` membership tests transforms an O(N) loop into an O(N^2) trap, causing unnecessary and heavy runtime costs.
**Action:** Extract membership data into a pre-computed `set()` before the loop. If the tracked object is mutated inside the loop, dynamically add newly inserted items to the set (`my_set.add(item)`) to maintain O(1) checking cost while preserving correctness.
