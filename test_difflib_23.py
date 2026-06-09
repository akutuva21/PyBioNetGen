import difflib

# How about `sequenceMatcher` that is defined in the file?
# sequenceMatcher ignores underscores in ratio.

# But we really want to know if `A` and `B` are nearby in `modifiedElement`.
# Wait, `get_close_matches` is used in the codebase like this:
# get_close_matches(word, possibilities)
# Maybe we get close matches of `permutations` among the substrings of `modifiedElement`?
# In analyzeSBML.py, `get_close_matches` is usually called with `dataset` being `species` or `strippedMolecules` which are lists of known molecules.

# The comment says: "there should be a better way of doing this with difflib"
# What if it means using `difflib.get_close_matches` against the list of `permutations`?
# NO, we want to check if ANY permutation is in `modifiedElement`.
# What if we use `get_close_matches(modifiedElement, permutations)`?
# If `modifiedElement` is longer, it won't match well.
# What if we use `difflib.SequenceMatcher.get_matching_blocks()`?

# "make sure we only do a search on those variables that are viable candidates. this is once again fuzzy string matchign."
# "there should be a better way of doing this with difflib"

def better_way(particle, partialAnalysis, modifiedElement):
    # What if we split modifiedElement?
    # No, what if we use get_close_matches(particle, partialAnalysis)?
    # NO!

    permutations = [
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    ]

    # OLD:
    # if all(x not in modifiedElement for x in permutations):

    # NEW:
    # We want to check if there is a fuzzy match.
    # What if we just use difflib.get_close_matches?
    # The signature is difflib.get_close_matches(word, possibilities, n=3, cutoff=0.6)
    pass
