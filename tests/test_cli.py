import os
import pytest
from unittest.mock import patch, MagicMock
from bionetgen.core.tools.cli import BNGCLI
from bionetgen.core.exc import BNGRunError


@patch("bionetgen.core.utils.utils.find_BNG_path")
def test_bngcli_init(mock_find_bng_path):
    mock_find_bng_path.return_value = ("/fake/bng/path", "/fake/bng/path/BNG2.pl")
    cli = BNGCLI("test.bngl", "output_dir", "/fake/bng/path")
    assert cli.inp_file == "test.bngl"
    assert cli.output == os.path.abspath("output_dir")
    assert cli.bngpath == "/fake/bng/path"
    assert cli.bng_exec == "/fake/bng/path/BNG2.pl"
    assert not cli.is_bngmodel


@patch("bionetgen.core.utils.utils.find_BNG_path")
def test_bngcli_init_bngmodel(mock_find_bng_path):
    mock_find_bng_path.return_value = ("/fake/bng/path", "/fake/bng/path/BNG2.pl")

    class MockModel:
        pass

    mock_model = MockModel()

    with patch("bionetgen.modelapi.model.bngmodel", MockModel):
        cli = BNGCLI(mock_model, "output_dir", "/fake/bng/path")
        assert cli.inp_file == mock_model
        assert cli.is_bngmodel


@patch("bionetgen.core.utils.utils.find_BNG_path")
def test_bngcli_init_invalid_bngpath(mock_find_bng_path):
    mock_find_bng_path.side_effect = Exception("Not found")
    with pytest.raises(AssertionError):
        BNGCLI("test.bngl", "output_dir", "/invalid/bng/path")


@patch("bionetgen.core.utils.utils.find_BNG_path")
@patch("bionetgen.core.utils.utils.run_command")
@patch("bionetgen.core.tools.BNGResult")
def test_bngcli_run_success(mock_bngresult, mock_run_command, mock_find_bng_path):
    mock_find_bng_path.return_value = ("/fake/bng/path", "/fake/bng/path/BNG2.pl")
    # For success, BNGCLI expects the second return from run_command to be iterable (list of lines) for writing logs
    # and it just sets it as result.output
    mock_run_command.return_value = (0, ["output line 1", "output line 2"])

    cli = BNGCLI("test.bngl", "output_dir", "/fake/bng/path")
    cli.run()

    mock_run_command.assert_called_once()
    mock_bngresult.assert_called_once_with(os.path.abspath("output_dir"))
    assert cli.result == mock_bngresult.return_value
    assert cli.result.process_return == 0
    assert cli.result.output == ["output line 1", "output line 2"]


@patch("bionetgen.core.utils.utils.find_BNG_path")
@patch("bionetgen.core.utils.utils.run_command")
def test_bngcli_run_failure(mock_run_command, mock_find_bng_path):
    mock_find_bng_path.return_value = ("/fake/bng/path", "/fake/bng/path/BNG2.pl")
    # In BNGCLI failure logic, it checks if the second return value has .stdout and .stderr
    # This matches the subprocess.run or process return from run_command.
    mock_out = MagicMock()
    mock_out.stdout = b"error in stdout"
    mock_out.stderr = b"error in stderr"
    mock_run_command.return_value = (1, mock_out)

    cli = BNGCLI("test.bngl", "output_dir", "/fake/bng/path")

    with pytest.raises(BNGRunError) as exc_info:
        cli.run()

    assert "error in stdout" in str(exc_info.value)


@patch("bionetgen.core.utils.utils.find_BNG_path")
@patch("bionetgen.core.tools.BNGResult")
def test_bngcli_run_fallback(mock_bngresult, mock_find_bng_path):
    mock_find_bng_path.return_value = ("/fake/bng/path", None)

    cli = BNGCLI("test.bngl", "output_dir", "/fake/bng/path")
    cli.run()

    mock_bngresult.assert_called_once_with(os.path.abspath("output_dir"))
    assert cli.result == mock_bngresult.return_value
    assert cli.result.process_return == 0
    assert cli.result.output == []


@patch("bionetgen.core.utils.utils.find_BNG_path")
@patch("bionetgen.core.utils.utils.run_command")
def test_bngcli_run_invalid_stdout_stderr(mock_run_command, mock_find_bng_path):
    mock_find_bng_path.return_value = ("/fake/bng/path", "/fake/bng/path/BNG2.pl")
    mock_run_command.return_value = (0, ["output line 1"])

    cli = BNGCLI("test.bngl", "output_dir", "/fake/bng/path")
    cli.stdout = "INVALID_STDOUT"
    cli.stderr = "INVALID_STDERR"

    cli.run()

    mock_run_command.assert_called_once()
