import difflib

# Let's say modifiedElement is "EGF_EGFR_2_P"
modifiedElement = "EGF_EGFR_2_P"
permutations = ["EGF_EGFR"]

# We want to use difflib to find if permutations are "in" modifiedElement
# difflib.get_close_matches(word, possibilities)
# Wait, get_close_matches finds the best matches for 'word' from 'possibilities'
# If we have a list of valid permutations, we could check if any are close matches to parts of modifiedElement?
# No, "fuzzy string matchign" might just mean we match `particle` and `partialAnalysis` elements more robustly than just exact string joining.

# Currently:
# permutations = { "_".join(x) for x in itertools.permutations(partialAnalysis, 2) if x[0] == particle }
# if all(x not in modifiedElement for x in permutations):

def check_difflib(particle, partialAnalysis, modifiedElement):
    viable_candidates = [
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    ]

    # Check if any candidate is a substring (old way)
    old_result = all(x not in modifiedElement for x in viable_candidates)

    # New way with difflib?
    # Maybe we want to see if there's any close match of any viable candidate in modifiedElement?
    # difflib doesn't natively do "substring fuzzy match".
    # SequenceMatcher could be used.

    # Let's check sequenceMatcher from utils?

    # Or maybe it just means using difflib.get_close_matches against the parts of modifiedElement?
    parts = [modifiedElement[i:j] for i in range(len(modifiedElement)) for j in range(i+1, len(modifiedElement)+1)]
    # That's O(N^2), but modifiedElement is short.

print("ok")
