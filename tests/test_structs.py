import pytest
from bionetgen.modelapi.structs import ModelObj, Function


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

def test_function_gen_string():
    f1 = Function(name="f1", expr="2 * x")
    assert f1.gen_string() == "f1 = 2 * x"

    f2 = Function(name="f2", expr="2 * x", args=["x"])
    assert f2.gen_string() == "f2(x) = 2 * x"

    f3 = Function(name="f3", expr="x * y", args=["x", "y"])
    assert f3.gen_string() == "f3(x,y) = x * y"
