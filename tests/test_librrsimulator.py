import pytest
import unittest.mock
import sys
from bionetgen.simulator.librrsimulator import libRRSimulator

def test_librrsimulator_basic():
    """Test the basic property getters/setters and simulate method."""
    mock_rr_module = unittest.mock.MagicMock()
    mock_instance = unittest.mock.MagicMock()
    mock_rr_module.RoadRunner.return_value = mock_instance
    mock_instance.getCurrentSBML.return_value = "<sbml>mocked</sbml>"
    mock_instance.simulate.return_value = "simulation_result"

    with unittest.mock.patch.dict('sys.modules', {'roadrunner': mock_rr_module}):
        sim = libRRSimulator("mock_model.xml")

        # Test property getter
        assert sim.simulator == mock_instance
        mock_rr_module.RoadRunner.assert_called_with("mock_model.xml")

        # Test simulate method
        res = sim.simulate(0, 10, 100)
        assert res == "simulation_result"
        mock_instance.simulate.assert_called_with(0, 10, 100)

        # Test sbml property
        assert sim.sbml == "<sbml>mocked</sbml>"
        mock_instance.getCurrentSBML.assert_called_once()

        # Test sbml setter
        sim.sbml = "<sbml>new</sbml>"
        assert sim.sbml == "<sbml>new</sbml>"

def test_librrsimulator_import_error():
    """Test the import error handling when roadrunner is not installed."""
    with unittest.mock.patch.dict('sys.modules', {'roadrunner': None}):
        with unittest.mock.patch('builtins.print') as mock_print:
            sim = libRRSimulator("mock_model.xml")
            mock_print.assert_called_with("libroadrunner is not installed!")
