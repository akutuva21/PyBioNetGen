import collections

Counter = collections.Counter

modifiedElementsPerCandidate = [[("A", "A_P1"), ("A_P1", "A_P1_P2")]]
reactant = "A_P1_P2"

newModifiedElements = {}
modifiedElementsCounters = [Counter() for x in range(len(modifiedElementsPerCandidate))]

for idx, modifiedElementsInCandidate in enumerate(modifiedElementsPerCandidate):
    for element in modifiedElementsInCandidate:
        if element[0] not in newModifiedElements or element[1] == reactant:
            newModifiedElements[element[0]] = element[1]
        modifiedElementsCounters[idx][element[0]] += 1

print("Original dict:", newModifiedElements)
print("Original counters:", modifiedElementsCounters)

tmpCandidates = [["A"]]

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
