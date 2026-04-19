import pytest
from unittest.mock import patch


def test_bngexec_success():
    from bionetgen.core.utils.utils import test_bngexec

    with patch("bionetgen.core.utils.utils.run_command") as mock_run_command:
        # Mock successful run where return code is 0
        mock_run_command.return_value = (0, "output")

        result = test_bngexec("path/to/BNG2.pl")

        assert result is True
        mock_run_command.assert_called_once_with(["perl", "path/to/BNG2.pl"])


def test_bngexec_failure():
    from bionetgen.core.utils.utils import test_bngexec

    with patch("bionetgen.core.utils.utils.run_command") as mock_run_command:
        # Mock failed run where return code is non-zero
        mock_run_command.return_value = (1, "error")

        result = test_bngexec("path/to/BNG2.pl")

        assert result is False
        mock_run_command.assert_called_once_with(["perl", "path/to/BNG2.pl"])


@patch("bionetgen.core.utils.utils.test_bngexec")
def test_find_BNG_path_explicit_dir(mock_test_bngexec):
    from bionetgen.core.utils.utils import find_BNG_path

    # Mock successful execution
    mock_test_bngexec.return_value = True

    # Test passing a directory explicitly
    dir_path = "/path/to/bng/dir"
    result = find_BNG_path(dir_path)

    assert result == (dir_path, f"{dir_path}/BNG2.pl")
    mock_test_bngexec.assert_called_once_with(f"{dir_path}/BNG2.pl")


@patch("bionetgen.core.utils.utils.test_bngexec")
def test_find_BNG_path_explicit_file(mock_test_bngexec):
    from bionetgen.core.utils.utils import find_BNG_path

    # Mock successful execution
    mock_test_bngexec.return_value = True

    # Test passing a file directly
    file_path = "/path/to/bng/dir/BNG2.pl"
    dir_path = "/path/to/bng/dir"
    result = find_BNG_path(file_path)

    assert result == (dir_path, file_path)
    mock_test_bngexec.assert_called_once_with(file_path)


@patch("bionetgen.core.utils.utils.test_bngexec")
@patch("os.environ.get")
def test_find_BNG_path_env_var(mock_env_get, mock_test_bngexec):
    from bionetgen.core.utils.utils import find_BNG_path

    # Setup mocks
    env_dir = "/env/path/to/bng"
    mock_env_get.return_value = env_dir
    mock_test_bngexec.return_value = True

    result = find_BNG_path()

    assert result == (env_dir, f"{env_dir}/BNG2.pl")
    mock_env_get.assert_called_once_with("BNGPATH")
    mock_test_bngexec.assert_called_once_with(f"{env_dir}/BNG2.pl")


@patch("bionetgen.core.utils.utils.test_bngexec")
@patch("os.environ.get")
@patch("bionetgen.core.utils.utils.spawn.which")
def test_find_BNG_path_on_path(mock_which, mock_env_get, mock_test_bngexec):
    from bionetgen.core.utils.utils import find_BNG_path

    # Setup mocks: explicitly None for previous checks, valid for this one
    mock_env_get.return_value = None

    path_file = "/usr/local/bin/BNG2.pl"
    path_dir = "/usr/local/bin"
    mock_which.return_value = path_file
    mock_test_bngexec.return_value = True

    result = find_BNG_path()

    assert result == (path_dir, path_file)
    mock_env_get.assert_called_once_with("BNGPATH")
    mock_which.assert_called_once_with("BNG2.pl")
    mock_test_bngexec.assert_called_once_with(path_file)


@patch("bionetgen.core.utils.utils.test_bngexec")
@patch("os.environ.get")
@patch("bionetgen.core.utils.utils.spawn.which")
def test_find_BNG_path_not_found(mock_which, mock_env_get, mock_test_bngexec):
    from bionetgen.core.utils.utils import find_BNG_path

    # Setup mocks to fail everything
    mock_env_get.return_value = None
    mock_which.return_value = None

    # Should test_bngexec get called? Probably not if paths are None,
    # but let's mock it just in case
    mock_test_bngexec.return_value = False

    result = find_BNG_path()

    assert result == (None, None)
    mock_env_get.assert_called_once_with("BNGPATH")
    mock_which.assert_called_once_with("BNG2.pl")
    # test_bngexec should not be called because no valid paths were found
    mock_test_bngexec.assert_not_called()
