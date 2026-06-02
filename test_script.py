import sys
import collections
Counter = collections.Counter

# Simulate the issue
candidates = [['A_P_P']]
reactant = 'A_P_P'
tmpCandidates = [['A']]
originalTmpCandidates = [['A']]

modifiedElementsPerCandidate = [[('A', 'A_P'), ('A', 'A_P')]] # Assuming A is double phosphorylated

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
print("modifiedElementsCounters:", modifiedElementsCounters)

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

print("tmpCandidates after:", tmpCandidates)
