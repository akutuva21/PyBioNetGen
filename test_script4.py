import sys
import collections
Counter = collections.Counter

# Another hypothesis: newModifiedElements mapping is overwritten.
# Suppose modifiedElementsPerCandidate is [[('A', 'A_P1'), ('A', 'A_P2')]]
# The loop doing `newModifiedElements[element[0]] = element[1]` will result in `newModifiedElements['A'] = 'A_P2'`
# And `modifiedElementsCounter['A']` will be 2.
# So tmpCandidate will replace two instances of 'A' with 'A_P2', ignoring 'A_P1'!
# What if `newModifiedElements` maps to a list? Or what if we apply modifications directly instead of aggregating first?
# The problem is `tmpCandidate` only contains ONE instance of 'A' but it's supposed to get 2 modifications?
# No, `for element in rootChemical:` expands `chemical` into its base components.
# If `chemical` is a complex `A_B`, it gets expanded into `['A', 'B']`.
# If `chemical` was `A_P1_P2`, its `mod` might be `[('A', 'A_P1'), ('A', 'A_P2')]`? Wait, `resolveDependencyGraph(withModifications=True)` returns a list of modifications.

candidates = [['A_P1_P2']]
reactant = 'A_P1_P2'
tmpCandidates = [['A']]

modifiedElementsPerCandidate = [[('A', 'A_P1'), ('A_P1', 'A_P1_P2')]]
# In the loop:
newModifiedElements = {}
modifiedElementsCounters = [Counter() for x in range(len(candidates))]

for idx, modifiedElementsInCandidate in enumerate(
    modifiedElementsPerCandidate
):
    for element in modifiedElementsInCandidate:
        if element[0] not in newModifiedElements or element[1] == reactant:
            newModifiedElements[element[0]] = element[1]
        modifiedElementsCounters[idx][element[0]] += 1

print("newModifiedElements:", newModifiedElements)

for tmpCandidate, modifiedElementsCounter in zip(
    tmpCandidates, modifiedElementsCounters
):
    flag = True
    while flag:
        flag = False
        for idx, chemical in enumerate(tmpCandidate):
            if modifiedElementsCounter[chemical] > 0:
                modifiedElementsCounter[chemical] -= 1
                tmpCandidate[idx] = newModifiedElements[chemical]
                flag = True
                break

print("tmpCandidate after:", tmpCandidate)
