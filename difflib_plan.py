import difflib
import itertools

# The issue specifies: "Restrict the search to only viable variables."
# Looking at analyzeSBML.py:289:
# FIXME: make sure we only do a search on those variables that are viable
# candidates. this is once again fuzzy string matchign. there should
# be a better way of doing this with difflib
# permutations = {
#     "_".join(x)
#     for x in itertools.permutations(partialAnalysis, 2)
#     if x[0] == particle
# }
# if all(x not in modifiedElement for x in permutations):

# What if we implement the fuzzy substring match using difflib for "viable candidates"?
# Wait! "viable candidates" might refer to `permutations` itself.
# Are all permutations viable?
# What if we just use difflib.get_close_matches to find the viable permutations from `modifiedElement`?

# What if we change it to:
# viable_candidates = difflib.get_close_matches(particle, [x for x in partialAnalysis if x != particle])
# Then `permutations` is built ONLY using viable candidates!

# "Restrict the search to only viable variables. ... candidates. this is once again fuzzy string matchign. there should be a better way of doing this with difflib"
