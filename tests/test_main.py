import pytest
from unittest.mock import patch, MagicMock
import signal

from bionetgen.main import main, BioNetGen
from bionetgen.core.exc import BNGError
from cement.core.exc import CaughtSignal


def test_main_successful_run():
    with patch("bionetgen.main.BioNetGen") as mock_app_class:
        mock_app = MagicMock()
        mock_app_class.return_value.__enter__.return_value = mock_app

        main()

        mock_app.run.assert_called_once()
        mock_app.log.error.assert_not_called()


def test_main_assertion_error():
    with patch("bionetgen.main.BioNetGen") as mock_app_class:
        mock_app = MagicMock()
        mock_app.run.side_effect = AssertionError("Test Assertion")
        mock_app.debug = False
        mock_app_class.return_value.__enter__.return_value = mock_app

        main()

        mock_app.run.assert_called_once()
        mock_app.log.error.assert_called_with("AssertionError > Test Assertion")
        assert mock_app.exit_code == 1


def test_main_bng_error():
    with patch("bionetgen.main.BioNetGen") as mock_app_class:
        mock_app = MagicMock()
        mock_app.run.side_effect = BNGError("Test BNG Error")
        mock_app.debug = False
        mock_app_class.return_value.__enter__.return_value = mock_app

        main()

        mock_app.run.assert_called_once()
        mock_app.log.error.assert_called_with("BNGError > Test BNG Error")
        assert mock_app.exit_code == 1


def test_main_caught_signal_error(capsys):
    with patch("bionetgen.main.BioNetGen") as mock_app_class:
        mock_app = MagicMock()
        # Mocking the initialization of CaughtSignal with appropriate signal arguments
        mock_app.run.side_effect = CaughtSignal(
            signal.SIGINT, signal.getsignal(signal.SIGINT)
        )
        mock_app_class.return_value.__enter__.return_value = mock_app

        main()

        mock_app.run.assert_called_once()
        captured = capsys.readouterr()
        # Verify that the message was printed to stdout
        assert "Caught signal" in captured.out
        assert mock_app.exit_code == 0
