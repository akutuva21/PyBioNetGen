import re
import difflib

# Let's say partialAnalysis = ['A', 'B', 'C']
# particle = 'A'
# What does difflib do?
# Maybe `difflib.get_close_matches`?

# Look at the FIXME again:
# # FIXME: make sure we only do a search on those variables that are viable
# # candidates. this is once again fuzzy string matchign. there should
# # be a better way of doing this with difflib
# permutations = {
#     "_".join(x)
#     for x in itertools.permutations(partialAnalysis, 2)
#     if x[0] == particle
# }
# if all(x not in modifiedElement for x in permutations):
#     distance = self.distanceToModification(
#         particle, comparisonElement, translationKeys[0]
#     )

# The permutations check: it builds strings like `particle_something` and checks if it's NOT in `modifiedElement`.
# Wait, if `particle` is in `modifiedElement`, but NOT adjacent to ANY other element from `partialAnalysis` (i.e. `x not in modifiedElement for x in permutations`), THEN we calculate `distanceToModification`.
# Wait! This means if `particle` IS adjacent to another element in `modifiedElement`, it skips calculating `distanceToModification`!
# Why would it skip? Because if it's adjacent to another element, it implies `particle` itself is probably unmodified. The modification happened somewhere else.
# BUT wait, what if `modifiedElement` is `particle_modification`? Then `particle` is adjacent to `modification`, which is NOT in `partialAnalysis`. So it is NOT adjacent to another element from `partialAnalysis`. Thus `x not in modifiedElement` is True. Then we calculate distance!
# YES! That's the logic. It only searches for a modification on `particle` if `particle` is NOT found perfectly adjacent to its original neighbors.

# But exact substring match `x not in modifiedElement` is fragile. What if the original neighbor was also slightly modified?
# E.g. `partialAnalysis` = ['A', 'B']. `modifiedElement` = 'A_Bmod'.
# `permutations` = ['A_B'].
# `A_B` in `A_Bmod` is True! So it skips `A`!
# Wait, `A_B` in `A_Bmod` is True because `A_B` is a substring of `A_Bmod`.
# So it skips `A`. This might be correct or incorrect.

# "viable candidates"
# The comment says: "there should be a better way of doing this with difflib"
# What if we use `difflib.get_close_matches(particle, modifiedElement)`? No, `particle` is just a chunk.
# What if we get close matches for permutations against parts of `modifiedElement`?
# Or maybe the problem is that we are looking for permutations. Instead of permutations, we could just use difflib to find if `particle` is a viable candidate.
#
