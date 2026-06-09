import difflib

# Let's consider the task carefully.
# "Restrict the search to only viable variables."
# "make sure we only do a search on those variables that are viable candidates. this is once again fuzzy string matchign. there should be a better way of doing this with difflib"

# The original code:
# permutations = {
#     "_".join(x)
#     for x in itertools.permutations(partialAnalysis, 2)
#     if x[0] == particle
# }
# if all(x not in modifiedElement for x in permutations):

# How can difflib improve this?
# Currently, it iterates over all other items in partialAnalysis, joins them with `_` and checks if it's a substring.
# What if partialAnalysis has `['A', 'B', 'C']` and `modifiedElement` is `A_X_C_B`?
# `A` is next to `X`. Is `X` in partialAnalysis? No.
# `A` joined with `B` is `A_B`, which is not in `A_X_C_B`.
# `A_C` is not in `A_X_C_B`.
# So `A` is searched.
# But wait! If `modifiedElement` is `A_B_C` and we want to find the modified part. (Actually `A_B_C` means no modification, but suppose it's `A_B_C_mod`).
# Then `A_B` is in `A_B_C_mod`, so `A` is skipped.

# What if we just use difflib to find the closest match of `particle` in `modifiedElement`?
# No, `particle` is exactly in `modifiedElement` (the else branch of `re.search("(_|^){0}(_|$)".format(particle), comparisonElement) == None` is taken when `particle` IS in `comparisonElement`).
# Wait!
# if re.search("(_|^){0}(_|$)".format(particle), comparisonElement) == None:
# This means `particle` is NOT perfectly found in `comparisonElement`.
# So the ELSE branch means `particle` IS perfectly found in `comparisonElement`.
# If `particle` IS perfectly found in `comparisonElement`, then how could it be the one that got modified?
# It could be that it got a new neighbor! E.g. `A` -> `A_mod`.
# So `A` is perfectly found, but it has a new neighbor `mod`.
# If `A` is perfectly found, we check if ANY of its old neighbors from `partialAnalysis` are still next to it (`x in modifiedElement`).
# If NONE of its old neighbors are next to it, then we search for the modification distance!
# "make sure we only do a search on those variables that are viable candidates. this is once again fuzzy string matchign. there should be a better way of doing this with difflib"

# The issue is `all(x not in modifiedElement for x in permutations)`.
# What if the old neighbor `B` got modified to `B_mod`?
# Then `A_B_mod` is the `modifiedElement`.
# `A_B` IS a substring of `A_B_mod`! So `A_B` in `modifiedElement` is True.
# So `A` is skipped.
# But what if the neighbor `B` was modified to `mod_B`? Then `modifiedElement` is `A_mod_B`.
# `A_B` is NOT in `A_mod_B`! So `A` is searched!
# But `A` was NOT modified! `B` was modified!
# So `A` is NOT a viable candidate, but we search it anyway!
# If we used difflib, we could see that `A_B` is a "fuzzy match" for `A_mod_B`, and thus `A` is NOT a viable candidate!

pass
