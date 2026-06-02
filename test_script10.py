import collections
Counter = collections.Counter

# The FIXME says: FIXME:Fails if there is a double modification
# Let's say we have [('A', 'A_P1'), ('A', 'A_P2')] -> two independent modifications to the same molecule type 'A'
# For example, A_P1 is produced by A + P1, and A_P2 is produced by A + P2.
# Then maybe A_P1_P2 is produced by A_P1 + P2, or A_P2 + P1.
# BUT wait! If the dependency graph resolved A_P1_P2 directly into TWO modifications of 'A'?
# Wait, if `resolveDependencyGraph(withModifications=True)` returns a flat list of modifications...
# In `resolveSCT.py:984`: `mod = self.resolveDependencyGraph(dependencyGraph, chemical, True)`
# If `chemical` is `A_P1_P2`, and it resolves to base molecule `A`.
# Does `mod` contain `[('A', 'A_P1'), ('A_P1', 'A_P1_P2')]`? In that case it works.
# What if the graph is `A_P1_P2 -> A` directly, so `mod` is `[('A', 'A_P1_P2')]`? Then no double modification.
# What if it's `[('A', 'A_P1'), ('A', 'A_P2')]` but we only have one 'A' in tmpCandidates?
# No, if there is a double modification, maybe both modifications apply to the SAME instance, and we only capture one in `newModifiedElements`?
modifiedElementsPerCandidate = [[('A', 'A_P1'), ('A', 'A_P2')]]
reactant = 'A_P1_P2'

newModifiedElements = {}
for element in modifiedElementsPerCandidate[0]:
    if element[0] not in newModifiedElements or element[1] == reactant:
        newModifiedElements[element[0]] = element[1]

print("Dict if they both map from 'A':", newModifiedElements)
