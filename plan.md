# Plan for Refactoring getAssignmentRules

## Analysis of `getAssignmentRules` complexity
The `getAssignmentRules` method in `bionetgen/atomizer/sbml2bngl.py` (lines 2323-2678) is extremely long and has extensive duplicated code.
Specifically:
1. **Handling Rate Rules (`isRate == True`)**:
   - Building `artificialReactions` duplicates the `rxn_str = writer.bnglReaction(...)` call 4 times to handle cases of `rateLaw2 == "0"` vs `rateLaw2 != "0"` and `useID == True` vs `useID == False`.
2. **Handling Assignment Rules (`isAssignment == True`)**:
   - The logic for defining an assignment rule as an artificial observable is duplicated many times across multiple `if/elif/else` branches (`rawArule[0] in zRules`, `rawArule[0] in molecules`, `rawArule[0] in observablesDict`, etc.).
   - The chunk:
     ```python
     artificialObservables[target_name + "_ar"] = writer.bnglFunction(
         rawArule[1][0],
         rawArule[0] + "_ar()",
         [],
         compartments=compartmentList,
         reactionDict=self.reactionDictionary,
     )
     self.arule_map[rawArule[0]] = target_name + "_ar"
     if target_name in observablesDict:
         observablesDict[target_name] = target_name + "_ar"
     for obs_k, obs_v in list(observablesDict.items()):
         if obs_v == target_name:
             observablesDict[obs_k] = target_name + "_ar"
     ```
     is repeated over and over (at least 6-7 times). Only the `target_name` varies (either `rawArule[0]` or `name`).

## Proposed Refactoring

1. **Create an inner helper method (or just a local helper function/lambda) inside or outside `getAssignmentRules` for the assignment rule tracking**:
   Let's create a local helper `def track_assignment_rule(target_name):` to handle updating `artificialObservables`, `self.arule_map`, and `observablesDict`. Wait, we can't do it inside without dealing with self state, but we can write a helper method `_track_assignment_rule` or just a local inner function. A local function `_track_assignment_rule(target_name)` inside `getAssignmentRules` is a very clean way since it captures the outer scope (like `artificialObservables`, `self.arule_map`, `observablesDict`, `writer`, `rawArule`, `compartmentList`, `self.reactionDictionary`). Or better yet, since the file is large, we can create a `__track_assignment_rule` or just refactor by collapsing the logic. Let's create an inner function:

```python
            def _track_assignment_rule(target_name):
                artificialObservables[target_name + "_ar"] = writer.bnglFunction(
                    rawArule[1][0],
                    rawArule[0] + "_ar()",
                    [],
                    compartments=compartmentList,
                    reactionDict=self.reactionDictionary,
                )
                self.arule_map[rawArule[0]] = target_name + "_ar"
                if target_name in observablesDict:
                    observablesDict[target_name] = target_name + "_ar"
                for obs_k, obs_v in list(observablesDict.items()):
                    if obs_v == target_name:
                        observablesDict[obs_k] = target_name + "_ar"
```

2. **Refactor Rate Law Reaction creation**:
   Collapse the 4 branches into a single flow that computes `molec_name`, `rate_str`, and `reversible`, and calls `writer.bnglReaction(...)` exactly once.

3. **Simplify Assignment Rule branches**:
   Use `_track_assignment_rule` instead of duplicating 15 lines of code every time.

4. **Verify correctness**: Run `PYTHONPATH=. python -m pytest tests/` to verify tests still pass.
