import difflib

# In analyzeSpeciesModification:
# we have a `particle` which is one of the `partialAnalysis`.
# `baseElement` and `modifiedElement` are the components.
# `comparisonElement` = max(baseElement, modifiedElement, key=len) -> normally `modifiedElement`
# We check `re.search("(_|^){0}(_|$)".format(particle), comparisonElement) == None`
# If None, it means `particle` is NOT perfectly found (i.e. as a separate part by '_').
# BUT wait! The `re.search` checks for `particle` with boundaries `_` or `^`/`$`.
# If `particle` is NOT perfectly found, it calculates `distance`.
# Else (if `particle` IS perfectly found), it checks permutations:
# permutations = { "_".join(x) for x in itertools.permutations(partialAnalysis, 2) if x[0] == particle }
# if all(x not in modifiedElement for x in permutations):
#     distance = ...

# Let's think: what does the Else branch mean?
# `particle` IS found exactly in `comparisonElement` as a distinct unit (e.g. `_EGF_` is in `..._EGF_...`).
# BUT wait, what if `EGF` is in `modifiedElement` as a distinct unit, but it was supposed to be modified?
# If `all(x not in modifiedElement for x in permutations):`
# The permutations are ALL pairs of `particle` and another `partialAnalysis` item.
# E.g., `EGF_EGFR`.
# If NONE of these pairs are in `modifiedElement`, then `EGF` is considered for `distance`!
# Why? Because if `EGF_EGFR` IS in `modifiedElement`, then `EGF` is probably part of the larger unmodified block, so it's not the modified part.
# But "fuzzy string matchign" comment says:
# "make sure we only do a search on those variables that are viable candidates. this is once again fuzzy string matchign. there should be a better way of doing this with difflib"

# Wait! The "search" on "those variables that are viable candidates" means that we shouldn't just check `x not in modifiedElement` (exact substring match).
# Because if `EGFR` was slightly modified to `EGFRmod`, then `EGF_EGFR` wouldn't be in `modifiedElement`, but `EGF_EGFRmod` would be.
# If `EGF_EGFRmod` is in `modifiedElement`, we STILL want to recognize that `EGF` is adjacent to `EGFR` (or its modified version), and so `EGF` is NOT the thing that was modified.
# So we want to see if `EGF` is adjacent to any close match of the rest of the permutations!

pass
