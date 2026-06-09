import difflib

# In analyzeSpeciesModification2, fuzzy search uses difflib.SequenceMatcher:
# sequenceMatcher = difflib.SequenceMatcher(None, token, tmpModifiedElement)
# match = "".join(...)
# if (len(match)) / float(len(token)) < 0.8: ...

# We could do something very similar for permutations in analyzeSpeciesModification!
# Instead of `all(x not in modifiedElement for x in permutations)`,
# For each perm, we do SequenceMatcher against modifiedElement.
# If `len(match) / len(perm) >= 0.8` (or something similar), then it IS in modifiedElement.
# BUT wait! If it's a permutation like "EGF_EGFR", we want to know if it's there.
# If `A_B` matches `A_modified_B_C` as `A_B`, length of match is 3, length of perm is 3.
# So `len(match)/len(perm)` is 1.0!

permutations = ["A_B"]
modifiedElement = "A_modified_B_C"

def check_new_3(permutations, modifiedElement):
    for perm in permutations:
        matcher = difflib.SequenceMatcher(None, perm, modifiedElement)
        match = "".join(modifiedElement[j : j + n] for i, j, n in matcher.get_matching_blocks() if n)
        if len(match) / float(len(perm)) >= 0.8:
            # Wait, `match` is the sum of ALL matching blocks!
            # If `perm` is `A_B`, matching blocks might be `A` and `_B`. So `A_B`.
            # BUT wait, what if the blocks are far apart?
            # In analyzeSpeciesModification2:
            # tmp = [i for i, y in enumerate(difflib.ndiff(token, tmpModifiedElement)) if not y.startswith("+")]
            # if tmp[-1] - tmp[0] > len(token) + 5: # check if they are far apart!

            # This is exactly what "fuzzy string matchign" comment means!
            # It means we should use difflib to see if `x` is in `modifiedElement` fuzzily!
            # Let's test difflib.get_close_matches again. What if we split modifiedElement? No.
            pass
