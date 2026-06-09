import itertools
import difflib

def distanceToModification(particle, comparisonElement, translationKey):
    return 1 # dummy

def test_function(partialAnalysis, modifiedElement, particle):
    permutations = {
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    }
    old_ans = all(x not in modifiedElement for x in permutations)

    # "make sure we only do a search on those variables that are viable candidates. this is once again fuzzy string matchign. there should be a better way of doing this with difflib"

    # What if we use difflib to see if `particle` is standalone vs joined with something else?
    # If the user means we should use get_close_matches instead of exact permutation checks,
    # Maybe we should check if there's any close match of `particle_something` in modifiedElement?

    # Actually, difflib get_close_matches:
    # "difflib.get_close_matches(word, possibilities, n=3, cutoff=0.6)"

    # Wait, permutations are all pairs where the first element is `particle`.
    # `x not in modifiedElement for x in permutations`
    # What if we use `difflib.get_close_matches`?
    # the comment says "this is once again fuzzy string matchign" and "difflib"

    # If we look at how permutations are built, it is building strings to see if the particle is adjacent to another particle.
    # What if modifiedElement has a modified version of the other particle, so exact match fails?
    # "make sure we only do a search on those variables that are viable candidates"
    pass
