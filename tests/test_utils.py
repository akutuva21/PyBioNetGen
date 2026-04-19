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


def test_perl_success_explicit_path():
    from bionetgen.core.utils.utils import test_perl

    with patch("bionetgen.core.utils.utils.run_command") as mock_run_command:
        mock_run_command.return_value = (0, "output")
        test_perl(app=None, perl_path="/usr/bin/perl")
        mock_run_command.assert_called_once_with(["/usr/bin/perl", "-v"])


def test_perl_success_implicit_path():
    from bionetgen.core.utils.utils import test_perl

    with patch("bionetgen.core.utils.utils.run_command") as mock_run_command:
        with patch("bionetgen.core.utils.utils.spawn.which") as mock_which:
            mock_which.return_value = "/bin/perl"
            mock_run_command.return_value = (0, "output")
            test_perl(app=None)
            mock_which.assert_called_once_with("perl")
            mock_run_command.assert_called_once_with(["/bin/perl", "-v"])


def test_perl_missing_binary():
    from bionetgen.core.utils.utils import test_perl
    from bionetgen.core.exc import BNGPerlError

    with patch("bionetgen.core.utils.utils.spawn.which") as mock_which:
        mock_which.return_value = None
        with pytest.raises(BNGPerlError):
            test_perl(app=None)


def test_perl_execution_failure():
    from bionetgen.core.utils.utils import test_perl
    from bionetgen.core.exc import BNGPerlError

    with patch("bionetgen.core.utils.utils.run_command") as mock_run_command:
        mock_run_command.return_value = (1, "error")
        with pytest.raises(BNGPerlError):
            test_perl(app=None, perl_path="/usr/bin/perl")
        mock_run_command.assert_called_once_with(["/usr/bin/perl", "-v"])
