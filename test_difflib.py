import difflib
import itertools
import re

partialAnalysis = ['EGF', 'EGFR']
modifiedElement = 'EGF_EGFR_2_P'
particle = 'EGF'

permutations = {
    "_".join(x)
    for x in itertools.permutations(partialAnalysis, 2)
    if x[0] == particle
}
print(f"Old permutations: {permutations}")
print(f"Old condition: {all(x not in modifiedElement for x in permutations)}")

# The old way did exact substring matching: `x not in modifiedElement`
# The comment says: "there should be a better way of doing this with difflib"

# Let's try difflib
matches = difflib.get_close_matches(particle, partialAnalysis)
print(f"Matches for {particle} in {partialAnalysis}: {matches}")

# Wait, the old code checks if any permutation like `particle_something` is in `modifiedElement`.
# What does this mean? It means checking if `particle` is adjacent to another element in `partialAnalysis` inside `modifiedElement`.
# If `all(x not in modifiedElement for x in permutations)` is True, it calculates `distance`.
