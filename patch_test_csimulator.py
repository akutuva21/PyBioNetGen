import re

with open("tests/test_csimulator.py", "r") as f:
    content = f.read()

content = content.replace("    with (\n        unittest.mock.patch(\"os.path.abspath\", side_effect=lambda x: x),\n        unittest.mock.patch(\n            \"bionetgen.simulator.csimulator.CSimWrapper\"\n        ) as mock_wrapper,\n    ):", "    with unittest.mock.patch(\"os.path.abspath\", side_effect=lambda x: x), \\\n         unittest.mock.patch(\"bionetgen.simulator.csimulator.CSimWrapper\") as mock_wrapper:")

with open("tests/test_csimulator.py", "w") as f:
    f.write(content)
