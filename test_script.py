import sys, os
sys.path.insert(0, os.getcwd())
import bionetgen as bng
fpath = os.path.abspath("tests/models/test_synthesis_simple.bngl")
m = bng.bngmodel(fpath)
librr_simulator = m.setup_simulator()
res = librr_simulator.simulate(0, 1, 10)
print(res)
