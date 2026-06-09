import copy
import json
from unittest import mock

import pytest
import xmltodict

from bionetgen.core.exc import BNGFileError
from bionetgen.core.tools.gdiff import BNGGdiff


def _make_shape_node(name, color, node_id, font_size="12"):
    return {
        "@id": node_id,
        "data": {
            "@key": "d6",
            "y:ShapeNode": {
                "y:Geometry": {"@height": "30", "@width": "30"},
                "y:Fill": {"@color": color, "@transparent": "false"},
                "y:NodeLabel": {"#text": name, "@fontSize": font_size},
            },
        },
    }


def _make_group_node(name, color, node_id, children, font_size="12"):
    child_nodes = children if len(children) != 1 else children[0]
    return {
        "@id": node_id,
        "data": [
            {"@key": "d4"},
            {
                "@key": "d6",
                "y:ProxyAutoBoundsNode": {
                    "y:Realizers": {
                        "y:GroupNode": {
                            "y:Geometry": {"@height": "80", "@width": "120"},
                            "y:Fill": {"@color": color, "@transparent": "false"},
                            "y:NodeLabel": {"#text": name, "@fontSize": font_size},
                        }
                    }
                },
            },
        ],
        "graph": {"@id": node_id + ":", "node": child_nodes},
    }


def _make_edge(edge_id, source, target):
    return {
        "@id": edge_id,
        "@source": source,
        "@target": target,
        "data": {"@key": "d10"},
    }


def _make_graphml(nodes, edges):
    return {
        "graphml": {
            "@xmlns": "http://graphml.graphstruct.org/graphml",
            "graph": {
                "@id": "G",
                "@edgedefault": "undirected",
                "node": nodes,
                "edge": edges,
            },
        }
    }


def _write_graphml(path, graph):
    with open(path, "w") as handle:
        xmltodict.unparse(graph, output=handle, pretty=True)


def _read_graphml(path):
    with open(path, "r") as handle:
        return xmltodict.parse(
            handle.read(), force_list=("node", "edge"), disable_entities=True
        )


GRAPH1 = _make_graphml(
    [
        _make_group_node(
            "A",
            "#D2D2D2",
            "n0",
            [
                _make_shape_node("a1", "#FFFFFF", "n0::n0"),
                _make_shape_node("a2", "#FFFFFF", "n0::n1"),
            ],
        ),
        _make_group_node(
            "B",
            "#D2D2D2",
            "n1",
            [_make_shape_node("b1", "#FFFFFF", "n1::n0")],
        ),
    ],
    [
        _make_edge("e0", "n0::n0", "n1::n0"),
        _make_edge("e1", "n0::n1", "n1::n0"),
    ],
)

GRAPH2 = _make_graphml(
    [
        _make_group_node(
            "A",
            "#D2D2D2",
            "n0",
            [_make_shape_node("a1", "#FFFFFF", "n0::n0")],
        ),
        _make_group_node(
            "C",
            "#D2D2D2",
            "n1",
            [_make_shape_node("c1", "#FFFFFF", "n1::n0")],
        ),
    ],
    [
        _make_edge("e0", "n0::n0", "n1::n0"),
        _make_edge("e1", "n1::n0", "n0::n0"),
    ],
)


def _make_gdiff(path1, path2):
    obj = BNGGdiff.__new__(BNGGdiff)
    from bionetgen.core.utils.logging import BNGLogger

    obj.app = None
    obj.logger = BNGLogger(app=None)
    obj.input = path1
    obj.input2 = path2
    obj.output = None
    obj.output2 = None
    obj.colors = {
        "g1": ["#dadbfd", "#e6e7fe", "#f3f3ff"],
        "g2": ["#ff9e81", "#ffbfaa", "#ffdfd4"],
        "intersect": ["#c4ed9e", "#d9f4be", "#ecf9df"],
    }
    obj.available_modes = ["matrix", "union"]
    obj.mode = "matrix"
    obj.gdict_1 = _read_graphml(path1)
    obj.gdict_2 = _read_graphml(path2)
    return obj


@pytest.fixture
def gdiff_obj(tmp_path):
    path1 = tmp_path / "g1.graphml"
    path2 = tmp_path / "g2.graphml"
    _write_graphml(path1, copy.deepcopy(GRAPH1))
    _write_graphml(path2, copy.deepcopy(GRAPH2))
    return _make_gdiff(str(path1), str(path2))


def test_get_color_id_unknown_raises_bng_file_error(gdiff_obj):
    node = _make_shape_node("x", "#123456", "n0")
    with pytest.raises(
        BNGFileError, match="doesn't match known BioNetGen contact-map colors"
    ):
        gdiff_obj._get_color_id(node)


def test_get_node_properties_shape_without_supported_node_type_raises(gdiff_obj):
    node = {"@id": "n0", "data": {"@key": "d6", "y:UnsupportedNode": {}}}
    with pytest.raises(BNGFileError, match="Could not find supported yEd properties"):
        gdiff_obj._get_node_properties(node)


def test_color_node_logs_and_raises_for_invalid_node(gdiff_obj):
    node = {"@id": "n0", "data": {"@key": "d6", "y:UnsupportedNode": {}}}
    with mock.patch.object(gdiff_obj.logger, "error") as mock_error:
        with pytest.raises(
            BNGFileError, match="Could not find supported yEd properties"
        ):
            gdiff_obj._color_node(node, "#AABBCC")
    mock_error.assert_called_once()
    assert "Couldn't color GraphML node n0" in mock_error.call_args.args[0]


def test_keylist_finds_nested_leaf_node(gdiff_obj):
    graph = copy.deepcopy(gdiff_obj.gdict_1)
    result = gdiff_obj._get_node_from_keylist(graph, ["graphml", "n0", "n0::n0"])
    assert result["@id"] == "n0::n0"
    assert gdiff_obj._get_node_name(result) == "a1"


def test_keylist_finds_leaf_in_single_dict_child_graph(gdiff_obj):
    graph = copy.deepcopy(gdiff_obj.gdict_1)
    result = gdiff_obj._get_node_from_keylist(graph, ["graphml", "n1", "n1::n0"])
    assert result["@id"] == "n1::n0"
    assert gdiff_obj._get_node_name(result) == "b1"
