import re

with open('bionetgen/atomizer/bngModel.py', 'r') as f:
    text = f.read()

# Replace the specific lines
old_code = """                        # this will be a function
                        fobj = self.make_function()
                        # TODO: sometimes molec.name is not
                        # normalized, check if .Id works consistently
                        fobj.Id = molec.Id + "()"
                        fobj.definition = arule.rates[0]"""

new_code = """                        # this will be a function
                        fobj = self.make_function()
                        fobj.Id = molec.Id + "()"
                        fobj.definition = arule.rates[0]"""

new_text = text.replace(old_code, new_code)

with open('bionetgen/atomizer/bngModel.py', 'w') as f:
    f.write(new_text)
