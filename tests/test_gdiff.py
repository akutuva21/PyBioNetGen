import pytest
import os
from bionetgen.core.tools.gdiff import BNGGdiff

def test_get_node_from_keylist(tmp_path):
    # Create dummy graphml files needed for instantiation
    dummy1 = tmp_path / "dummy1.graphml"
    dummy2 = tmp_path / "dummy2.graphml"
    dummy1.write_text('<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns" />')
    dummy2.write_text('<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns" />')

    gdiff = BNGGdiff(str(dummy1), str(dummy2))

    # 1. Base case: empty list after graphml
    graph1 = {"graphml": "dummy_val"}
    keylist1 = ["graphml"]
    assert gdiff._get_node_from_keylist(graph1, keylist1) == "dummy_val"

    # 2. Out of group nodes: no "graph" in g[gkey]
    graph2 = {"graphml": {"not_graph": {}}}
    keylist2 = ["graphml", "dummy_node"]
    assert gdiff._get_node_from_keylist(graph2, keylist2) is None

    # 3. Valid traversal to a specific node in a list
    graph3 = {
        "graphml": {
            "graph": {
                "node": [
                    {"@id": "n1", "val": 1},
                    {"@id": "n2", "val": 2}
                ]
            }
        }
    }
    keylist3 = ["graphml", "n2"]
    assert gdiff._get_node_from_keylist(graph3, keylist3) == {"@id": "n2", "val": 2}

    # 4. Valid traversal to a specific node (not a list)
    graph4 = {
        "graphml": {
            "graph": {
                "node": {"@id": "n1", "val": 1}
            }
        }
    }
    keylist4 = ["graphml", "n1"]
    assert gdiff._get_node_from_keylist(graph4, keylist4) == {"@id": "n1", "val": 1}

    # 5. Nested nodes traversal
    graph5 = {
        "graphml": {
            "graph": {
                "node": [
                    {
                        "@id": "group1",
                        "graph": {
                            "node": [
                                {"@id": "n1", "val": 1},
                                {"@id": "n2", "val": 2}
                            ]
                        }
                    }
                ]
            }
        }
    }
    keylist5 = ["graphml", "group1", "n2"]
    assert gdiff._get_node_from_keylist(graph5, keylist5) == {"@id": "n2", "val": 2}

    # 6. Not found node
    keylist6 = ["graphml", "group1", "n3"]
    assert gdiff._get_node_from_keylist(graph5, keylist6) is None
