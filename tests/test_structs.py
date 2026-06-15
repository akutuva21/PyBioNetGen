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


def test_modelobj_print_line():
    class DummyModelObj(ModelObj):
        def gen_string(self) -> str:
            return "dummy_object"

    obj = DummyModelObj()

    # Test base case with no line label and no comment
    assert obj.print_line() == "  dummy_object"

    # Test with line label only
    obj.line_label = 1
    assert obj.print_line() == "  1 dummy_object"

    # Test with comment only
    obj._line_label = None # reset line_label
    obj.comment = "# test comment"
    assert obj.print_line() == "  dummy_object # test comment"

    # Test with both line label and comment
    obj.line_label = 1
    obj.comment = "# test comment"
    assert obj.print_line() == "  1 dummy_object # test comment"
