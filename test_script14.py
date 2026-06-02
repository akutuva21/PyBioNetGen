import sys
from collections import Counter, defaultdict

# The code reviewer noted:
# The patch correctly identifies that a list (or queue) is needed to store multiple modifications for the same element, rather than overwriting a single dictionary key. However, the logic is deeply flawed. newModifiedElements is initialized as a single dictionary shared across all candidates. Because the application loop uses .pop(0), it mutates this shared queue. If two candidates apply modifications to the same base molecule, they will consume each other's modifications.
# AND
# To fix this properly, newModifiedElements needs to be created on a per-candidate basis (e.g., newModifiedElements = [defaultdict(list) for _ in candidates]).

# In original code:
# modifiedElementsCounters = [Counter() for x in range(len(candidates))]
# for idx, modifiedElementsInCandidate in enumerate(modifiedElementsPerCandidate):
#   # modifiedElementsPerCandidate is created by iterating over candidates!
#   # len(modifiedElementsPerCandidate) <= len(candidates)
#   # wait, it's appended inside a try/except block, so some candidates might be skipped!
#   # In resolveSCT.py line 998: modifiedElementsPerCandidate.append(modifiedElements)
#   # But wait, original code iterates:
#   # modifiedElementsCounters = [Counter() for x in range(len(candidates))]
#   # for idx, modifiedElementsInCandidate in enumerate(modifiedElementsPerCandidate):
#   #     for element in modifiedElementsInCandidate:
#   #         newModifiedElements[element[0]] = element[1] # THIS WAS A SINGLE DICT
#   #         modifiedElementsCounters[idx][element[0]] += 1
#   # So modifiedElementsCounters was based on `len(candidates)`, but `idx` goes up to `len(modifiedElementsPerCandidate) - 1`.
#   # wait! candidates is NOT modified! BUT `tmpCandidates` is appended.
#   # The code actually does:
#   # for idx, modifiedElementsInCandidate in enumerate(modifiedElementsPerCandidate):
#   # So idx maps to modifiedElementsPerCandidate, which corresponds exactly to tmpCandidates.
#   # But modifiedElementsCounters = [Counter() for x in range(len(candidates))] creates enough for `candidates`, which might be MORE than `tmpCandidates`.
#   # And then: zip(tmpCandidates, modifiedElementsCounters) ignores the extra.

candidates = [['A_P1_P2']]
reactant = 'A_P1_P2'
tmpCandidates = [['A', 'A']]

modifiedElementsPerCandidate = [
    [('A', 'A_P1'), ('A', 'A_P2')]
]

newModifiedElements = [defaultdict(list) for x in range(len(candidates))]
modifiedElementsCounters = [Counter() for x in range(len(candidates))]

for idx, modifiedElementsInCandidate in enumerate(modifiedElementsPerCandidate):
    for element in modifiedElementsInCandidate:
        if element[1] == reactant:
            newModifiedElements[idx][element[0]].insert(0, element[1])
        else:
            newModifiedElements[idx][element[0]].append(element[1])
        modifiedElementsCounters[idx][element[0]] += 1

print(newModifiedElements)
print(modifiedElementsCounters)

for idx, (tmpCandidate, modifiedElementsCounter) in enumerate(zip(
    tmpCandidates, modifiedElementsCounters
)):
    flag = True
    while flag:
        flag = False
        for cidx, chemical in enumerate(tmpCandidate):
            if modifiedElementsCounter[chemical] > 0:
                modifiedElementsCounter[chemical] -= 1
                mod = newModifiedElements[idx][chemical].pop(0) if newModifiedElements[idx][chemical] else chemical
                tmpCandidate[cidx] = mod
                flag = True
                break

print(tmpCandidates)
