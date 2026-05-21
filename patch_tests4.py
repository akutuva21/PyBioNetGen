with open("tests/test_pathwaycommons.py", "r") as f:
    content = f.read()

# Change the arguments to be unique per test to avoid memoize cache collision
content = content.replace('name2uniprot("EGFR", ["tax/9606"])', 'name2uniprot("EGFR_A", ["tax/9606"])', 1)
content = content.replace('name2uniprot("EGFR", ["tax/9606"])', 'name2uniprot("EGFR_B", ["tax/9606"])', 1)
content = content.replace('name2uniprot("EGFR", ["tax/9606"])', 'name2uniprot("EGFR_C", ["tax/9606"])', 1)
content = content.replace('name2uniprot("EGFR", ["tax/9606"])', 'name2uniprot("EGFR_D", ["tax/9606"])', 1)

with open("tests/test_pathwaycommons.py", "w") as f:
    f.write(content)
