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


def test_modelobj_comment():
    obj = ModelObj()

    # Test setting a string with #
    obj.comment = "# this is a comment"
    assert obj.comment == " this is a comment"

    # Test setting a string with leading whitespace and #
    obj.comment = "   # this is another comment"
    assert obj.comment == " this is another comment"

    # Test setting a string without #
    obj.comment = "no hash comment"
    assert obj.comment == "no hash comment"

    # Test setting a non-string value
    obj.comment = 12345
    assert obj.comment == 12345
