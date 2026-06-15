import pytest
from bionetgen.modelapi.structs import ModelObj, Rule
from bionetgen.modelapi.pattern import Pattern, Molecule
from bionetgen.modelapi.rulemod import RuleMod


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
