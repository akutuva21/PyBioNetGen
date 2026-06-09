import difflib

# How about `get_close_matches(particle, modifiedElement)`?
# "there should be a better way of doing this with difflib"

# The old code:
# permutations = {"_".join(x) for x in itertools.permutations(partialAnalysis, 2) if x[0] == particle}
# if all(x not in modifiedElement for x in permutations): ...

# What if we just split the modified element into parts separated by `_`?
# E.g. modifiedElement = "A_modified_B_C" -> ["A", "modified", "B", "C"]
# If any close match of `particle` is in those parts, AND it's adjacent to another part that closely matches another element of `partialAnalysis`?
# This is basically re-implementing `analyzeSpeciesModification2` logic!

# Wait, what if we use `difflib.get_close_matches` on `permutations` against `modifiedElement.split("_")`? No.
# What if we use `sequenceMatcher` to compare `permutations` against `modifiedElement`?
