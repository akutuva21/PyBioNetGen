import sys
sys.path.append('.')
from bionetgen.atomizer.bngModel import Molecule, bngModel

class MockMolecule:
    def __init__(self, id, name):
        self.Id = id
        self.name = name
        self.isConstant = False

class MockRule:
    def __init__(self, id, rates):
        self.Id = id
        self.rates = rates
        self.compartmentList = []

m = bngModel()
m.molecule_ids = {"rule1": "m1"}
m.molecules = {"m1": MockMolecule("molec1", "m1_name")}
m.observables = {"m1_name": type("Obs", (), {"get_obs_name": lambda self: "obs_m1"})()}
m.species = {"m1_name": "spec1"}

arule = MockRule("rule1", ["rate_expr"])
m.arules = {"rule1": arule}

# test what happens if name is missing
try:
    m.molecules["m2"] = MockMolecule("molec2", None)
    m.molecule_ids["rule2"] = "m2"
    m.arules["rule2"] = MockRule("rule2", ["rate_expr2"])
except Exception as e:
    print(f"Exception: {e}")
