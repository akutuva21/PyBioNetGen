import pytest

from bionetgen.modelapi.xmlparsers import BondsXML


def test_resolve_xml_missing_id():
    # Arrange
    xml_obj = BondsXML()
    bonds_xml = [
        {"@id": "1", "@site1": "O1_P1_M1_C1", "@site2": "O1_P1_M2_C1"},
        {"@id": "2", "@site1": "O1_P2_M1_C1"},  # Missing @site2
    ]
    # Act & Assert
    with pytest.raises(KeyError):
        xml_obj.resolve_xml(bonds_xml)


def test_resolve_xml_not_list_missing_id():
    xml_obj = BondsXML()
    bonds_xml = {"@id": "1", "@site1": "O1_P1_M1_C1"}  # Missing @site2
    with pytest.raises(KeyError):
        xml_obj.resolve_xml(bonds_xml)
