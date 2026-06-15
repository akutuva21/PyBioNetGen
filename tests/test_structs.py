import pytest
from bionetgen.modelapi.structs import ModelObj, Rule
from bionetgen.core.exc import BNGParseError


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


def test_rule_set_rate_constants():
    # 1 rate constant
    r1 = Rule(name="r1", rate_constants=("k1",))
    assert r1.rate_constants == ["k1"]
    assert r1.bidirectional is False

    # 2 rate constants
    r2 = Rule(name="r2", rate_constants=("k1", "k2"))
    assert r2.rate_constants == ["k1", "k2"]
    assert r2.bidirectional is True

    # 0 rate constants should raise BNGParseError
    with pytest.raises(BNGParseError) as excinfo:
        Rule(name="r3", rate_constants=())
    assert "Rule r3 requires 1 or 2 rate constants, got 0" in str(excinfo.value)

    # >2 rate constants should raise BNGParseError
    with pytest.raises(BNGParseError) as excinfo:
        Rule(name="r4", rate_constants=("k1", "k2", "k3"))
    assert "Rule r4 requires 1 or 2 rate constants, got 3" in str(excinfo.value)

    # test calling set_rate_constants after initialization
    r5 = Rule(name="r5", rate_constants=("k1",))
    r5.set_rate_constants(("k3", "k4"))
    assert r5.rate_constants == ["k3", "k4"]
    assert r5.bidirectional is True
