import difflib

permutations = ["A_B"]
modifiedElement = "A_modified_B_C"
for x in permutations:
    matcher = difflib.SequenceMatcher(None, x, modifiedElement)
    match = "".join(modifiedElement[j : j + n] for i, j, n in matcher.get_matching_blocks() if n)
    print("Match:", match)
    if len(match) / float(len(x)) >= 0.8:
        # they are close! But are they contiguous in modifiedElement?
        # get indices in modifiedElement
        indices = []
        for i, j, n in matcher.get_matching_blocks():
            if n > 0:
                indices.extend(range(j, j + n))
        print("Indices:", indices)
        if indices[-1] - indices[0] <= len(x) + 5:
            print(x, "is fuzzily in modifiedElement")
        else:
            print(x, "is NOT fuzzily in modifiedElement")
