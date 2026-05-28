import pytest
import sys
from unittest.mock import mock_open, patch, MagicMock
import networkx as nx

# This test file ensures testing of bionetgen/atomizer/contactMap.py


@pytest.fixture(scope="module")
def contactMap_module():
    """
    Safely imports bionetgen.atomizer.contactMap by mocking legacy dependencies
    during import. Returns the imported module.
    """
    with patch.dict(
        "sys.modules",
        {
            "utils": MagicMock(),
            "utils.consoleCommands": MagicMock(),
            "cPickle": MagicMock(),
        },
    ):
        import bionetgen.atomizer.contactMap as cm

        yield cm


def test_simpleGraph(contactMap_module):
    graph = nx.Graph()

    comp1 = MagicMock()
    comp1.name = "comp1"

    comp2 = MagicMock()
    comp2.name = "comp2"

    species1 = MagicMock()
    species1.name = "spec1"
    species1.idx = 1
    species1.components = [comp1, comp2]

    species2 = MagicMock()
    species2.name = "spec2"
    species2.idx = 2
    species2.components = []

    species = [species1, species2]

    observableList = [["spec1(comp1)", "spec2(something)"]]

    nodeDict = contactMap_module.simpleGraph(
        graph, species, observableList, prefix="test", superNode={}
    )

    assert nodeDict == {1: "test_spec1", 2: "test_spec2"}

    # check nodes
    assert "test_spec1" in graph.nodes
    assert "test_spec1(comp1)" in graph.nodes
    assert "test_spec1(comp2)" in graph.nodes
    assert "test_spec2" in graph.nodes
    assert "test_spec2(something)" in graph.nodes

    # check edges
    assert ("test_spec1", "test_spec1(comp1)") in graph.edges
    assert ("test_spec1", "test_spec1(comp2)") in graph.edges
    assert ("test_spec1(comp1)", "test_spec2(something)") in graph.edges


def test_simpleGraph_superNode(contactMap_module):
    graph = nx.Graph()

    comp1 = MagicMock()
    comp1.name = "comp1"

    species1 = MagicMock()
    species1.name = "spec1"
    species1.idx = 1
    species1.components = [comp1]

    species = [species1]

    # an observable edge that also uses superNode
    observableList = [["spec1(comp1)", "spec1(comp1)"]]

    superNode = {"test_spec1": "super1", "super1": 5}

    nodeDict = contactMap_module.simpleGraph(
        graph, species, observableList, prefix="test", superNode=superNode
    )

    assert nodeDict == {1: "super1"}
    assert "super1" in graph.nodes
    assert "super1(comp1)" in graph.nodes
    assert ("super1", "super1(comp1)") in graph.edges
    assert ("super1(comp1)", "super1(comp1)") in graph.edges

    assert graph.nodes["super1"]["size"] == 5


@patch("bionetgen.atomizer.contactMap.listdir")
@patch("bionetgen.atomizer.contactMap.pickle.load")
@patch("builtins.open", new_callable=mock_open)
@patch("bionetgen.atomizer.contactMap.nx.write_gml")
@patch("bionetgen.atomizer.contactMap.readBNGXML.parseXML")
@patch("bionetgen.atomizer.contactMap.console.bngl2xml")
def test_main(
    mock_bngl2xml,
    mock_parseXML,
    mock_write_gml,
    mock_file,
    mock_pickle_load,
    mock_listdir,
    contactMap_module,
):
    # To fix `x.split(".")[0][6:]`, we need the file name to have at least 6 chars before '.'
    # For example: `prefix123.bngl.dict` -> split(".")[0] is `prefix123` -> [6:] is `123`
    mock_listdir.return_value = ["prefix123.bngl.dict"]

    # linkArray
    linkArray = [[1, 2]]
    # annotations (empty list to avoid complex annotation dict structures)
    annotations = []
    # speciesEquivalence
    speciesEquivalence = {"spec1": "spec2"}

    mock_pickle_load.side_effect = [linkArray, annotations, speciesEquivalence]

    mock_parseXML.return_value = ([], [], {}, [])

    contactMap_module.main()

    assert mock_listdir.called
    assert mock_pickle_load.call_count == 3
    assert mock_file.call_count == 3

    assert mock_bngl2xml.called
    assert mock_parseXML.called
    assert mock_write_gml.called


@patch("bionetgen.atomizer.contactMap.readBNGXML.parseXML")
@patch("bionetgen.atomizer.contactMap.nx.write_gml")
def test_main2(mock_write_gml, mock_parseXML, contactMap_module):
    mock_parseXML.return_value = ([], [], {}, [])

    contactMap_module.main2()

    assert mock_parseXML.called
    assert mock_write_gml.called
