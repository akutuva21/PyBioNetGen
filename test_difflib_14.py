import difflib
import itertools

def is_viable_difflib(particle, partialAnalysis, modifiedElement):
    # Old way:
    permutations = [
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    ]
    # Check if ANY of the permutations are "in" modifiedElement
    # difflib.SequenceMatcher or get_close_matches?
    # Wait, the codebase has a `sequenceMatcher(a, b)` which ignores underscores.

    # What if we just use difflib.get_close_matches on the permutations against all substrings?
    pass
