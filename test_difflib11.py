import difflib
import itertools

def check_old(partialAnalysis, modifiedElement, particle):
    permutations = {
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    }
    return all(x not in modifiedElement for x in permutations)

def check_new(partialAnalysis, modifiedElement, particle):
    permutations = [
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    ]
    # Use get_close_matches to see if modifiedElement contains a fuzzy match of permutations.
    # Instead of "x not in modifiedElement", we do:
    # return not bool(get_close_matches(modifiedElement, permutations))
    # Or, checking if ANY permutation is closely matching modifiedElement.
    matches = difflib.get_close_matches(modifiedElement, permutations, cutoff=0.6)
    # wait, if modifiedElement is much longer, it might not match.
    # But wait, if modifiedElement is "A_B_modified_C", "A_B" length is 3, modifiedElement is 14.
    # ratio = 2 * 3 / (3 + 14) = 6 / 17 = 0.35, which is < 0.6!
    # So difflib.get_close_matches(modifiedElement, permutations) would be empty!
    return len(matches) == 0

print(check_old(['A', 'B', 'C'], 'A_B_modified_C', 'A'))
print(check_new(['A', 'B', 'C'], 'A_B_modified_C', 'A'))
