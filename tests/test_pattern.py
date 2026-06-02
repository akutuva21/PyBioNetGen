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

import sys
import unittest.mock

def test_canonicalize_import_error():
    mol = Molecule(name="A")
    pat = Pattern(molecules=[mol])

    with unittest.mock.patch('bionetgen.modelapi.pattern.logger') as mock_logger:
        with unittest.mock.patch.dict(sys.modules, {'pynauty': None}):
            pat.canonicalize()
            mock_logger.warning.assert_called_once()
            args, kwargs = mock_logger.warning.call_args
            assert "Importing pynauty failed" in args[0]
            assert pat.canonical_label is None
