import pytest
import unittest.mock
import sys
from bionetgen.simulator.librrsimulator import libRRSimulator

def test_librrsimulator_sbml():
    sim = libRRSimulator()
    mock_simulator = unittest.mock.Mock()
    mock_simulator.getCurrentSBML.return_value = "<sbml>mock</sbml>"
    sim._simulator = mock_simulator

    # Initially _sbml doesn't exist, so it should fetch from simulator
    assert sim.sbml == "<sbml>mock</sbml>"
    mock_simulator.getCurrentSBML.assert_called_once()

    # Calling it again should return the cached _sbml and not call getCurrentSBML again
    assert sim.sbml == "<sbml>mock</sbml>"
    assert mock_simulator.getCurrentSBML.call_count == 1

    # Setting sbml should override the cached value
    sim.sbml = "<sbml>new</sbml>"
    assert sim.sbml == "<sbml>new</sbml>"
    assert mock_simulator.getCurrentSBML.call_count == 1

def test_librrsimulator_simulator_property():
    sim = libRRSimulator()

    # Test simulator setter with a mock roadrunner model
    mock_rr_module = unittest.mock.Mock()
    mock_rr_module.RoadRunner.return_value = "mock_rr_instance"

    with unittest.mock.patch.dict('sys.modules', {'roadrunner': mock_rr_module}):
        sim.simulator = "dummy_model"

        # Verify RoadRunner was instantiated with the model
        mock_rr_module.RoadRunner.assert_called_once_with("dummy_model")

        # Verify simulator property returns the instance
        assert sim.simulator == "mock_rr_instance"

def test_librrsimulator_simulator_import_error():
    sim = libRRSimulator()

    # Test simulator setter when roadrunner import fails
    with unittest.mock.patch.dict('sys.modules', {'roadrunner': None}):
        # Mock print to verify the error message is printed
        with unittest.mock.patch('builtins.print') as mock_print:
            sim.simulator = "dummy_model"
            mock_print.assert_called_once_with("libroadrunner is not installed!")

            # _simulator should remain uninitialized or as previously set
            assert not hasattr(sim, '_simulator')

def test_librrsimulator_simulate():
    sim = libRRSimulator()
    mock_simulator = unittest.mock.Mock()
    mock_simulator.simulate.return_value = "simulation_results"
    sim._simulator = mock_simulator

    # Test that simulate passes args and kwargs to the underlying simulator
    res = sim.simulate("arg1", kwarg1="val1")

    assert res == "simulation_results"
    mock_simulator.simulate.assert_called_once_with("arg1", kwarg1="val1")
