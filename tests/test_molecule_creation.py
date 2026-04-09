import pytest
from unittest.mock import MagicMock, patch

from bionetgen.atomizer.atomizer.moleculeCreation import createBindingRBM

def test_createBindingRBM_keyerror(capsys):
    mol1 = MagicMock()
    mol1.name = "UnknownMol"
    mol1.components = []

    mol2 = MagicMock()
    mol2.name = "Mol2"
    mol2.components = []

    element = ["test_element"]
    translator = {}  # Empty translator to trigger KeyError
    dependencyGraph = {"test_element": [[]]}
    database = MagicMock()
    database.partialUserLabelDictionary = {}

    with patch("bionetgen.atomizer.atomizer.moleculeCreation.getComplexationComponents2") as mock_get_complexation:
        mock_get_complexation.return_value = [(mol1, mol2)]

        with pytest.raises(KeyError) as exc_info:
            createBindingRBM(
                element,
                translator,
                dependencyGraph,
                bioGridFlag=False,
                pathwaycommonsFlag=False,
                parser=None,
                database=database
            )

    # Check if KeyError was raised
    assert exc_info.type is KeyError

    # Verify the printed output
    captured = capsys.readouterr()
    assert "The translator doesn't know the molecule: UnknownMol" in captured.out

def test_createBindingRBM_keyerror_molecule2(capsys):
    mol1 = MagicMock()
    mol1.name = "Mol1"
    mol1.components = []

    mol2 = MagicMock()
    mol2.name = "UnknownMol2"
    mol2.components = []

    element = ["test_element"]
    translator = {
        "Mol1": MagicMock()
    }
    translator["Mol1"].molecules = [MagicMock()]
    translator["Mol1"].molecules[0].components = []

    dependencyGraph = {"test_element": [[]]}
    database = MagicMock()
    database.partialUserLabelDictionary = {}

    with patch("bionetgen.atomizer.atomizer.moleculeCreation.getComplexationComponents2") as mock_get_complexation:
        mock_get_complexation.return_value = [(mol1, mol2)]

        with pytest.raises(KeyError) as exc_info:
            createBindingRBM(
                element,
                translator,
                dependencyGraph,
                bioGridFlag=False,
                pathwaycommonsFlag=False,
                parser=None,
                database=database
            )

    # Check if KeyError was raised
    assert exc_info.type is KeyError

    # Verify the printed output
    captured = capsys.readouterr()
    assert "The translator doesn't know the molecule: UnknownMol2" in captured.out
