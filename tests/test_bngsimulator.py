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


def test_bngsimulator_model_file_init():
    sim = BNGSimulator(model_file="test.bngl")
    assert sim.model_file == "test.bngl"
    assert sim.simulator == "test.bngl"
    with pytest.raises(AttributeError):
        sim.model_str


def test_bngsimulator_model_str_init():
    sim = BNGSimulator(model_str="model_content")
    assert sim.model_str == "model_content"
    assert sim.simulator == "model_content"
    with pytest.raises(AttributeError):
        sim.model_file


def test_bngsimulator_setters():
    sim = BNGSimulator()
    sim.model_file = "test2.bngl"
    assert sim.model_file == "test2.bngl"
    assert sim.simulator == "test2.bngl"

    sim.model_str = "new_content"
    assert sim.model_str == "new_content"
    assert sim.simulator == "new_content"


def test_bngsimulator_simulate_raises():
    sim = BNGSimulator()
    with pytest.raises(NotImplementedError):
        sim.simulate()
