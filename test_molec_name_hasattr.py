class Molecule:
    def __init__(self, id=None):
        self.Id = id

molec = Molecule(id="MoleculeID")

observables = {}

try:
    # If molec doesn't have a 'name' attribute
    if getattr(molec, "name", None) in observables:
        print("In observables")
    else:
        print("Not in observables")

except Exception as e:
    print(f"Exception: {e}")
