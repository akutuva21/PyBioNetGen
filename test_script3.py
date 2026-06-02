import sys
import collections

Counter = collections.Counter

# Simulation with double modification bug
candidates = [["A"]]
reactant = "A_P_P"
tmpCandidates = [["A"]]

# What actually happens when a double modification fails?
# In the original code, the FIXME says:
# FIXME:Fails if there is a double modification
# Let's say `modifiedElementsPerCandidate` is:
# [[('A', 'A_P'), ('A', 'A_P')]]
# And `tmpCandidate` is just `['A']`.
# `modifiedElementsCounter` has `Counter({'A': 2})`.

newModifiedElements = {"A": "A_P"}
tmpCandidate = ["A"]
modifiedElementsCounter = Counter({"A": 2})

flag = True
while flag:
    flag = False
    for idx, chemical in enumerate(tmpCandidate):
        if modifiedElementsCounter[chemical] > 0:
            modifiedElementsCounter[chemical] -= 1
            tmpCandidate[idx] = newModifiedElements[chemical]
            flag = True
            break

print("tmpCandidate after loop:", tmpCandidate)
