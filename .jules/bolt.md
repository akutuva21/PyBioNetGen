## 2024-05-24 - O(N^2) Loop List Comprehension Optimization
**Learning:** Checking membership inside a loop against a re-created list via comprehension creates an O(N*M) bottleneck.
**Action:** Extract membership collections into O(1) sets before the loop, and ensure newly added items are also appended to the set to maintain consistency with the loop's original dynamic evaluation behavior.
