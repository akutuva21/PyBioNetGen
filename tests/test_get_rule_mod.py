import pytest
from bionetgen.modelapi.xmlparsers import RuleBlockXML


def test_get_rule_mod():
    parser = RuleBlockXML([])

    xml_totalrate = {
        "@name": "test_rule",
        "ListOfOperations": {},
        "RateLaw": {
            "@type": "Function",
            "@totalrate": 1,
            "@id": "rule1",
            "@name": "rate1",
        },
    }
    mod = parser.get_rule_mod(xml_totalrate)
    assert mod.type == "TotalRate"
    assert mod.call == 1

    xml_delete = {
        "@name": "test_rule",
        "ListOfOperations": {
            "Delete": [{"@DeleteMolecules": "1"}, {"@DeleteMolecules": "1"}]
        },
    }
    mod2 = parser.get_rule_mod(xml_delete)
    assert mod2.type == "DeleteMolecules"

    xml_delete_missing = {"@name": "test_rule", "ListOfOperations": {"Delete": [{}]}}
    mod3 = parser.get_rule_mod(xml_delete_missing)
    assert mod3.type is None

    xml_move = {
        "@name": "test_rule",
        "ListOfOperations": {
            "ChangeCompartment": [
                {
                    "@moveConnected": "1",
                    "@id": "m1",
                    "@source": "s1",
                    "@destination": "d1",
                    "@flipOrientation": "0",
                },
                {
                    "@moveConnected": "1",
                    "@id": "m2",
                    "@source": "s2",
                    "@destination": "d2",
                    "@flipOrientation": "1",
                },
            ]
        },
    }
    mod4 = parser.get_rule_mod(xml_move)
    assert mod4.type == "MoveConnected"
    assert mod4.id == ["m1", "m2"]
    assert mod4.source == ["s1", "s2"]
