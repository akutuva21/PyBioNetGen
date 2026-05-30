import pytest
from bionetgen.core.tools.gdiff import BNGGdiff


def test_get_node_from_keylist_base_case(tmp_path):
    dummy_file = tmp_path / "dummy.graphml"
    dummy_file.write_text("<graphml></graphml>")

    gdiff = BNGGdiff(str(dummy_file), str(dummy_file))
    mock_graph = {"graphml": {"node": "value"}}
    result = gdiff._get_node_from_keylist(mock_graph, ["graphml"])
    assert result == {"node": "value"}


def test_get_node_from_keylist_no_graph(tmp_path):
    dummy_file = tmp_path / "dummy.graphml"
    dummy_file.write_text("<graphml></graphml>")

    gdiff = BNGGdiff(str(dummy_file), str(dummy_file))
    mock_graph = {"graphml": {}}
    result = gdiff._get_node_from_keylist(mock_graph, ["graphml", "n1"])
    assert result is None


def test_get_node_from_keylist_list_nodes(tmp_path):
    dummy_file = tmp_path / "dummy.graphml"
    dummy_file.write_text("<graphml></graphml>")

    gdiff = BNGGdiff(str(dummy_file), str(dummy_file))
    mock_graph = {
        "graphml": {
            "graph": {"node": [{"@id": "n1", "val": 1}, {"@id": "n2", "val": 2}]}
        }
    }
    result = gdiff._get_node_from_keylist(mock_graph, ["graphml", "n2"])
    assert result == {"@id": "n2", "val": 2}


def test_get_node_from_keylist_single_dict_node(tmp_path):
    dummy_file = tmp_path / "dummy.graphml"
    dummy_file.write_text("<graphml></graphml>")

    gdiff = BNGGdiff(str(dummy_file), str(dummy_file))
    mock_graph = {"graphml": {"graph": {"node": {"@id": "n1", "val": 1}}}}
    result = gdiff._get_node_from_keylist(mock_graph, ["graphml", "n1"])
    assert result == {"@id": "n1", "val": 1}


def test_get_node_from_keylist_nested(tmp_path):
    dummy_file = tmp_path / "dummy.graphml"
    dummy_file.write_text("<graphml></graphml>")

    gdiff = BNGGdiff(str(dummy_file), str(dummy_file))
    mock_graph = {
        "graphml": {
            "graph": {
                "node": {
                    "@id": "group1",
                    "graph": {
                        "node": [
                            {"@id": "inner1", "val": 10},
                            {"@id": "inner2", "val": 20},
                        ]
                    },
                }
            }
        }
    }
    result = gdiff._get_node_from_keylist(mock_graph, ["graphml", "group1", "inner2"])
    assert result == {"@id": "inner2", "val": 20}


def test_get_node_from_keylist_nested_not_found(tmp_path):
    dummy_file = tmp_path / "dummy.graphml"
    dummy_file.write_text("<graphml></graphml>")

    gdiff = BNGGdiff(str(dummy_file), str(dummy_file))
    mock_graph = {
        "graphml": {
            "graph": {
                "node": {
                    "@id": "group1",
                    "graph": {"node": [{"@id": "inner1", "val": 10}]},
                }
            }
        }
    }
    result = gdiff._get_node_from_keylist(
        mock_graph, ["graphml", "group1", "inner_missing"]
    )
    assert result is None
