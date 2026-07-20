import os
from bionetgen.atomizer.atomizer.analyzeSBML import get_close_matches
import bionetgen.atomizer.atomizer.analyzeSBML as analyzeSBML
import pytest
from unittest.mock import patch


def test_get_close_matches_basic():
    """Test basic fuzzy matching functionality."""
    dataset = ["apple", "ape", "application", "banana"]
    matches = get_close_matches("appel", dataset)
    assert "apple" in matches


def test_get_close_matches_cutoff():
    """Test that cutoff parameter works correctly."""
    dataset = ["apple", "ape", "application", "banana"]
    # With low cutoff, both should match
    matches = get_close_matches("app", dataset, cutoff=0.3)
    assert "apple" in matches
    assert "ape" in matches

    # With high cutoff, fewer or no matches should be returned
    matches_strict = get_close_matches("app", dataset, cutoff=0.8)
    assert "ape" not in matches_strict


def test_get_close_matches_no_match():
    """Test behavior when no matches are close enough."""
    dataset = ["apple", "ape", "application", "banana"]
    matches = get_close_matches("xyz", dataset)
    assert matches == []


def test_get_close_matches_empty_dataset():
    """Test behavior with an empty dataset."""
    matches = get_close_matches("apple", [])
    assert matches == []


def test_get_close_matches_exact_match():
    """Test that an exact match is returned."""
    dataset = ["apple", "banana", "orange"]
    matches = get_close_matches("banana", dataset)
    assert matches[0] == "banana"


@patch("difflib.get_close_matches")
def test_get_close_matches_caching(mock_difflib):
    """Test that the @memoize decorator works as expected."""
    mock_difflib.return_value = ["apple"]
    dataset = ["apple", "banana"]
    # Clear cache before test if possible, or just use a unique input
    unique_str = "appl_unique_test_123"

    # The first call should hit difflib
    matches1 = get_close_matches(unique_str, dataset)

    # The second call should return the cached result
    matches2 = get_close_matches(unique_str, dataset)

    assert matches1 == matches2 == ["apple"]
    # verify difflib was only called once
    mock_difflib.assert_called_once()


import json
import tempfile


def test_loadConfigFiles_dictionaries():
    """Test loading config files where binding_interactions use dictionaries."""
    analyzer = analyzeSBML.SBMLAnalyzer(None, "dummy.xml", "")

    config = {
        "binding_interactions": [
            [
                {"name": "MoleculeA", "site": "site_b"},
                {"name": "MoleculeB", "site": "site_a"},
            ],
            [
                {"name": "MoleculeC", "site": "site_c", "state": ["s", "0"]},
                {"name": "MoleculeD"},
            ],
            ["MoleculeE", {"name": "MoleculeF", "site": "site_f", "state": ["s", "1"]}],
            [{"name": "MoleculeG", "site": "g1"}, {"name": "MoleculeG", "site": "g2"}],
        ]
    }

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(config, f)
        temp_name = f.name

    try:
        res = analyzer.loadConfigFiles(temp_name)

        complexes = res.get("complexDefinition", [])

        def get_complex(name):
            for c in complexes:
                if c[0] == name:
                    return c[1][0]
            return None

        a_sites = get_complex("MoleculeA")
        assert a_sites == ["MoleculeA", "site_b", []], a_sites

        b_sites = get_complex("MoleculeB")
        assert b_sites == ["MoleculeB", "site_a", []], b_sites

        c_sites = get_complex("MoleculeC")
        assert c_sites == ["MoleculeC", "site_c", ["s", "0"]], c_sites

        d_sites = get_complex("MoleculeD")
        assert d_sites == ["MoleculeD", "moleculec", []], d_sites

        e_sites = get_complex("MoleculeE")
        assert e_sites == ["MoleculeE", "moleculef", []], e_sites

        f_sites = get_complex("MoleculeF")
        assert f_sites == ["MoleculeF", "site_f", ["s", "1"]], f_sites

        g_sites = get_complex("MoleculeG")
        assert g_sites == ["MoleculeG", "g1", [], "g2", []], g_sites

    finally:
        os.remove(temp_name)
