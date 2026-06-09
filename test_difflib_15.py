import difflib

# Let's say modifiedElement is EGF_EGFR_2_P
modifiedElement = "EGF_EGFR_2_P"
permutations = ["EGF_EGFR"]

# We want to use difflib to check if ANY permutation is in modifiedElement (fuzzy).
# We can do this with difflib.SequenceMatcher

for perm in permutations:
    matcher = difflib.SequenceMatcher(None, perm, modifiedElement)

    # We want to see if there's a good match block
    match = "".join(modifiedElement[j : j + n] for i, j, n in matcher.get_matching_blocks() if n)
    print(f"Match for {perm}: '{match}' (len {len(match)} vs len {len(perm)}) ratio {len(match)/len(perm)}")

    # Or just `matcher.ratio()` ?
    # But `EGF_EGFR_2_P` is longer, so the ratio will be low.
    # What if we use difflib.get_close_matches?
