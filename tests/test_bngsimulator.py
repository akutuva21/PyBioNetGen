import pytest
from bionetgen.simulator.bngsimulator import BNGSimulator


def test_bngsimulator_simulate():
    simulator = BNGSimulator()
    with pytest.raises(NotImplementedError):
        simulator.simulate()
