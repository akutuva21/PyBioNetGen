import os
from unittest import mock

import pytest

from bionetgen.core.exc import BNGSimError
from bionetgen.simulator import csimulator as csim_module


def test_csimulator_init_logs_missing_cvode_paths():
    from bionetgen.simulator import csimulator as csim_module

    fake_model = mock.MagicMock()
    fake_model.parameters = {}
    fake_model.species = {}
    fake_compiler = mock.MagicMock()
    mock_conf_get = mock.MagicMock(side_effect=lambda key: None)

    def fake_compile(self):
        self.lib_file = "/tmp/fake/libcsim.so"

    with mock.patch.object(csim_module.conf, "get", mock_conf_get), mock.patch.object(
        csim_module, "logger"
    ) as mock_logger, mock.patch.object(
        csim_module.bionetgen, "bngmodel", return_value=fake_model
    ), mock.patch.object(
        csim_module, "_new_ccompiler", return_value=fake_compiler
    ), mock.patch.object(
        csim_module.CSimulator, "compile_shared_lib", fake_compile
    ), mock.patch.object(
        csim_module, "CSimWrapper"
    ) as mock_wrapper:
        csim_module.CSimulator("/fake/model.bngl")

    mock_logger.warning.assert_called_once()
    warning_args, warning_kwargs = mock_logger.warning.call_args
    assert "CVODE include and library paths are not set" in warning_args[0]
    assert "CSimulator.__init__()" in warning_kwargs["loc"]
    fake_compiler.add_include_dir.assert_called_once_with(None)
    fake_compiler.add_library_dir.assert_called_once_with(None)
    assert mock_conf_get.call_args_list == [
        mock.call("cvode_include"),
        mock.call("cvode_include"),
        mock.call("cvode_lib"),
    ]
    mock_wrapper.assert_called_once_with(
        os.path.abspath("/tmp/fake/libcsim.so"), num_params=0, num_spec_init=0
    )


def test_csimulator_init_rmtree_exception(tmp_path):
    import shutil

    import bionetgen
    from bionetgen.simulator import csimulator as csim_module

    model_path = tmp_path / "test.bngl"
    model_path.write_text("begin model\nend model\n")

    fake_model = bionetgen.bngmodel(str(model_path))
    fake_compiler = mock.MagicMock()
    mock_conf_get = mock.MagicMock(side_effect=lambda key: None)

    def fake_compile(self):
        self.lib_file = "/tmp/fake/libcsim.so"

    with mock.patch.object(csim_module.conf, "get", mock_conf_get), mock.patch.object(
        csim_module, "_new_ccompiler", return_value=fake_compiler
    ), mock.patch.object(
        csim_module.CSimulator, "compile_shared_lib", fake_compile
    ), mock.patch.object(
        csim_module, "CSimWrapper"
    ), mock.patch(
        "shutil.rmtree", side_effect=OSError("Permission denied")
    ) as mock_rmtree:
        csim_module.CSimulator(fake_model)

        assert mock_rmtree.called


def test_csimulator_init_invalid_model_type_raises_bng_format_error():
    from bionetgen.core.exc import BNGFormatError
    from bionetgen.simulator import csimulator as csim_module

    mock_conf_get = mock.MagicMock(
        side_effect=lambda key: {
            "cvode_include": "/tmp/include",
            "cvode_lib": "/tmp/lib",
        }[key]
    )

    with mock.patch.object(csim_module.conf, "get", mock_conf_get), mock.patch.object(
        csim_module, "logger"
    ) as mock_logger:
        with pytest.raises(
            BNGFormatError,
            match="CSimulator model input must be a BNGL path or bngmodel instance",
        ):
            csim_module.CSimulator(123)

    mock_logger.error.assert_called_once()
    error_args, error_kwargs = mock_logger.error.call_args
    assert "got int" in error_args[0]
    assert "CSimulator.__init__()" in error_kwargs["loc"]
    assert mock_conf_get.call_args_list == [
        mock.call("cvode_include"),
        mock.call("cvode_lib"),
    ]


