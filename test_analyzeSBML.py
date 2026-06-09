import itertools
import difflib

def old_logic(partialAnalysis, particle, modifiedElement):
    permutations = {
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    }
    return all(x not in modifiedElement for x in permutations)

# "make sure we only do a search on those variables that are viable candidates. this is once again fuzzy string matchign. there should be a better way of doing this with difflib"
# What if we just split the modified element into chunks, and get close matches for the permutations?
# Or maybe:
def new_logic(partialAnalysis, particle, modifiedElement):
    permutations = {
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    }
    parts = modifiedElement.split('_')
    # get all contiguous chunks
    modified_parts = ['_'.join(parts[i:j]) for i in range(len(parts)) for j in range(i+1, len(parts)+1)]
    # Or, perhaps difflib.get_close_matches(perm, modified_parts)

    # Wait, the problem with the original is that if `modifiedElement` is `A_B_modified_C`, `A_B` is in it!
    # Because `A_B` is a substring. The original logic works well for exact substrings.
    # What if `modifiedElement` is `A_modified_B_C`? `A_B` is not a substring!
    # BUT `A` and `B` are in there, separated by `modified`. So it IS adjacent in the original complex.
    # So `x not in modifiedElement` would be True, meaning we do the search, which is what we want?
    # Wait, if `x not in modifiedElement`, it means `A_B` is not there. So it calculates distance.
    # If `x in modifiedElement`, it DOES NOT calculate distance.

    pass
