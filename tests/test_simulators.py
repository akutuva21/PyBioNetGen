import pytest
import unittest.mock
import os
from bionetgen.simulator.simulators import sim_getter


def test_sim_getter_model_file():
    with unittest.mock.patch(
        "bionetgen.simulator.simulators.libRRSimulator"
    ) as mock_librr:
        sim_getter(model_file="test.bngl", sim_type="libRR")
        mock_librr.assert_called_once_with(model_file="test.bngl")

    with unittest.mock.patch("bionetgen.simulator.simulators.CSimulator") as mock_csim:
        sim_getter(model_file="test.bngl", sim_type="cpy")
        mock_csim.assert_called_once_with(model_file="test.bngl", generate_network=True)

    with unittest.mock.patch("builtins.print") as mock_print:
        res = sim_getter(model_file="test.bngl", sim_type="unknown")
        assert res is None
        mock_print.assert_called_once_with("simulator type unknown not supported")


def test_sim_getter_model_str():
    with unittest.mock.patch(
        "bionetgen.simulator.simulators.libRRSimulator"
    ) as mock_librr:
        sim_getter(model_str="begin model\nend model\n", sim_type="libRR")
        assert mock_librr.call_count == 1
        args, kwargs = mock_librr.call_args
        assert "model_file" in kwargs
        assert (
            os.path.exists(kwargs["model_file"]) is False
        )  # since NamedTemporaryFile is closed, it might not exist, but let's just check it's passed

    with unittest.mock.patch("bionetgen.simulator.simulators.CSimulator") as mock_csim:
        sim_getter(model_str="begin model\nend model\n", sim_type="cpy")
        assert mock_csim.call_count == 1
        args, kwargs = mock_csim.call_args
        assert "model_file" in kwargs
        assert kwargs["generate_network"] is True

    with unittest.mock.patch("builtins.print") as mock_print:
        res = sim_getter(model_str="begin model\nend model\n", sim_type="unknown")
        assert res is None
        assert mock_print.call_count == 2
        mock_print.assert_has_calls(
            [
                unittest.mock.call("simulator type unknown not supported"),
                unittest.mock.call("simulator type unknown not supported"),
            ]
        )


def test_sim_getter_no_args():
    res = sim_getter()
    assert res is None
