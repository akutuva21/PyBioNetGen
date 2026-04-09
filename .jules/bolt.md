## 2024-06-19 - [Optimize inner loop membership test in bnglWriter.py]
**Learning:** Using a list comprehension inside a list comprehension for membership tests results in an O(N^2) complexity because the inner list is re-created for every item in the outer list.
**Action:** Extract the inner list comprehension into a precomputed `set` literal/comprehension before the outer loop/comprehension. This changes the membership test to O(1) and eliminates redundant memory allocations, yielding significant performance gains (e.g., 39x speedup in this benchmark).
