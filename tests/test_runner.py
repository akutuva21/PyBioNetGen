import os
import unittest
from unittest.mock import patch, MagicMock

# Assuming the runner can be imported like this
from bionetgen.modelapi.runner import run


class TestRunner(unittest.TestCase):
    @patch("bionetgen.modelapi.runner.BNGCLI")
    @patch("bionetgen.modelapi.runner.TemporaryDirectory")
    @patch("bionetgen.modelapi.runner.os.chdir")
    def test_run_with_no_out(self, mock_chdir, mock_temp_dir, mock_bngcli):
        # Setup mocks
        mock_temp_dir.return_value.__enter__.return_value = "/tmp/mocked"
        mock_cli_instance = MagicMock()
        mock_cli_instance.result = "mocked_result"
        mock_bngcli.return_value = mock_cli_instance

        # Execute
        result = run("mock_input.bngl")

        # Verify
        mock_temp_dir.assert_called_once()
        mock_bngcli.assert_called_once_with(
            "mock_input.bngl",
            "/tmp/mocked",
            unittest.mock.ANY,
            suppress=False,
            timeout=None,
        )
        mock_cli_instance.run.assert_called_once()
        self.assertEqual(
            mock_chdir.call_count, 1
        )  # should return to original directory
        self.assertEqual(result, "mocked_result")

    @patch("bionetgen.modelapi.runner.BNGCLI")
    @patch("bionetgen.modelapi.runner.os.chdir")
    def test_run_with_out(self, mock_chdir, mock_bngcli):
        # Setup mocks
        mock_cli_instance = MagicMock()
        mock_cli_instance.result = "mocked_result"
        mock_bngcli.return_value = mock_cli_instance

        # Execute
        result = run("mock_input.bngl", out="/custom/out")

        # Verify
        mock_bngcli.assert_called_once_with(
            "mock_input.bngl",
            "/custom/out",
            unittest.mock.ANY,
            suppress=False,
            timeout=None,
        )
        mock_cli_instance.run.assert_called_once()
        self.assertEqual(mock_chdir.call_count, 1)
        self.assertEqual(result, "mocked_result")

    @patch("bionetgen.modelapi.runner.BNGCLI")
    @patch("bionetgen.modelapi.runner.TemporaryDirectory")
    @patch("bionetgen.modelapi.runner.os.chdir")
    def test_run_with_no_out_exception(self, mock_chdir, mock_temp_dir, mock_bngcli):
        # Setup mocks
        mock_temp_dir.return_value.__enter__.return_value = "/tmp/mocked"
        mock_cli_instance = MagicMock()
        mock_cli_instance.run.side_effect = Exception("Test exception")
        mock_bngcli.return_value = mock_cli_instance

        # Execute and Verify
        with self.assertRaises(Exception) as context:
            run("mock_input.bngl")

        self.assertTrue("Test exception" in str(context.exception))
        mock_temp_dir.assert_called_once()
        mock_bngcli.assert_called_once_with(
            "mock_input.bngl",
            "/tmp/mocked",
            unittest.mock.ANY,
            suppress=False,
            timeout=None,
        )
        mock_cli_instance.run.assert_called_once()
        self.assertEqual(
            mock_chdir.call_count, 1
        )  # Exception handling restores directory

    @patch("bionetgen.modelapi.runner.BNGCLI")
    @patch("bionetgen.modelapi.runner.os.chdir")
    def test_run_with_out_exception(self, mock_chdir, mock_bngcli):
        # Setup mocks
        mock_cli_instance = MagicMock()
        mock_cli_instance.run.side_effect = Exception("Test exception")
        mock_bngcli.return_value = mock_cli_instance

        # Execute and Verify
        with self.assertRaises(Exception) as context:
            run("mock_input.bngl", out="/custom/out")

        self.assertTrue("Test exception" in str(context.exception))
        mock_bngcli.assert_called_once_with(
            "mock_input.bngl",
            "/custom/out",
            unittest.mock.ANY,
            suppress=False,
            timeout=None,
        )
        mock_cli_instance.run.assert_called_once()
        self.assertEqual(
            mock_chdir.call_count, 1
        )  # Exception handling restores directory


if __name__ == "__main__":
    unittest.main()