def test_csimulator_simulator_setter_raises_bng_compile_error():
    from bionetgen.core.exc import BNGCompileError
    from bionetgen.simulator import csimulator as csim_module

    sim = csim_module.CSimulator.__new__(csim_module.CSimulator)
    sim.model = mock.MagicMock()
    sim.model.parameters = {"k1": mock.MagicMock(expr="0.1")}
    sim.model.species = {"A": mock.MagicMock(count="1")}

    with mock.patch.object(
        csim_module, "CSimWrapper", side_effect=OSError("boom")
    ), mock.patch.object(csim_module, "logger") as mock_logger:
        with pytest.raises(BNGCompileError):
            sim.simulator = "/fake/lib.so"

    mock_logger.error.assert_called_once()
    error_args, error_kwargs = mock_logger.error.call_args
    assert "Failed to initialize C simulator wrapper: boom" in error_args[0]
    assert "CSimulator.simulator.setter()" in error_kwargs["loc"]


def test_csimulator_simulate_resolves_species_parameter_counts():
    from bionetgen.simulator.csimulator import CSimulator

    sim = CSimulator.__new__(CSimulator)
    sim.model = mock.MagicMock()
    sim.model.species = {
        "A": mock.MagicMock(count="5"),
        "B": mock.MagicMock(count="k_init"),
    }
    sim.model.parameters = {
        "k_init": mock.MagicMock(value="7.5", expr="7.5"),
        "k_rate": mock.MagicMock(value="0.1", expr="0.1"),
        "_hidden": mock.MagicMock(value="9.9", expr="9.9"),
        "expr_only": mock.MagicMock(value="unused", expr="k_rate * 2"),
    }
    sim._simulator = mock.MagicMock()
    sim._simulator.simulate.return_value = ("t", "obs", "spcs")

    result = sim.simulate(t_start=1, t_end=4, n_steps=3)

    sim._simulator.set_species_init.assert_called_once_with([5.0, 7.5])
    sim._simulator.set_parameters.assert_called_once_with([7.5, 0.1])
    sim._simulator.simulate.assert_called_once_with(1, 4, 3)
    assert result == ("t", "obs", "spcs")


def test_csimulator_simulate_invalid_species_reference_raises_bng_sim_error():
    from bionetgen.core.exc import BNGSimError
    from bionetgen.simulator import csimulator as csim_module

    sim = csim_module.CSimulator.__new__(csim_module.CSimulator)
    sim.model = mock.MagicMock()
    sim.model.species = {"A": mock.MagicMock(count="missing_param")}
    sim.model.parameters = {}
    sim._simulator = mock.MagicMock()

    with mock.patch.object(csim_module, "logger") as mock_logger:
        with pytest.raises(
            BNGSimError, match="Could not resolve initial species value for 'A'"
        ):
            sim.simulate()

    mock_logger.error.assert_called_once()
    error_args, error_kwargs = mock_logger.error.call_args
    assert "missing_param" in error_args[0]
    assert "CSimulator.simulate()" in error_kwargs["loc"]
    sim._simulator.set_species_init.assert_not_called()


def test_csimulator_get_numeric_parameter_values_attribute_error():
    from bionetgen.simulator import csimulator as csim_module

    sim = csim_module.CSimulator.__new__(csim_module.CSimulator)
    sim.model = mock.MagicMock()

    val_mock = mock.MagicMock()
    del val_mock.expr

    sim.model.parameters = {"param1": val_mock}

    valid_params = sim._get_numeric_parameter_values()
    assert valid_params == []


def test_csimulator_get_numeric_parameter_values_type_error():
    from bionetgen.simulator import csimulator as csim_module

    sim = csim_module.CSimulator.__new__(csim_module.CSimulator)
    sim.model = mock.MagicMock()

    val_mock = mock.MagicMock()
    val_mock.expr = None

    sim.model.parameters = {"param1": val_mock}

    valid_params = sim._get_numeric_parameter_values()
    assert valid_params == []


