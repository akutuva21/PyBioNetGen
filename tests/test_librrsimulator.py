import pytest
import sys
import unittest.mock
from unittest.mock import MagicMock
from bionetgen.simulator.librrsimulator import libRRSimulator


def test_librrsimulator_sbml():
    mock_rr = MagicMock()
    mock_rr_instance = mock_rr.RoadRunner.return_value
    mock_rr_instance.getCurrentSBML.return_value = "mock_sbml_string"

    with unittest.mock.patch.dict(sys.modules, {"roadrunner": mock_rr}):
        simulator = libRRSimulator(model_str="initial_model")

        # Initially _sbml doesn't exist, so it should call getCurrentSBML()
        sbml_val = simulator.sbml
        assert sbml_val == "mock_sbml_string"
        mock_rr_instance.getCurrentSBML.assert_called_once()

        # Accessing it again shouldn't call getCurrentSBML again
        sbml_val_2 = simulator.sbml
        assert sbml_val_2 == "mock_sbml_string"
        assert mock_rr_instance.getCurrentSBML.call_count == 1

        # Test setter
        simulator.sbml = "new_sbml_string"
        assert simulator.sbml == "new_sbml_string"
        assert simulator._sbml == "new_sbml_string"
