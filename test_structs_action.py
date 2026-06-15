from bionetgen.modelapi.structs import Action
import pytest

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
    action._line_label = None # Bypass setter issue for a moment
    assert action.print_line() == "simulate({method=>ode,t_end=>10}) #test comment"
