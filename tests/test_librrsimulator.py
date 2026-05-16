import pytest
import unittest.mock
import sys
from bionetgen.simulator.librrsimulator import libRRSimulator


def test_librrsimulator_import_error(capsys):
    with unittest.mock.patch.dict(sys.modules, {"roadrunner": None}):
        sim = libRRSimulator(model_file="dummy_model.xml")
        captured = capsys.readouterr()
        assert "libroadrunner is not installed!" in captured.out


def test_librrsimulator_success():
    # Mock the roadrunner module
    mock_rr = unittest.mock.MagicMock()
    mock_rr_instance = unittest.mock.MagicMock()
    mock_rr.RoadRunner.return_value = mock_rr_instance
    mock_rr_instance.getCurrentSBML.return_value = "<sbml>test</sbml>"
    mock_rr_instance.simulate.return_value = "simulation_result"

    with unittest.mock.patch.dict(sys.modules, {"roadrunner": mock_rr}):
        sim = libRRSimulator(model_file="dummy_model.xml")

        # Check simulator setter
        mock_rr.RoadRunner.assert_called_once_with("dummy_model.xml")
        assert sim.simulator == mock_rr_instance

        # Check simulate method
        result = sim.simulate(1, 2, a=3)
        mock_rr_instance.simulate.assert_called_once_with(1, 2, a=3)
        assert result == "simulation_result"

        # Check sbml property getter
        assert sim.sbml == "<sbml>test</sbml>"
        mock_rr_instance.getCurrentSBML.assert_called_once()

        # Check sbml property setter
        sim.sbml = "<sbml>new</sbml>"
        assert sim.sbml == "<sbml>new</sbml>"


def test_librrsimulator_model_str():
    mock_rr = unittest.mock.MagicMock()
    with unittest.mock.patch.dict(sys.modules, {"roadrunner": mock_rr}):
        sim = libRRSimulator(model_str="<sbml>direct</sbml>")
        mock_rr.RoadRunner.assert_called_once_with("<sbml>direct</sbml>")
