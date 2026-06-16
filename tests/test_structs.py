from bionetgen.modelapi.structs import Action
import pytest
from bionetgen.modelapi.structs import ModelObj, Rule
from bionetgen.core.exc import BNGParseError


from bionetgen.modelapi.structs import ModelObj, EnergyPattern


from bionetgen.modelapi.structs import ModelObj, Rule
from bionetgen.modelapi.pattern import Pattern, Molecule
from bionetgen.modelapi.rulemod import RuleMod


from bionetgen.modelapi.structs import ModelObj, Function


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


def test_energypattern_gen_string():
    ep = EnergyPattern(name="ep1", pattern="A()", expression="k1")
    assert ep.gen_string() == "A() k1"


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


from bionetgen.modelapi.structs import Parameter


def test_parameter_gen_string():
    param = Parameter("k1", "0.1")
    assert param.gen_string() == "k1 0.1"

    param2 = Parameter("V_max", "100.5")
    assert param2.gen_string() == "V_max 100.5"


def test_rule_gen_string():
    mol_a = Molecule(name="A")
    mol_b = Molecule(name="B")
    mol_c = Molecule(name="C")

    pat_a = Pattern(molecules=[mol_a])
    pat_b = Pattern(molecules=[mol_b])
    pat_c = Pattern(molecules=[mol_c])

    # Test 1: Bidirectional rule with modifier
    rule_bi = Rule(
        name="R1",
        reactants=[pat_a],
        products=[pat_b],
        rate_constants=("k1", "k2"),
        rule_mod=RuleMod(mod_type="DeleteMolecules"),
    )
    assert rule_bi.gen_string() == "R1: A() <-> B() k1,k2 DeleteMolecules"

    # Test 2: Unidirectional rule with no explicit modifier
    rule_uni = Rule(
        name="R2",
        reactants=[pat_a],
        products=[pat_b],
        rate_constants=("k1",),
    )
    assert rule_uni.gen_string() == "R2: A() -> B() k1 "

    # Test 3: Multiple reactants and products
    rule_multi = Rule(
        name="R3",
        reactants=[pat_a, pat_b],
        products=[pat_c],
        rate_constants=("k1",),
        rule_mod=None,
    )
    assert rule_multi.gen_string() == "R3: A() + B() -> C() k1 "


def test_molecule_type_gen_string():
    from bionetgen.modelapi.structs import MoleculeType
    from bionetgen.modelapi.pattern import Component

    comp = Component()
    comp.name = "site"
    comp.states = ["state1", "state2"]
    mol_type = MoleculeType("A", [comp])

    assert mol_type.gen_string() == "A(site~state1~state2)"


def test_function_gen_string():
    f1 = Function(name="f1", expr="2 * x")
    assert f1.gen_string() == "f1 = 2 * x"

    f2 = Function(name="f2", expr="2 * x", args=["x"])
    assert f2.gen_string() == "f2(x) = 2 * x"

    f3 = Function(name="f3", expr="x * y", args=["x", "y"])
    assert f3.gen_string() == "f3(x,y) = x * y"


def test_species_gen_string():
    from bionetgen.modelapi.structs import Species

    # Create a species with a simple string pattern and count
    species = Species(pattern="A()", count=100)
    assert species.gen_string() == "A() 100"

    # Test default instantiation
    default_species = Species()
    assert default_species.gen_string() == " 0"


def test_modelobj_comment_setter():
    obj = ModelObj()

    # Test string with hashtag
    obj.comment = "   # some comment "
    assert obj.comment == " some comment "

    obj.comment = "#another comment"
    assert obj.comment == "another comment"

    # Test string without hashtag
    obj.comment = "just a string"
    assert obj.comment == "just a string"

    # Test non-string
    obj.comment = 123
    assert obj.comment == 123

    # Test list
    obj.comment = ["comment"]
    assert obj.comment == ["comment"]


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
