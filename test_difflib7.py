import itertools
import difflib

# Wait, if we use difflib to replace `all(x not in modifiedElement for x in permutations)`,
# What is the actual logical goal?
# The goal is to check if `particle` is NOT part of a larger `particle_other` construct in `modifiedElement`.
# BUT since the strings could be "fuzzy" (e.g. `particle` could be slightly modified, or `other` could be slightly modified), `x not in modifiedElement` might miss the fact that `particle` is indeed adjacent to `other` but separated by a small modification.
# So we want to see if `modifiedElement` CONTAINS a fuzzy match of ANY permutation.

def fuzzy_match(permutation, modifiedElement):
    # e.g., using SequenceMatcher or get_close_matches?
    # get_close_matches(word, possibilities) expects possibilities to be a list of words.
    # What if we split modifiedElement into chunks?
    # Or, we can just use difflib.get_close_matches(permutation, [modifiedElement])? No, modifiedElement is large.
    pass
