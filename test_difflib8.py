import difflib

# In Python, difflib has:
# difflib.get_close_matches(word, possibilities, n=3, cutoff=0.6)

def replace_with_difflib(particle, partialAnalysis, modifiedElement):
    # Instead of building permutations and checking if they are substrings,
    # what if we use get_close_matches?

    # We want to check if `particle` has any permutation that closely matches a part of `modifiedElement`.
    pass
