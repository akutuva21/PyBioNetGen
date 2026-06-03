import pytest
import os
import unittest.mock
import numpy as np
import ctypes
from bionetgen.simulator.csimulator import CSimWrapper, CSimulator
from bionetgen.core.exc import BNGSimulatorError, BNGCompileError


def test_set_parameters_error():
    with unittest.mock.patch("bionetgen.simulator.csimulator.ctypes.CDLL"):
        wrapper = CSimWrapper("dummy_lib_path", num_params=3, num_spec_init=2)
        with pytest.raises(BNGSimulatorError) as excinfo:
            wrapper.set_parameters([1.0, 2.0])
        assert "Expected 3 parameters, but got 2" in str(excinfo.value)


def test_set_species_init_error():
    with unittest.mock.patch("bionetgen.simulator.csimulator.ctypes.CDLL"):
        wrapper = CSimWrapper("dummy_lib_path", num_params=3, num_spec_init=2)
        with pytest.raises(BNGSimulatorError) as excinfo:
            wrapper.set_species_init([1.0])
        assert "Expected 2 initial species, but got 1" in str(excinfo.value)


def test_set_parameters_success():
    with unittest.mock.patch("bionetgen.simulator.csimulator.ctypes.CDLL"):
        wrapper = CSimWrapper("dummy_lib_path", num_params=3, num_spec_init=2)
        wrapper.set_parameters([1.0, 2.0, 3.0])
        np.testing.assert_array_equal(
            wrapper.parameters, np.array([1.0, 2.0, 3.0], dtype=np.float64)
        )


def test_set_species_init_success():
    with unittest.mock.patch("bionetgen.simulator.csimulator.ctypes.CDLL"):
        wrapper = CSimWrapper("dummy_lib_path", num_params=3, num_spec_init=2)
        wrapper.set_species_init([1.0, 2.0])
        np.testing.assert_array_equal(
            wrapper.species_init, np.array([1.0, 2.0], dtype=np.float64)
        )


def test_csimulator_simulator_property():
    csim = CSimulator.__new__(CSimulator)

    class MockVal:
        def __init__(self, expr):
            self.expr = expr

    class MockModel:
        def __init__(self):
            self.parameters = {
                "_ignore": MockVal("1.0"),
                "param1": MockVal("2.0"),
                "param2": MockVal("not_a_float"),
                "param3": MockVal("3.0"),
            }
            self.species = {"spec1": 1, "spec2": 2}

    csim.model = MockModel()

    with unittest.mock.patch(
        "os.path.abspath", side_effect=lambda x: x
    ), unittest.mock.patch(
        "bionetgen.simulator.csimulator.CSimWrapper"
    ) as mock_wrapper:
        csim.simulator = "dummy_lib_file"
        mock_wrapper.assert_called_once()
        args, kwargs = mock_wrapper.call_args
        assert kwargs["num_params"] == 2  # param1 and param3
        assert kwargs["num_spec_init"] == 2  # 2 species
        assert args[0] == "dummy_lib_file"

        assert csim.simulator == mock_wrapper.return_value

    with unittest.mock.patch(
        "bionetgen.simulator.csimulator.CSimWrapper",
            side_effect=OSError("Test Error"),
    ):
        with pytest.raises(BNGCompileError):
            csim.simulator = "dummy_lib_file"


def test_csimulator_simulate():
    csim = CSimulator.__new__(CSimulator)

    class MockVal:
        def __init__(self, expr):
            self.expr = expr

    class MockParam:
        def __init__(self, value, expr=None):
            self.value = value
            self.expr = expr if expr is not None else value

    class MockSpecies:
        def __init__(self, count):
            self.count = count

    class MockModel:
        def __init__(self):
            self.parameters = {
                "_ignore": MockParam("1.0"),
                "param1": MockParam("2.0"),
                "param2": MockParam("not_a_float", "not_a_float"),
                "param3": MockParam("3.0"),
                "spec2_init": MockParam("5.0"),
            }
            # Spec 1 is a direct float, Spec 2 points to a parameter
            self.species = {
                "spec1": MockSpecies("1.0"),
                "spec2": MockSpecies("spec2_init"),
            }

    csim.model = MockModel()

    mock_wrapper = unittest.mock.MagicMock()
    mock_wrapper.simulate.return_value = ("timepoints", "obs_all", "spcs_all")
    csim._simulator = mock_wrapper

    res = csim.simulate(t_start=1, t_end=5, n_steps=4)

    # Check that parameters are set correctly
    mock_wrapper.set_parameters.assert_called_once_with([2.0, 3.0, 5.0])

    # Check that initial species are set correctly
    mock_wrapper.set_species_init.assert_called_once_with([1.0, 5.0])

    # Check that simulate was called correctly
    mock_wrapper.simulate.assert_called_once_with(1, 5, 4)

    assert res == ("timepoints", "obs_all", "spcs_all")


