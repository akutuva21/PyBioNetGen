import pytest
from unittest.mock import patch, MagicMock
from bionetgen.main import BioNetGenTest
import os

tfold = os.path.dirname(__file__)


@patch("bionetgen.core.main.subprocess.Popen")
def test_bionetgen_notebook(mock_popen, tmp_path):
    # Mocking subprocess Popen to avoid actually opening nbopen
    mock_process = MagicMock()
    mock_process.wait.return_value = 0
    mock_popen.return_value = mock_process

    # create a dummy file for the notebook
    dummy_bngl = tmp_path / "dummy_test.bngl"
    dummy_bngl.write_text("begin model\nend model\n")

    test_notebook = tmp_path / "test_notebook.ipynb"

    # To avoid the bngmodel error, we'll patch bionetgen.bngmodel instead of bionetgen.core.main.bngmodel
    with patch("bionetgen.bngmodel") as mock_bngmodel:
        mock_bngmodel_instance = MagicMock()
        mock_bngmodel.return_value = mock_bngmodel_instance

        argv = [
            "notebook",
            "-i",
            str(dummy_bngl),
            "-o",
            str(test_notebook),
            "--open",
        ]
        with BioNetGenTest(argv=argv) as app:
            app.run()
            assert app.exit_code == 0

    # Ensure subprocess.Popen was called with expected arguments
    found_nbopen = False
    for c in mock_popen.call_args_list:
        if "nbopen" in c[0][0]:
            assert str(test_notebook) in c[0][0]
            found_nbopen = True
            break
    assert found_nbopen, "nbopen was not called"


@patch("bionetgen.core.main.subprocess.Popen")
def test_bionetgen_notebook_attribute_error(mock_popen, tmp_path):
    import subprocess

    mock_process = MagicMock()
    mock_process.wait.return_value = 0
    mock_popen.return_value = mock_process

    test_notebook = tmp_path / "test_notebook_attr_error.ipynb"

    argv = [
        "notebook",
        "-o",
        str(test_notebook),
        "--open",
    ]
    with BioNetGenTest(argv=argv) as app:
        app.config.set("bionetgen", "stdout", "INVALID_ATTR")
        app.config.set("bionetgen", "stderr", "INVALID_ATTR")
        app.run()
        assert app.exit_code == 0

    found_nbopen = False
    for c in mock_popen.call_args_list:
        if "nbopen" in c[0][0]:
            assert str(test_notebook) in c[0][0]
            assert c[1].get("stdout") == subprocess.PIPE
            assert c[1].get("stderr") == subprocess.STDOUT
            found_nbopen = True
            break
    assert found_nbopen, "nbopen was not called"


@patch("bionetgen.core.main.subprocess.Popen")
def test_bionetgen_notebook_key_error(mock_popen, tmp_path):
    import subprocess

    mock_process = MagicMock()
    mock_process.wait.return_value = 0
    mock_popen.return_value = mock_process

    test_notebook = tmp_path / "test_notebook_key_error.ipynb"

    argv = [
        "notebook",
        "-o",
        str(test_notebook),
        "--open",
    ]
    with BioNetGenTest(argv=argv) as app:
        del app.config["bionetgen"]["stdout"]
        del app.config["bionetgen"]["stderr"]
        app.run()
        assert app.exit_code == 0

    found_nbopen = False
    for c in mock_popen.call_args_list:
        if "nbopen" in c[0][0]:
            assert str(test_notebook) in c[0][0]
            assert c[1].get("stdout") == subprocess.PIPE
            assert c[1].get("stderr") == subprocess.STDOUT
            found_nbopen = True
            break
    assert found_nbopen, "nbopen was not called"


@patch("bionetgen.core.main.subprocess.Popen")
def test_bionetgen_notebook_no_input(mock_popen, tmp_path):
    # Mocking subprocess Popen to avoid actually opening nbopen
    mock_process = MagicMock()
    mock_process.wait.return_value = 0
    mock_popen.return_value = mock_process

    test_notebook = tmp_path / "test_notebook_no_input.ipynb"

    argv = [
        "notebook",
        "-o",
        str(test_notebook),
        "--open",
    ]
    with BioNetGenTest(argv=argv) as app:
        app.run()
        assert app.exit_code == 0

    # Ensure subprocess.Popen was called with expected arguments
    found_nbopen = False
    for c in mock_popen.call_args_list:
        if "nbopen" in c[0][0]:
            assert str(test_notebook) in c[0][0]
            found_nbopen = True
            break
    assert found_nbopen, "nbopen was not called"
