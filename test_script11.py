import sys
import collections

Counter = collections.Counter

# Another case for double modification:
# Let's say reactant is 'A_B_C'
# And A, B, C are base molecules.
# modifiedElementsPerCandidate could be something like:
# [[('A', 'A_B'), ('B', 'A_B'), ('A_B', 'A_B_C'), ('C', 'A_B_C')]]
# What if it's two separate modifications of the same element in a complex?
# e.g., complex is `A_A`. We have `A_P_A_P`.
# reactant = 'A_P_A_P'
# tmpCandidate = ['A', 'A']
# modifiedElementsPerCandidate = [[('A', 'A_P'), ('A', 'A_P')]]
# The loop:
modifiedElementsPerCandidate = [[("A", "A_P"), ("A", "A_P")]]
reactant = "A_P_A_P"

newModifiedElements = {}
modifiedElementsCounters = [Counter() for x in range(len(modifiedElementsPerCandidate))]

for idx, modifiedElementsInCandidate in enumerate(modifiedElementsPerCandidate):
    for element in modifiedElementsInCandidate:
        if element[0] not in newModifiedElements or element[1] == reactant:
            newModifiedElements[element[0]] = element[1]
        modifiedElementsCounters[idx][element[0]] += 1

print("Dict:", newModifiedElements)
print("Counters:", modifiedElementsCounters)

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

print("Result:", tmpCandidates)
