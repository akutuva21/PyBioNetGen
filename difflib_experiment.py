import difflib

def is_viable_difflib(particle, partialAnalysis, modifiedElement):
    permutations = [
        "_".join(x)
        for x in set(itertools.permutations(partialAnalysis, 2))
        if x[0] == particle
    ]
    # what if we try to see if modifiedElement has a match for any permutation?
    pass
