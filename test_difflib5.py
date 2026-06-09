import difflib
import itertools

def get_viable(partialAnalysis, particle, modifiedElement):
    # Old implementation:
    permutations = {
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    }
    old_res = all(x not in modifiedElement for x in permutations)

    # What if we use difflib to find if there are close matches?
    # Or, difflib.get_close_matches(particle, partialAnalysis) to limit viable candidates?
    # Wait, permutations are built from partialAnalysis.
    # What if we get close matches of modifiedElement parts?
    pass
