import pytest
from bionetgen.simulator.bngsimulator import BNGSimulator


def test_bngsimulator_model_file_property():
    sim = BNGSimulator()
    sim.model_file = "test_model.bngl"
    assert sim.model_file == "test_model.bngl"


def test_bngsimulator_model_str_property():
    sim = BNGSimulator()
    sim.model_str = "model content"
    assert sim.model_str == "model content"


def test_bngsimulator_init():
    sim1 = BNGSimulator(model_file="test_model.bngl")
    assert sim1.model_file == "test_model.bngl"
    assert sim1.simulator == "test_model.bngl"

    sim2 = BNGSimulator(model_str="model content")
    assert sim2.model_str == "model content"
    assert sim2.simulator == "model content"


def test_bngsimulator_simulate_raises():
    sim = BNGSimulator()
    with pytest.raises(NotImplementedError):
        sim.simulate()
