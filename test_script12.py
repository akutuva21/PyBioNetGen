import sys
import collections

Counter = collections.Counter

# The FIXME comment says:
# FIXME:Fails if there is a double modification
# newModifiedElements = {}
# modifiedElementsCounters = [Counter() for x in range(len(candidates))]

# Fails if there is a double modification... of WHAT?
# If we have `('A', 'A_P1')` and `('A', 'A_P2')`.
# A single molecule 'A' is modified to 'A_P1' and 'A_P2'.
# If `newModifiedElements` only stores ONE mapping per element `element[0]`,
# then `newModifiedElements['A'] = 'A_P1'`. `A_P2` is lost.
# If `tmpCandidate` has `['A', 'A']`, one will become `A_P1` and the other will become `A_P1`.
# But they should be `A_P1` and `A_P2`!

modifiedElementsPerCandidate = [[("A", "A_P1"), ("A", "A_P2")]]
reactant = "A_P1_A_P2"

newModifiedElements = {}
modifiedElementsCounters = [Counter() for x in range(1)]

for idx, modifiedElementsInCandidate in enumerate(modifiedElementsPerCandidate):
    for element in modifiedElementsInCandidate:
        if element[0] not in newModifiedElements or element[1] == reactant:
            newModifiedElements[element[0]] = element[1]
        modifiedElementsCounters[idx][element[0]] += 1

print("Original dict:", newModifiedElements)
print("Original counters:", modifiedElementsCounters)

tmpCandidates = [["A", "A"]]

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

print("Original result:", tmpCandidates)

# --- The proposed fix using collections.defaultdict(list) ---

newModifiedElementsFix = collections.defaultdict(list)
modifiedElementsCountersFix = [Counter() for x in range(1)]

for idx, modifiedElementsInCandidate in enumerate(modifiedElementsPerCandidate):
    for element in modifiedElementsInCandidate:
        if element[1] == reactant:
            newModifiedElementsFix[element[0]].insert(0, element[1])
        else:
            newModifiedElementsFix[element[0]].append(element[1])
        modifiedElementsCountersFix[idx][element[0]] += 1

print("Fix dict:", newModifiedElementsFix)
print("Fix counters:", modifiedElementsCountersFix)

tmpCandidatesFix = [["A", "A"]]

for tmpCandidate, modifiedElementsCounter in zip(
    tmpCandidatesFix, modifiedElementsCountersFix
):
    flag = True
    while flag:
        flag = False
        for idx, chemical in enumerate(tmpCandidate):
            if modifiedElementsCounter[chemical] > 0:
                modifiedElementsCounter[chemical] -= 1
                mod = (
                    newModifiedElementsFix[chemical].pop(0)
                    if newModifiedElementsFix[chemical]
                    else chemical
                )
                tmpCandidate[idx] = mod
                flag = True
                break

print("Fix result:", tmpCandidatesFix)
