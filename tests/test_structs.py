import pytest
from bionetgen.modelapi.structs import ModelObj


def test_modelobj_setitem():
    obj = ModelObj()
    obj["test_key"] = "test_value"
    assert obj.test_key == "test_value"
    assert obj["test_key"] == "test_value"


def test_modelobj_contains():
    obj = ModelObj()
    obj["test_key"] = "test_value"
    assert "test_key" in obj
    assert "wrong_key" not in obj


def test_modelobj_delitem():
    obj = ModelObj()
    obj["test_key"] = "test_value"
    del obj["test_key"]
    assert "test_key" not in obj


def test_modelobj_line_label_setter():
    obj = ModelObj()

    # Test setting a valid integer label
    obj.line_label = 10
    assert obj.line_label == "10 "

    # Test setting a valid string integer label
    obj.line_label = "20"
    assert obj.line_label == "20 "

    # Test ValueError (setting a non-integer string)
    obj.line_label = "invalid"
    assert obj.line_label == "invalid: "

    # Test TypeError (setting a non-string/non-integer like a list)
    obj.line_label = [1, 2, 3]
    assert obj.line_label == "[1, 2, 3]: "


from bionetgen.modelapi.structs import Observable


class MockPattern:
    def __init__(self, name, match_once=False):
        self.name = name
        self.MatchOnce = match_once

    def __str__(self):
        return self.name


def test_observable_gen_string():
    # Test with one pattern
    obs1 = Observable(name="O1", otype="Molecules", patterns=[MockPattern("P1")])
    assert obs1.gen_string() == "Molecules O1 P1"

    # Test with multiple patterns
    obs2 = Observable(
        name="O2", otype="Molecules", patterns=[MockPattern("P1"), MockPattern("P2")]
    )
    assert obs2.gen_string() == "Molecules O2 P1,P2"

    # Test with Species type which sets MatchOnce
    obs3 = Observable(
        name="S1", otype="Species", patterns=[MockPattern("P1", match_once=True)]
    )
    assert obs3.gen_string() == "Species S1 P1"
    assert obs3.patterns[0].MatchOnce is False
