import re

with open('bionetgen/modelapi/runner.py', 'r') as f:
    content = f.read()

target = """from bionetgen.core.defaults import BNGDefaults

# This allows access to the CLIs config setup
conf = BNGDefaults()"""

replacement = """app = BioNetGen()
app.setup()
conf = app.config["bionetgen"]"""

content = content.replace(target, replacement)

with open('bionetgen/modelapi/runner.py', 'w') as f:
    f.write(content)
