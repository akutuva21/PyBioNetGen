import pytest
from bionetgen.core.tools.gdiff import BNGGdiff


def test_color_node_success():
    gdiff = BNGGdiff.__new__(BNGGdiff)
    node = {"data": {"y:ShapeNode": {"y:Fill": {"@color": "#000000"}}}}
    result = gdiff._color_node(node, "#FFFFFF")
    assert result is True
    assert node["data"]["y:ShapeNode"]["y:Fill"]["@color"] == "#FFFFFF"


def test_color_node_failure(capsys):
    gdiff = BNGGdiff.__new__(BNGGdiff)
    node = {"data": {}}
    result = gdiff._color_node(node, "#FFFFFF")
    assert result is False
    captured = capsys.readouterr()
    assert "Couldn't color node, error" in captured.out
