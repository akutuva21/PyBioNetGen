import pytest
import os
import sys
from unittest.mock import MagicMock

# Create a mock for roadrunner BEFORE importing any PyBioNetGen modules
mock_roadrunner = MagicMock()
mock_rr_instance = MagicMock()
mock_roadrunner.RoadRunner.return_value = mock_rr_instance
sys.modules["roadrunner"] = mock_roadrunner

# Now we can import the simulator
from bionetgen.simulator.librrsimulator import libRRSimulator


def test_librrsimulator_sbml():
    """Test the sbml getter and setter in libRRSimulator."""
    # Create simulator instance
    sim = libRRSimulator("fake_bngl_path", "fake_sbml_path")

    # Check initial state (should not have _sbml attribute yet)
    assert not hasattr(sim, "_sbml")

    # Mock the getCurrentSBML method on the roadrunner instance
    mock_sbml_content = "<sbml>mock content</sbml>"
    sim.simulator.getCurrentSBML.return_value = mock_sbml_content

    # Test getter - should call getCurrentSBML and set _sbml
    retrieved_sbml = sim.sbml
    assert retrieved_sbml == mock_sbml_content
    sim.simulator.getCurrentSBML.assert_called_once()
    assert hasattr(sim, "_sbml")
    assert sim._sbml == mock_sbml_content

    # Reset mock to ensure it's not called again
    sim.simulator.getCurrentSBML.reset_mock()

    # Test getter again - should return cached _sbml without calling getCurrentSBML
    retrieved_sbml_2 = sim.sbml
    assert retrieved_sbml_2 == mock_sbml_content
    sim.simulator.getCurrentSBML.assert_not_called()

    # Test setter
    new_sbml_content = "<sbml>new content</sbml>"
    sim.sbml = new_sbml_content
    assert sim._sbml == new_sbml_content

    # Test getter after setter
    assert sim.sbml == new_sbml_content
