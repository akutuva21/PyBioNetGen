import pytest
from bionetgen.modelapi.pattern import Pattern, Molecule


def test_pattern_contains():
    # 1. Create a Pattern with one Molecule
    mol1 = Molecule(name="A")
    pat = Pattern(molecules=[mol1])

    # 2. Create a matching Molecule
    mol2 = Molecule(name="A")

    # 3. Create a non-matching Molecule
    mol3 = Molecule(name="B")

    # 4. Check the `in` operation
    assert mol1 in pat
    assert mol2 in pat
    assert mol3 not in pat

    # Also test for string based checking
    assert "A" in pat
    assert "B" not in pat
