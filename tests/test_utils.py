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
