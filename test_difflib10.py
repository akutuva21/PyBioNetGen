import difflib

# Let's say modifiedElement is "EGF_EGFR_2_P".
# We want to check if ANY permutation is closely matching a substring of modifiedElement.
# But wait, difflib.get_close_matches('EGF_EGFR_2_P', ['EGF_EGFR']) returns ['EGF_EGFR'].
# Why? Because 'EGF_EGFR' is somewhat close to 'EGF_EGFR_2_P' in terms of difflib's ratio (8/12 = 0.66 > 0.6 cutoff).

def get_close_matches(match, dataset, cutoff=0.6):
    return difflib.get_close_matches(match, dataset, cutoff=cutoff)

print(get_close_matches('EGF_EGFR_2_P', ['EGF_EGFR']))
