import pytest
from bionetgen.modelapi.structs import ModelObj, Action


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


def test_action_print_line():
    action = Action("simulate", {"method": "ode", "t_end": 100, "n_steps": 100})
    # Test base print_line
    assert action.print_line() == "simulate({method=>ode,t_end=>100,n_steps=>100})"

    # Test with line_label
    action.line_label = 1
    assert action.print_line() == "1 simulate({method=>ode,t_end=>100,n_steps=>100})"

    # Test with comment
    action = Action("simulate", {"method": "ode", "t_end": 100, "n_steps": 100})
    action.comment = "This is a comment"
    assert (
        action.print_line()
        == "simulate({method=>ode,t_end=>100,n_steps=>100}) #This is a comment"
    )

    # Test with line_label and comment
    action.line_label = 1
    assert (
        action.print_line()
        == "1 simulate({method=>ode,t_end=>100,n_steps=>100}) #This is a comment"
    )
