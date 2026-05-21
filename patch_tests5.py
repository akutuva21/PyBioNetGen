with open("tests/test_pathwaycommons.py", "r") as f:
    content = f.read()

# Change it back to EGFR for all of them so the mock works because it looks for "nameStr" inside the mocked string!
# The string "EGFR_HUMAN" contains "EGFR". If I change to "EGFR_A", it won't match "EGFR_HUMAN".
content = content.replace('EGFR_A', 'EGFR')
content = content.replace('EGFR_B', 'EGFR')
content = content.replace('EGFR_C', 'EGFR')
content = content.replace('EGFR_D', 'EGFR')

# To clear the cache from `memoize`, we should do `name2uniprot.cache.clear()`
content = content.replace('name2uniprot.cache = {}', 'name2uniprot.cache.clear()')

with open("tests/test_pathwaycommons.py", "w") as f:
    f.write(content)