def test_csimulator_get_numeric_parameter_values_value_error():
    from bionetgen.simulator import csimulator as csim_module

    sim = csim_module.CSimulator.__new__(csim_module.CSimulator)
    sim.model = mock.MagicMock()

    val_mock = mock.MagicMock()
    val_mock.expr = "not_a_float"

    sim.model.parameters = {"param1": val_mock}

    valid_params = sim._get_numeric_parameter_values()
    assert valid_params == []


def test_csimulator_resolve_species_count_type_error():
    sim = csim_module.CSimulator.__new__(csim_module.CSimulator)
    sim.model = mock.MagicMock()

    # raise TypeError on first float(count_value) -> count_value=None
    sim.model.species = {"A": mock.MagicMock(count=None)}

    # second float(self.model.parameters[count_value].value) should succeed
    sim.model.parameters = {None: mock.MagicMock(value="5.5")}

    val = sim._resolve_species_count("A")
    assert val == 5.5


def test_csimulator_resolve_species_count_value_error():
    sim = csim_module.CSimulator.__new__(csim_module.CSimulator)
    sim.model = mock.MagicMock()

    # raise ValueError on first float(count_value) -> count_value="k1"
    sim.model.species = {"A": mock.MagicMock(count="k1")}

    # second float(self.model.parameters[count_value].value) should succeed
    sim.model.parameters = {"k1": mock.MagicMock(value="10.5")}

    val = sim._resolve_species_count("A")
    assert val == 10.5


def test_csimulator_resolve_species_count_inner_attribute_error():
    sim = csim_module.CSimulator.__new__(csim_module.CSimulator)
    sim.model = mock.MagicMock()

    sim.model.species = {"A": mock.MagicMock(count="k1")}

    # inner try block: float(self.model.parameters[count_value].value)
    # let's trigger AttributeError
    param_mock = mock.MagicMock()
    del param_mock.value
    sim.model.parameters = {"k1": param_mock}

    with pytest.raises(
        BNGSimError, match="Could not resolve initial species value for 'A'"
    ):
        sim._resolve_species_count("A")


def test_csimulator_resolve_species_count_inner_key_error():
    sim = csim_module.CSimulator.__new__(csim_module.CSimulator)
    sim.model = mock.MagicMock()

    sim.model.species = {"A": mock.MagicMock(count="k1")}

    # let's trigger KeyError on self.model.parameters[count_value]
    # MagicMock doesn't raise KeyError automatically for non-existent dict keys, so we must set a side_effect
    sim.model.parameters = mock.MagicMock()
    sim.model.parameters.__getitem__.side_effect = KeyError("k1")

    with pytest.raises(
        BNGSimError, match="Could not resolve initial species value for 'A'"
    ):
        sim._resolve_species_count("A")


def test_csimulator_resolve_species_count_inner_type_error():
    sim = csim_module.CSimulator.__new__(csim_module.CSimulator)
    sim.model = mock.MagicMock()

    sim.model.species = {"A": mock.MagicMock(count="k1")}

    # inner try block: float(self.model.parameters[count_value].value)
    # let's trigger TypeError
    param_mock = mock.MagicMock(value=None)
    sim.model.parameters = {"k1": param_mock}

    with pytest.raises(
        BNGSimError, match="Could not resolve initial species value for 'A'"
    ):
        sim._resolve_species_count("A")


def test_csimulator_resolve_species_count_inner_value_error():
    sim = csim_module.CSimulator.__new__(csim_module.CSimulator)
    sim.model = mock.MagicMock()

    sim.model.species = {"A": mock.MagicMock(count="k1")}

    # inner try block: float(self.model.parameters[count_value].value)
    # let's trigger ValueError
    param_mock = mock.MagicMock(value="not_a_float")
    sim.model.parameters = {"k1": param_mock}

    with pytest.raises(
        BNGSimError, match="Could not resolve initial species value for 'A'"
    ):
        sim._resolve_species_count("A")
