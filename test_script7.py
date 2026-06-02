import collections
Counter = collections.Counter

modifiedElementsPerCandidate = [[('A', 'A_P1'), ('A', 'A_P2')]]
reactant = 'A_P1_P2'

# What if we use a list for newModifiedElements to store multiple modifications?
newModifiedElements = collections.defaultdict(list)
modifiedElementsCounters = [Counter() for x in range(len(modifiedElementsPerCandidate))]

for idx, modifiedElementsInCandidate in enumerate(modifiedElementsPerCandidate):
    for element in modifiedElementsInCandidate:
        # If there are multiple modifications to the same element, we might append all of them.
        # How to handle the priority of element[1] == reactant?
        if element[1] == reactant:
            newModifiedElements[element[0]].insert(0, element[1])
        else:
            newModifiedElements[element[0]].append(element[1])
        modifiedElementsCounters[idx][element[0]] += 1

print(newModifiedElements)

tmpCandidates = [['A', 'A']]

for tmpCandidate, modifiedElementsCounter in zip(tmpCandidates, modifiedElementsCounters):
    flag = True
    while flag:
        flag = False
        for idx, chemical in enumerate(tmpCandidate):
            if modifiedElementsCounter[chemical] > 0:
                modifiedElementsCounter[chemical] -= 1
                # pop from the list of modifications
                mod = newModifiedElements[chemical].pop(0) if newModifiedElements[chemical] else chemical
                tmpCandidate[idx] = mod
                flag = True
                break

print(tmpCandidates)
