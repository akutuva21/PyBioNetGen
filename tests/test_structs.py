from bionetgen.modelapi.structs import Action
import pytest
from bionetgen.modelapi.structs import ModelObj, Compartment, Observable, Action
from bionetgen.modelapi.pattern import Pattern, Molecule


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


def test_compartment_gen_string():
    # Test without outside compartment
    c1 = Compartment(name="comp1", dim=3, size=1.0)
    assert c1.gen_string() == "comp1 3 1.0"

    # Test with outside compartment
    c2 = Compartment(name="comp2", dim=2, size=2.0, outside="comp1")
    assert c2.gen_string() == "comp2 2 2.0 comp1"


def test_observable_add_pattern():
    # Test for "Molecules" type
    obs_mol = Observable(name="obs_mol", otype="Molecules", patterns=[])
    pat_mol = Pattern(molecules=[Molecule(name="A")])
    pat_mol.MatchOnce = True  # Should remain True
    obs_mol.add_pattern(pat_mol)
    assert len(obs_mol.patterns) == 1
    assert obs_mol.patterns[0] == pat_mol
    assert obs_mol.patterns[0].MatchOnce is True

    # Test for "Species" type
    obs_spec = Observable(name="obs_spec", otype="Species", patterns=[])
    pat_spec = Pattern(molecules=[Molecule(name="B")])
    pat_spec.MatchOnce = True  # Should be set to False
    obs_spec.add_pattern(pat_spec)
    assert len(obs_spec.patterns) == 1
    assert obs_spec.patterns[0] == pat_spec
    assert obs_spec.patterns[0].MatchOnce is False


def test_action_print_line_v2():
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
    obj._line_label = None  # reset line_label
    obj.comment = "# test comment"
    assert obj.print_line() == "  dummy_object # test comment"

    # Test with both line label and comment
    obj.line_label = 1
    obj.comment = "# test comment"
    assert obj.print_line() == "  1 dummy_object # test comment"


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


def test_action_gen_string():
    from bionetgen.modelapi.structs import Action

    # Normal action with arguments
    a1 = Action("simulate", {"method": "ode", "t_end": 10})
    assert a1.gen_string() == "simulate({method=>ode,t_end=>10})"

    # Normal action with no arguments
    a2 = Action("simulate", {})
    assert a2.gen_string() == "simulate()"

    # Positional action without => setter syntax
    a3 = Action("setConcentration", {"A": None, "10": None})
    assert a3.gen_string() == "setConcentration(A,10)"

    # Positional action with square braces
    a4 = Action("saveConcentrations", {"A": None, "B": None})
    assert a4.gen_string() == "saveConcentrations([A,B])"
