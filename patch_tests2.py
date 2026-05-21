with open("tests/test_pathwaycommons.py", "r") as f:
    content = f.read()

# I will replace b"Entry name\tEntry\nEGFR_HUMAN\tP00533\n" with "Entry name\tEntry\nEGFR_HUMAN\tP00533\n"
content = content.replace('b"Entry name\\tEntry\\nEGFR_HUMAN\\tP00533\\n"', '"Entry name\\tEntry\\nEGFR_HUMAN\\tP00533\\n"')
content = content.replace('b""', '""')

with open("tests/test_pathwaycommons.py", "w") as f:
    f.write(content)
