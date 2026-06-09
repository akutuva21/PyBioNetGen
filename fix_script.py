import re

with open('tests/test_notebook_cmd.py', 'r') as f:
    content = f.read()

# remove app.setup() calls
content = re.sub(r'\s+app\.setup\(\)\n', '\n', content)

with open('tests/test_notebook_cmd.py', 'w') as f:
    f.write(content)
