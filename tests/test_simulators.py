import pytest
import os
from unittest.mock import patch, MagicMock
from bionetgen.simulator.simulators import sim_getter


@patch("bionetgen.simulator.simulators.libRRSimulator")
def test_sim_getter_model_file_libRR(mock_libRR):
    mock_libRR.return_value = "mock_libRR_instance"
    result = sim_getter(model_file="test.bngl", sim_type="libRR")
    mock_libRR.assert_called_once_with(model_file="test.bngl")
    assert result == "mock_libRR_instance"


@patch("bionetgen.simulator.simulators.CSimulator")
def test_sim_getter_model_file_cpy(mock_cpy):
    mock_cpy.return_value = "mock_cpy_instance"
    result = sim_getter(model_file="test.bngl", sim_type="cpy")
    mock_cpy.assert_called_once_with(model_file="test.bngl", generate_network=True)
    assert result == "mock_cpy_instance"


@patch("builtins.print")
def test_sim_getter_model_file_unsupported(mock_print):
    result = sim_getter(model_file="test.bngl", sim_type="unsupported")
    mock_print.assert_called_once_with("simulator type unsupported not supported")
    assert result is None


@patch("os.remove")
@patch("bionetgen.simulator.simulators.libRRSimulator")
@patch("tempfile.NamedTemporaryFile")
def test_sim_getter_model_str_libRR(mock_ntf, mock_libRR, mock_remove):
    mock_libRR.return_value = "mock_libRR_instance"

    mock_file_obj = mock_ntf.return_value.__enter__.return_value
    mock_file_obj.name = "temp_model_str.bngl"

    result = sim_getter(model_str="model_content", sim_type="libRR")

    mock_file_obj.write.assert_called_once_with("model_content")
    mock_file_obj.seek.assert_called_once_with(0)
    mock_libRR.assert_called_once_with(model_file="temp_model_str.bngl")
    mock_remove.assert_called_with("temp_model_str.bngl")
    assert result == "mock_libRR_instance"


@patch("os.remove")
@patch("bionetgen.simulator.simulators.CSimulator")
@patch("tempfile.NamedTemporaryFile")
def test_sim_getter_model_str_cpy(mock_ntf, mock_cpy, mock_remove):
    mock_cpy.return_value = "mock_cpy_instance"

    mock_file_obj = mock_ntf.return_value.__enter__.return_value
    mock_file_obj.name = "temp_model_str.bngl"

    result = sim_getter(model_str="model_content", sim_type="cpy")

    mock_file_obj.write.assert_called_once_with("model_content")
    mock_cpy.assert_called_once_with(
        model_file="temp_model_str.bngl", generate_network=True
    )
    mock_remove.assert_called_with("temp_model_str.bngl")
    assert result == "mock_cpy_instance"


@patch("tempfile.NamedTemporaryFile")
@patch("builtins.print")
def test_sim_getter_model_str_unsupported(mock_print, mock_ntf):
    mock_file_obj = mock_ntf.return_value.__enter__.return_value
    mock_file_obj.name = "temp_model_str.bngl"

    result = sim_getter(model_str="model_content", sim_type="unsupported")

    assert mock_print.call_count == 2
    mock_print.assert_any_call("simulator type unsupported not supported")
    assert result is None


def test_sim_getter_neither_provided():
    result = sim_getter()
    assert result is None
