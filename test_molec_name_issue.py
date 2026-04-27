class Molecule:
    def __init__(self, name=None, id=None):
        self.name = name
        self.Id = id

molec = Molecule(id="MoleculeID")

# Simulated attributes
observables = {}
species = {}
parameters = {"MoleculeID": "ParamValue"}

# What happens when molec.name is accessed?
print(getattr(molec, 'name', None))

try:
    if molec.name in observables:
        print("In observables by name")
    elif molec.Id in observables:
        print("In observables by Id")

    if molec.name in species:
        print("In species by name")
    elif molec.Id in species:
        print("In species by Id")
except Exception as e:
    print(f"Exception: {e}")
