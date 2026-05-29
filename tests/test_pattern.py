import pytest
from bionetgen.modelapi.pattern import Pattern, Molecule


def test_pattern_eq():
    mol1 = Molecule(name="A")
    mol2 = Molecule(name="B")
    mol3 = Molecule(name="C")

    # Baseline match
    pat1 = Pattern(molecules=[mol1, mol2])
    pat2 = Pattern(molecules=[mol1, mol2])
    assert pat1 == pat2

    # Non-Pattern object
    assert pat1 != "not a pattern"

    # Difference in compartment
    pat_diff_comp = Pattern(molecules=[mol1, mol2], compartment="cell")
    assert pat1 != pat_diff_comp

    # Difference in label
    pat_diff_label = Pattern(molecules=[mol1, mol2], label="l1")
    assert pat1 != pat_diff_label

    # Difference in fixed
    pat_diff_fixed = Pattern(molecules=[mol1, mol2])
    pat_diff_fixed.fixed = True
    assert pat1 != pat_diff_fixed

    # Difference in MatchOnce
    pat_diff_matchonce = Pattern(molecules=[mol1, mol2])
    pat_diff_matchonce.MatchOnce = True
    assert pat1 != pat_diff_matchonce

    # Difference in relation
    pat_diff_relation = Pattern(molecules=[mol1, mol2])
    pat_diff_relation.relation = "=="
    assert pat1 != pat_diff_relation

    # Difference in quantity
    pat_diff_quantity = Pattern(molecules=[mol1, mol2])
    pat_diff_quantity.quantity = "5"
    assert pat1 != pat_diff_quantity

    # Difference in canonical_label
    pat_canon_1 = Pattern(molecules=[mol1, mol2])
    pat_canon_1.canonical_label = "canon1"
    pat_canon_2 = Pattern(molecules=[mol1, mol2])
    pat_canon_2.canonical_label = "canon2"
    assert pat_canon_1 != pat_canon_2

    # Difference in canonical_certificate
    pat_cert_1 = Pattern(molecules=[mol1, mol2])
    pat_cert_1.canonical_certificate = "cert1"
    pat_cert_2 = Pattern(molecules=[mol1, mol2])
    pat_cert_2.canonical_certificate = "cert2"
    assert pat_cert_1 != pat_cert_2

    # Difference in molecules
    pat_diff_mol = Pattern(molecules=[mol1, mol3])
    assert pat1 != pat_diff_mol
