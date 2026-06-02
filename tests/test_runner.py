import os
import pytest
from unittest.mock import patch, MagicMock, ANY
from bionetgen.modelapi.runner import run


@patch("bionetgen.modelapi.runner.BNGCLI")
def test_runner_with_out(mock_bngcli):
    mock_cli_instance = MagicMock()
    mock_bngcli.return_value = mock_cli_instance
    mock_cli_instance.result = "mock_result"

    inp = "test.bngl"
    out = "test_out"

    result = run(inp, out=out, suppress=True, timeout=10)

    mock_bngcli.assert_called_once_with(inp, out, ANY, suppress=True, timeout=10)
    mock_cli_instance.run.assert_called_once()
    assert result == "mock_result"


@patch("bionetgen.modelapi.runner.BNGCLI")
@patch("tempfile.mkdtemp")
def test_runner_without_out(mock_mkdtemp, mock_bngcli):
    mock_cli_instance = MagicMock()
    mock_bngcli.return_value = mock_cli_instance
    mock_cli_instance.result = "mock_result"

    mock_mkdtemp.return_value = "temp_out"

    inp = "test.bngl"

    result = run(inp, suppress=False, timeout=None)

    mock_mkdtemp.assert_called_once()
    mock_bngcli.assert_called_once_with(
        inp, "temp_out", ANY, suppress=False, timeout=None
    )
    mock_cli_instance.run.assert_called_once()
    assert result == "mock_result"


@patch("bionetgen.modelapi.runner.BNGCLI")
def test_runner_exception(mock_bngcli):
    mock_cli_instance = MagicMock()
    mock_bngcli.return_value = mock_cli_instance
    mock_cli_instance.run.side_effect = Exception("Test Exception")

    inp = "test.bngl"
    out = "test_out"

    with pytest.raises(Exception, match="Test Exception"):
        run(inp, out=out)

@patch("bionetgen.modelapi.runner.logger")
@patch("bionetgen.modelapi.runner.BNGCLI")
def test_runner_exception_with_stdout_stderr(mock_bngcli, mock_logger):
    mock_cli_instance = MagicMock()
    mock_bngcli.return_value = mock_cli_instance

    class CustomException(Exception):
        def __init__(self, message, stdout, stderr):
            super().__init__(message)
            self.stdout = stdout
            self.stderr = stderr

    mock_cli_instance.run.side_effect = CustomException("Test Exception", "test stdout", "test stderr")

    inp = "test.bngl"
    out = "test_out"

    with pytest.raises(CustomException, match="Test Exception"):
        run(inp, out=out)

    mock_logger.error.assert_any_call("Couldn't run the simulation, see error")
    mock_logger.error.assert_any_call("STDOUT:\ntest stdout")
    mock_logger.error.assert_any_call("STDERR:\ntest stderr")


@patch("bionetgen.modelapi.runner.logger")
@patch("bionetgen.modelapi.runner.BNGCLI")
@patch("tempfile.mkdtemp")
def test_runner_exception_without_out(mock_mkdtemp, mock_bngcli, mock_logger):
    mock_cli_instance = MagicMock()
    mock_bngcli.return_value = mock_cli_instance

    class CustomException(Exception):
        def __init__(self, message, stdout, stderr):
            super().__init__(message)
            self.stdout = stdout
            self.stderr = stderr

    mock_cli_instance.run.side_effect = CustomException("Test Exception", "test stdout", "test stderr")

    mock_mkdtemp.return_value = "temp_out"
    inp = "test.bngl"

    with pytest.raises(CustomException, match="Test Exception"):
        run(inp, suppress=False, timeout=None)

    mock_logger.error.assert_any_call("Couldn't run the simulation, see error")
    mock_logger.error.assert_any_call("STDOUT:\ntest stdout")
    mock_logger.error.assert_any_call("STDERR:\ntest stderr")
