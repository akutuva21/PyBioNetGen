import sys
sys.path.append('.')
from bionetgen.atomizer.bngModel import Molecule

m = Molecule()
try:
    m.parse_raw({"returnID": "test", "initialConcentration": 1, "initialAmount": 1, "isConstant": False, "isBoundary": False, "compartment": "c", "name": None, "identifier": "id", "conversionFactor": 1})
    print(m.name)
except Exception as e:
    print(f"Exception: {e}")
