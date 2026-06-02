import sys
import collections

Counter = collections.Counter

# If double modification means two independent modifications on the SAME base molecule?
candidates = [["A_P1_P2"]]
reactant = "A_P1_P2"
tmpCandidates = [["A"]]

# e.g., 'A_P1' is from 'A', and 'A_P2' is also from 'A'.
modifiedElementsPerCandidate = [[("A", "A_P1"), ("A", "A_P2")]]

newModifiedElements = {}
modifiedElementsCounters = [Counter() for x in range(len(candidates))]

for idx, modifiedElementsInCandidate in enumerate(modifiedElementsPerCandidate):
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

print("tmpCandidate after:", tmpCandidate)
