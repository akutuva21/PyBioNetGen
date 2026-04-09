## 2025-04-09 - [Performance] Optimization of O(N^2) list comprehensions in Species.extend

**Learning:** When appending to a list inside a loop and checking `if element.name not in [x.name for x in self.components]`, creating the list comprehension on every iteration creates an O(N*M) lookup structure.
**Action:** Extract the property extraction to a set before the loop (`comp_names = {x.name for x in self.components}`) and then use O(1) set lookups (`if element.name not in comp_names`). Ensure you `add()` to the set when appending new elements to the list to keep the cache synchronized.
