## 2024-05-24 - Python Set vs List Literal Membership Performance
**Learning:** Python optimizes set literals containing constants to `frozenset` at compile time. Therefore, membership checks using `in {"A", "B"}` are $O(1)$ and significantly faster than `in ["A", "B"]` ($O(N)$ and incurs list creation overhead).
**Action:** Use set literals instead of list literals for all constant membership checks inside tight loops.
