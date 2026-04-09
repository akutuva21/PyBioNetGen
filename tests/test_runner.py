import os
import pytest
from unittest.mock import patch, MagicMock

import bionetgen.modelapi.runner as runner

def test_runner_run_with_out():
    with patch("bionetgen.modelapi.runner.BNGCLI") as mock_cli_class:
        with patch("os.chdir") as mock_chdir:
            mock_cli_inst = MagicMock()
            mock_cli_class.return_value = mock_cli_inst
            mock_cli_inst.result = "mock_result"

            cur_dir = os.getcwd()
            res = runner.run("test.bngl", out="out_dir")

            mock_cli_class.assert_called_once_with("test.bngl", "out_dir", runner.conf["bngpath"], suppress=False, timeout=None)
            mock_cli_inst.run.assert_called_once()
            mock_chdir.assert_called_once_with(cur_dir)
            assert res == "mock_result"

def test_runner_run_without_out():
    with patch("bionetgen.modelapi.runner.BNGCLI") as mock_cli_class:
        with patch("bionetgen.modelapi.runner.TemporaryDirectory") as mock_tempdir:
            with patch("os.chdir") as mock_chdir:
                mock_tempdir.return_value.__enter__.return_value = "temp_dir"
                mock_cli_inst = MagicMock()
                mock_cli_class.return_value = mock_cli_inst
                mock_cli_inst.result = "mock_result"

                cur_dir = os.getcwd()
                res = runner.run("test.bngl")

                mock_cli_class.assert_called_once_with("test.bngl", "temp_dir", runner.conf["bngpath"], suppress=False, timeout=None)
                mock_cli_inst.run.assert_called_once()
                mock_chdir.assert_called_once_with(cur_dir)
                assert res == "mock_result"

def test_runner_run_exception_with_out():
    with patch("bionetgen.modelapi.runner.BNGCLI") as mock_cli_class:
        with patch("os.chdir") as mock_chdir:
            mock_cli_inst = MagicMock()
            mock_cli_class.return_value = mock_cli_inst
            mock_cli_inst.run.side_effect = RuntimeError("Run failed")

            cur_dir = os.getcwd()
            with pytest.raises(RuntimeError):
                runner.run("test.bngl", out="out_dir")

            mock_chdir.assert_called_once_with(cur_dir)

def test_runner_run_exception_without_out():
    with patch("bionetgen.modelapi.runner.BNGCLI") as mock_cli_class:
        with patch("bionetgen.modelapi.runner.TemporaryDirectory") as mock_tempdir:
            with patch("os.chdir") as mock_chdir:
                mock_tempdir.return_value.__enter__.return_value = "temp_dir"
                mock_cli_inst = MagicMock()
                mock_cli_class.return_value = mock_cli_inst
                mock_cli_inst.run.side_effect = RuntimeError("Run failed")

                cur_dir = os.getcwd()
                with pytest.raises(RuntimeError):
                    runner.run("test.bngl")

                mock_chdir.assert_called_once_with(cur_dir)
