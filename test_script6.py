import sys
import collections

Counter = collections.Counter

# With double modification on the same base molecule,
# modifiedElementsPerCandidate = [[('A', 'A_P1'), ('A', 'A_P2')]]
# The user wants both modifications to be reflected in the final reactant, presumably.
# Wait, if both modifications are applied to 'A', then we want something that can apply multiple modifications.
# Wait, `newModifiedElements` maps 'A' to 'A_P1' only. The second modification is ignored or overwrites 'A_P1' if it was the reactant.
# Actually, if we just keep `newModifiedElements` as a list of modifications for each element, we could pop from it.

modifiedElementsPerCandidate = [[("A", "A_P1"), ("A", "A_P2")]]
candidates = [["A_P1_P2"]]
reactant = "A_P1_P2"
tmpCandidates = [
    ["A", "B"]
]  # suppose the complex was A_B, but A was modified twice. wait, if A is modified twice, is it ['A', 'A']?
