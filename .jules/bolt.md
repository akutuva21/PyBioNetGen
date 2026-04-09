
## 2024-05-18 - Replacing list literals with set literals in membership checks
**Learning:** Checking membership (`in`) against a dynamically created list literal (e.g., `in ["A", "B"]`) inside a loop is suboptimal because Python creates a list every time and performs an O(n) search. Replacing the list literal with a set literal (`in {"A", "B"}`) allows Python's compiler to optimize it into checking against a `frozenset` constant. A `frozenset` lookup provides O(1) containment testing and completely avoids recreating the literal structure in memory during each iteration.
**Action:** Always use set literals (`{}`) instead of list literals (`[]`) for fixed collections of constants when performing membership checks in Python, especially within tight loops.
