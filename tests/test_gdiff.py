import pytest
import copy
from bionetgen.core.tools.gdiff import BNGGdiff


def test_gdiff_init():
    inp1 = "tests/models/testviz1_cm.graphml"
    inp2 = "tests/models/testviz2_cm.graphml"

    # Test valid modes
    gdiff = BNGGdiff(inp1, inp2, mode="matrix")
    assert gdiff.mode == "matrix"

    gdiff = BNGGdiff(inp1, inp2, mode="union")
    assert gdiff.mode == "union"

    # Test invalid mode
    with pytest.raises(ValueError, match="Mode invalid is not a valid mode"):
        BNGGdiff(inp1, inp2, mode="invalid")

    # Test colors
    gdiff = BNGGdiff(inp1, inp2, colors=None)
    assert "g1" in gdiff.colors
    assert "intersect" in gdiff.colors

    with pytest.raises(ValueError, match="Color type .* not recognized"):
        BNGGdiff(inp1, inp2, colors=123)


def test_gdiff_run_matrix(tmp_path):
    inp1 = "tests/models/testviz1_cm.graphml"
    inp2 = "tests/models/testviz2_cm.graphml"

    out1 = str(tmp_path / "out1.graphml")
    out2 = str(tmp_path / "out2.graphml")

    gdiff = BNGGdiff(inp1, inp2, out=out1, out2=out2, mode="matrix")
    graphs = gdiff.run()

    assert out1 in graphs
    assert out2 in graphs
    assert len(graphs) == 4  # diff1, diff2, recolor1, recolor2


def test_gdiff_run_union(tmp_path):
    inp1 = "tests/models/testviz1_cm.graphml"
    inp2 = "tests/models/testviz2_cm.graphml"

    out1 = str(tmp_path / "out_union.graphml")

    gdiff = BNGGdiff(inp1, inp2, out=out1, mode="union")
    graphs = gdiff.run()

    assert out1 in graphs
    assert len(graphs) == 1


# Minimal mock node dict that satisfies _get_node_properties
mock_node_grey = {
    "@id": "n0",
    "data": {
        "y:ShapeNode": {
            "y:NodeLabel": {"#text": "MockSpecies", "@fontSize": "12"},
            "y:Fill": {"@color": "#D2D2D2"},
        }
    },
}

mock_node_white = copy.deepcopy(mock_node_grey)
mock_node_white["data"]["y:ShapeNode"]["y:NodeLabel"]["#text"] = "MockComponent"
mock_node_white["data"]["y:ShapeNode"]["y:Fill"]["@color"] = "#FFFFFF"

mock_node_yellow = copy.deepcopy(mock_node_grey)
mock_node_yellow["data"]["y:ShapeNode"]["y:NodeLabel"]["#text"] = "MockState"
mock_node_yellow["data"]["y:ShapeNode"]["y:Fill"]["@color"] = "#FFCC00"

mock_node_unknown = copy.deepcopy(mock_node_grey)
mock_node_unknown["data"]["y:ShapeNode"]["y:Fill"]["@color"] = "#000000"

mock_node_group = {
    "@id": "n1",
    "data": [
        {
            "y:ProxyAutoBoundsNode": {
                "y:Realizers": {
                    "y:GroupNode": [
                        {
                            "y:NodeLabel": {"#text": "MockGroup", "@fontSize": "14"},
                            "y:Fill": {"@color": "#D2D2D2"},
                        }
                    ]
                }
            }
        }
    ],
}


def test_gdiff_node_methods():
    inp1 = "tests/models/testviz1_cm.graphml"
    inp2 = "tests/models/testviz2_cm.graphml"
    gdiff = BNGGdiff(inp1, inp2)

    # test _get_node_properties
    props = gdiff._get_node_properties(mock_node_grey)
    assert props["y:NodeLabel"]["#text"] == "MockSpecies"

    props = gdiff._get_node_properties(mock_node_group)
    assert props["y:NodeLabel"]["#text"] == "MockGroup"

    # test _get_node_name
    assert gdiff._get_node_name(mock_node_grey) == "MockSpecies"
    assert gdiff._get_node_name(mock_node_white) == "MockComponent"

    # test _get_node_fill
    assert gdiff._get_node_fill(mock_node_grey)["@color"] == "#D2D2D2"

    # test _get_node_color
    assert gdiff._get_node_color(mock_node_grey) == "#D2D2D2"

    # test _get_font_size
    assert gdiff._get_font_size(mock_node_grey) == 12
    assert gdiff._get_font_size(mock_node_group) == 14

    # test _resize_node_font
    test_node = copy.deepcopy(mock_node_grey)
    gdiff._resize_node_font(test_node, 20)
    assert gdiff._get_font_size(test_node) == 20

    # test _get_color_id
    assert gdiff._get_color_id(mock_node_grey) == 0
    assert gdiff._get_color_id(mock_node_white) == 1
    assert gdiff._get_color_id(mock_node_yellow) == 2

    with pytest.raises(
        RuntimeError, match="Node color #000000 doesn't match known colors"
    ):
        gdiff._get_color_id(mock_node_unknown)

    # test _color_node
    test_node = copy.deepcopy(mock_node_grey)
    success = gdiff._color_node(test_node, "#FF0000")
    assert success
    assert gdiff._get_node_color(test_node) == "#FF0000"
