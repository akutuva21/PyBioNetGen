import pytest
from bionetgen.modelapi.structs import ModelObj, Observable
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
