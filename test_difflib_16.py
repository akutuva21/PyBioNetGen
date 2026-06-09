import difflib

permutations = ["A_B", "A_C"]
modifiedElement = "A_modified_B_C"

for perm in permutations:
    matcher = difflib.SequenceMatcher(None, perm, modifiedElement)
    match = "".join(modifiedElement[j : j + n] for i, j, n in matcher.get_matching_blocks() if n)
    print(f"Match for {perm}: '{match}' (len {len(match)} vs len {len(perm)}) ratio {len(match)/len(perm)}")
