import difflib
import itertools

def old_check(particle, partialAnalysis, modifiedElement):
    permutations = {
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    }
    return all(x not in modifiedElement for x in permutations)

def new_check(particle, partialAnalysis, modifiedElement):
    permutations = {
        "_".join(x)
        for x in itertools.permutations(partialAnalysis, 2)
        if x[0] == particle
    }

    # "this is once again fuzzy string matchign. there should be a better way of doing this with difflib"

    for perm in permutations:
        sequenceMatcher = difflib.SequenceMatcher(None, perm, modifiedElement)
        match = "".join(
            modifiedElement[j : j + n]
            for i, j, n in sequenceMatcher.get_matching_blocks()
            if n
        )
        if (len(match)) / float(len(perm)) >= 0.8:
            tmp = [
                i
                for i, y in enumerate(difflib.ndiff(perm, modifiedElement))
                if not y.startswith("+")
            ]
            if len(tmp) > 0 and tmp[-1] - tmp[0] <= len(perm) + 5:
                return False
    return True

print("A_B_C -> A_mod_B_C")
print("old 'A':", old_check("A", ["A", "B", "C"], "A_mod_B_C"))
print("new 'A':", new_check("A", ["A", "B", "C"], "A_mod_B_C"))

print("\nA_B_C -> A_B_mod_C")
print("old 'A':", old_check("A", ["A", "B", "C"], "A_B_mod_C"))
print("new 'A':", new_check("A", ["A", "B", "C"], "A_B_mod_C"))

print("\nA_B_C -> A_B_C_mod")
print("old 'A':", old_check("A", ["A", "B", "C"], "A_B_C_mod"))
print("new 'A':", new_check("A", ["A", "B", "C"], "A_B_C_mod"))