def test_simulator_setter_success():
    # Bypass init
    sim = CSimulator.__new__(CSimulator)
    sim.model = unittest.mock.Mock()

    # Setup mock parameters and species
    param_mock = unittest.mock.Mock()
    param_mock.expr = "1.5"

    param_invalid = unittest.mock.Mock()
    param_invalid.expr = "not_a_float"

    sim.model.parameters = {
        "param1": param_mock,
        "_ignored": unittest.mock.Mock(),
        "param2": param_invalid,
    }
    sim.model.species = {"spec1": unittest.mock.Mock(), "spec2": unittest.mock.Mock()}

    with unittest.mock.patch(
        "bionetgen.simulator.csimulator.CSimWrapper"
    ) as mock_wrapper:
        sim.simulator = "dummy_lib"

        # Check that CSimWrapper is instantiated correctly
        mock_wrapper.assert_called_once()
        args, kwargs = mock_wrapper.call_args
        assert "dummy_lib" in args[0]
        assert kwargs["num_params"] == 1  # only param1 is valid and not ignored
        assert kwargs["num_spec_init"] == 2  # 2 species

        # Check property getter
        assert sim.simulator == mock_wrapper.return_value


def test_simulator_setter_compile_error():
    sim = CSimulator.__new__(CSimulator)
    sim.model = unittest.mock.Mock()
    sim.model.parameters = {}
    sim.model.species = {}

    with unittest.mock.patch(
        "bionetgen.simulator.csimulator.CSimWrapper",
        side_effect=OSError("Wrapper failed"),
    ):
        with pytest.raises(BNGCompileError):
            sim.simulator = "dummy_lib"


def test_csimulator_init_str():
    import bionetgen

    dummy_bngl = "tests/models/test_Hill.bngl"

    with unittest.mock.patch(
        "bionetgen.simulator.csimulator._new_ccompiler", create=True
    ) as mock_new_ccompiler:
        with unittest.mock.patch("bionetgen.simulator.csimulator.conf") as mock_conf:
            mock_conf.get.return_value = "dummy"

            with unittest.mock.patch(
                "bionetgen.simulator.csimulator.bionetgen.run"
            ) as mock_run:
                with unittest.mock.patch("bionetgen.simulator.csimulator.CSimWrapper"):
                    mock_compiler_instance = mock_new_ccompiler.return_value

                    csim = CSimulator(dummy_bngl, generate_network=True)

                    mock_compiler_instance.compile.assert_called_once()
                    mock_compiler_instance.link_shared_lib.assert_called_once()
                    mock_run.assert_called_once()

                    assert csim.model.model_name == "test_Hill"


def test_csimulator_init_bngmodel():
    import bionetgen

    dummy_bngl = "tests/models/test_Hill.bngl"
    mock_model = bionetgen.bngmodel(dummy_bngl, generate_network=True)

    with unittest.mock.patch(
        "bionetgen.simulator.csimulator._new_ccompiler", create=True
    ) as mock_new_ccompiler:
        with unittest.mock.patch("bionetgen.simulator.csimulator.conf") as mock_conf:
            mock_conf.get.return_value = "dummy"

            with unittest.mock.patch(
                "bionetgen.simulator.csimulator.bionetgen.run"
            ) as mock_run:
                with unittest.mock.patch("bionetgen.simulator.csimulator.CSimWrapper"):
                    mock_compiler_instance = mock_new_ccompiler.return_value

                    csim = CSimulator(mock_model, generate_network=True)

                    mock_compiler_instance.compile.assert_called_once()
                    mock_compiler_instance.link_shared_lib.assert_called_once()
                    mock_run.assert_called_once()

                    assert csim.model.model_name == "test_Hill_cpy"
