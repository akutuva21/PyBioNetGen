import difflib

permutations = ["A_B", "B_A"]
modifiedElement = "A_mod_B"

# We want to check if ANY permutation is a fuzzy match in modifiedElement.
# How about difflib.get_close_matches?
# Can we just split modifiedElement? No, a fuzzy match could span multiple parts.
# What about difflib.SequenceMatcher(None, perm, modifiedElement).ratio()?
for p in permutations:
    matcher = difflib.SequenceMatcher(None, p, modifiedElement)
    match = "".join(modifiedElement[j : j + n] for i, j, n in matcher.get_matching_blocks() if n)
    print(p, match, matcher.ratio())

# Wait, difflib.get_close_matches uses SequenceMatcher.ratio().
# Is A_B close to A_mod_B?
# len(A_B) = 3
# len(A_mod_B) = 7
# Match is 'A_B' length 3. Ratio = 2 * 3 / 10 = 0.6.
# If cutoff is 0.6, it matches!
print(difflib.get_close_matches("A_B", ["A_mod_B"], cutoff=0.6))
