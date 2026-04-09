## 2024-05-24 - Optimize list comprehensions in loops
**Learning:** O(N) list comprehensions generated repeatedly within a loop (e.g. `[x.name for x in items]`) severely degrade performance to O(N^2) or worse.
**Action:** Extract list comprehensions to pre-computed sets or dictionaries outside the loop, especially in critical paths. Ensure the sets/dicts are properly updated within the loop if new items are appended.
