import difflib
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
            return False # meaning it IS in modifiedElement
    return True # meaning it is NOT in modifiedElement

print(check_viable("A", ["A", "B"], "A_mod_B"))
