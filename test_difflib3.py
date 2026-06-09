import itertools
import difflib

# Looking at analyzeSBML.py
# The FIXME says:
# FIXME: make sure we only do a search on those variables that are viable
# candidates. this is once again fuzzy string matchign. there should
# be a better way of doing this with difflib

def old_logic(partialAnalysis, particle, modifiedElement):
    permutations = {
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    }
    return all(x not in modifiedElement for x in permutations)


def new_logic(partialAnalysis, particle, modifiedElement):
    permutations = {
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    }

    # "make sure we only do a search on those variables that are viable candidates"
    # Wait, the issue might be that `x not in modifiedElement` is a strict substring check.
    # What if we use difflib.get_close_matches? Or SequenceMatcher?

    # Or, the issue is that iterating through all permutations of size 2 is not scaling, or just naive.
    # But partialAnalysis is usually small.
    # Wait, "viable candidates": maybe we should only check if there is a match in modifiedElement
    # with a high ratio?
    pass
