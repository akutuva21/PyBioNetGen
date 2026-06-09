import itertools
import difflib

# Currently:
# permutations = {
#     "_".join(x)
#     for x in itertools.permutations(partialAnalysis, 2)
#     if x[0] == particle
# }
# if all(x not in modifiedElement for x in permutations):

# Could it just be replaced by checking if `particle` has any close match in parts of modifiedElement?
# What if the user meant:
# Instead of iterating over permutations, just use get_close_matches on the split modifiedElement.
# "make sure we only do a search on those variables that are viable candidates"
#
