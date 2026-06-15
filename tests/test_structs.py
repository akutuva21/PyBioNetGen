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


from bionetgen.modelapi.structs import Parameter


def test_parameter_gen_string():
    param = Parameter("k1", "0.1")
    assert param.gen_string() == "k1 0.1"

    param2 = Parameter("V_max", "100.5")
    assert param2.gen_string() == "V_max 100.5"
