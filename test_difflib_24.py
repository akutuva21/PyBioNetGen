import difflib

# In analyzeSpeciesModification2, fuzzy string matching is done by:
# sequenceMatcher = difflib.SequenceMatcher(None, token, tmpModifiedElement)
# match = "".join(...)
# if (len(match)) / float(len(token)) < 0.8:

# So, if we use the same technique for permutations in analyzeSpeciesModification:
import itertools

def check_viable(particle, partialAnalysis, modifiedElement):
    permutations = [
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    ]
    for perm in permutations:
        sequenceMatcher = difflib.SequenceMatcher(None, perm, modifiedElement)
        match = "".join(
            modifiedElement[j : j + n]
            for i, j, n in sequenceMatcher.get_matching_blocks()
            if n
        )
        if len(match) / float(len(perm)) >= 0.8:
            # Check if they are contiguous enough
            tmp = [i for i, y in enumerate(difflib.ndiff(perm, modifiedElement)) if not y.startswith("+")]
            if tmp[-1] - tmp[0] <= len(perm) + 5:
                return False # meaning it IS in modifiedElement
    return True # meaning it is NOT in modifiedElement

print(check_viable("A", ["A", "B"], "A_mod_B"))
print(check_viable("A", ["A", "B"], "C_mod_B"))
