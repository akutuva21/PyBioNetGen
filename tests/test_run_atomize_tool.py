import pytest
from unittest.mock import MagicMock, patch
import os
import json
from bionetgen.core.main import runAtomizeTool

def test_runAtomizeTool_basic():
    mock_app = MagicMock()
    mock_app.pargs.input = "test_model.xml"
    mock_app.pargs.write_scts = False
    mock_app.pargs.write_sct_graphs = False

    with patch("bionetgen.atomizer.AtomizeTool") as mock_atomize_tool:
        mock_atomize_instance = mock_atomize_tool.return_value

        mock_res_arr = MagicMock()
        mock_atomize_instance.run.return_value = mock_res_arr

        runAtomizeTool(mock_app)

        mock_atomize_tool.assert_called_once_with(parser_namespace=mock_app.pargs, app=mock_app)
        mock_atomize_instance.run.assert_called_once()

def test_runAtomizeTool_write_scts(tmp_path):
    mock_app = MagicMock()
    mock_app.pargs.input = "test_model.xml"
    mock_app.pargs.write_scts = True
    mock_app.pargs.write_sct_graphs = False

    with patch("bionetgen.atomizer.AtomizeTool") as mock_atomize_tool:
        mock_atomize_instance = mock_atomize_tool.return_value

        mock_res_arr = MagicMock()
        mock_res_arr.database.scts = {"graph1": {"node1": [["conn1", "conn2"]]}}
        mock_atomize_instance.run.return_value = mock_res_arr

        orig_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            runAtomizeTool(mock_app)

            assert os.path.exists("test_model_scts.json")
            with open("test_model_scts.json", "r") as f:
                data = json.load(f)
                assert data == {"graph1": {"node1": [["conn1", "conn2"]]}}

            assert not os.path.exists("test_model_graph1.graphml")
        finally:
            os.chdir(orig_cwd)

def test_runAtomizeTool_write_scts_and_graphs(tmp_path):
    mock_app = MagicMock()
    mock_app.pargs.input = "test_model.xml"
    mock_app.pargs.write_scts = True
    mock_app.pargs.write_sct_graphs = True

    with patch("bionetgen.atomizer.AtomizeTool") as mock_atomize_tool:
        mock_atomize_instance = mock_atomize_tool.return_value

        mock_res_arr = MagicMock()
        mock_res_arr.database.scts = {"graph1": {"node1": [["conn1", "conn2"]]}}
        mock_atomize_instance.run.return_value = mock_res_arr

        orig_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            runAtomizeTool(mock_app)

            assert os.path.exists("test_model_scts.json")
            assert os.path.exists("test_model_graph1.graphml")

            with open("test_model_graph1.graphml", "r") as f:
                content = f.read()
                assert "node1" in content
                assert "conn1" in content
                assert "conn2" in content
                assert "<graphml" in content
        finally:
            os.chdir(orig_cwd)
