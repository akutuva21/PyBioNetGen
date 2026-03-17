import pytest

from bionetgen.modelapi.xmlparsers import RuleBlockXML


def _rule_block_parser():
    # Create a RuleBlockXML instance without running __init__ (which expects full rule XML)
    return RuleBlockXML.__new__(RuleBlockXML)


def test_get_rule_mod_total_rate_string_true():
    xml = {
        "ListOfOperations": {},
        "RateLaw": {"@type": "Function", "@totalrate": "1", "@id": "r1", "@name": "foo"},
    }

    mod = _rule_block_parser().get_rule_mod(xml)
    assert mod.type == "TotalRate"
    assert mod.id == "r1"
    assert mod.call == "1"


def test_get_rule_mod_delete_molecules_all_operations():
    xml = {
        "ListOfOperations": {
            "Delete": [
                {"@DeleteMolecules": "1"},
                {"@DeleteMolecules": "1"},
            ]
        }
    }

    mod = _rule_block_parser().get_rule_mod(xml)
    assert mod.type == "DeleteMolecules"


def test_get_rule_mod_delete_molecules_missing_attribute_does_not_apply():
    xml = {
        "ListOfOperations": {
            "Delete": [
                {"@DeleteMolecules": "1"},
                {},
            ]
        }
    }

    mod = _rule_block_parser().get_rule_mod(xml)
    assert mod.type is None


def test_get_rule_mod_move_connected_list_uses_each_element():
    xml = {
        "ListOfOperations": {
            "ChangeCompartment": [
                {
                    "@moveConnected": "1",
                    "@id": "a",
                    "@source": "s",
                    "@destination": "d",
                    "@flipOrientation": "0",
                },
                {
                    "@moveConnected": "1",
                    "@id": "b",
                    "@source": "s2",
                    "@destination": "d2",
                    "@flipOrientation": "1",
                },
            ]
        }
    }

    mod = _rule_block_parser().get_rule_mod(xml)
    assert mod.type == "MoveConnected"
    assert mod.id == ["a", "b"]
    assert mod.source == ["s", "s2"]
    assert mod.destination == ["d", "d2"]
    assert mod.flip == ["0", "1"]
    assert mod.call == ["1", "1"]
