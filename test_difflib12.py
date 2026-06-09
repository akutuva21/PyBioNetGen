import difflib
import itertools

def check_new_2(partialAnalysis, modifiedElement, particle):
    permutations = [
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    ]

    # We want to know if 'perm' is found as a substring (fuzzy) inside 'modifiedElement'.
    # difflib doesn't have a direct "fuzzy substring" except SequenceMatcher.

    # Wait, get_close_matches checks if 'word' is in 'possibilities'.
    # What if 'possibilities' is parts of 'modifiedElement'?
    # Split modifiedElement by '_'
    parts = modifiedElement.split('_')
    # Generate all sub-sequences of parts
    subseqs = ["_".join(parts[i:j]) for i in range(len(parts)) for j in range(i+1, len(parts)+1)]

    # For each perm, check if it is close to any subseqs
    for perm in permutations:
        matches = difflib.get_close_matches(perm, subseqs, cutoff=0.8)
        if matches:
            return False # equivalent to: found in modifiedElement
    return True

print(check_new_2(['A', 'B', 'C'], 'A_modified_B_C', 'A'))
