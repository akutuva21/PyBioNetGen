import difflib
import itertools

partialAnalysis = ['EGF', 'EGFR']
modifiedElement = 'EGF_EGFR_2_P'
particle = 'EGF'

permutations = [
    "_".join(x)
    for x in itertools.permutations(partialAnalysis, 2)
    if x[0] == particle
]

print("permutations:", permutations)
print("get_close_matches modifiedElement vs permutations:", difflib.get_close_matches(modifiedElement, permutations))

# What if we split modifiedElement into chunks of size 2?
chunks = modifiedElement.split('_')
chunk_pairs = ["_".join(chunks[i:i+2]) for i in range(len(chunks)-1)]
print("chunk_pairs:", chunk_pairs)

for perm in permutations:
    print(f"close matches for {perm} in {chunk_pairs}:", difflib.get_close_matches(perm, chunk_pairs))
