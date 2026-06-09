import difflib

permutations = ["A_B"]
modifiedElement = "C_A_mod_B_D"

print(difflib.get_close_matches("A_B", [modifiedElement], cutoff=0.4))
# len(A_B) = 3
# len(C_A_mod_B_D) = 11
# match = 3
# ratio = 6 / 14 = 0.428.
# If modifiedElement is very long, ratio will be very small, even if "A_B" is fully contained!
# e.g., if modifiedElement is 20 chars long, ratio < 0.3.
# So `get_close_matches` with `modifiedElement` directly is BAD because of length differences.
