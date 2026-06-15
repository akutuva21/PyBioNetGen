from bionetgen.modelapi.structs import Action
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


def test_action_print_line():
    action = Action(action_type="simulate", action_args={"method": "ode", "t_end": 10})
    # Basic print_line without comment or label
    assert action.print_line() == "simulate({method=>ode,t_end=>10})"

    # Print with line label
    action.line_label = 1
    assert action.print_line() == "1 simulate({method=>ode,t_end=>10})"

    # Print with comment
    action.comment = "test comment"
    assert action.print_line() == "1 simulate({method=>ode,t_end=>10}) #test comment"

    # Print with comment but no label
    action._line_label = None
    assert action.print_line() == "simulate({method=>ode,t_end=>10}) #test comment"
