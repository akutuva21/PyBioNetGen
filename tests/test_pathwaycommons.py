import urllib.error
from unittest.mock import patch, MagicMock
from bionetgen.atomizer.utils.pathwaycommons import queryBioGridByName, getReactomeBondByName


def test_queryBioGridByName_httperror_with_organism():
    with patch("urllib.request.urlopen") as mock_urlopen, patch(
        "bionetgen.atomizer.utils.pathwaycommons.logMess"
    ) as mock_logMess:

        # Setup mock to raise HTTPError
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://test.com",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None,
        )

        name1 = "GENE1"
        name2 = "GENE2"
        organism = ["tax/9606"]
        truename1 = "GENE1"
        truename2 = "GENE2"

        queryBioGridByName.cache = {}
        result = queryBioGridByName(name1, name2, organism, truename1, truename2)

        # Verify the specific error log was triggered
        mock_logMess.assert_any_call(
            "ERROR:MSC02",
            "A connection could not be established to biogrid while testing with taxon 9606 and genes GENE1|GENE2, trying without organism taxonomy limitation",
        )
        assert result is False


def test_queryBioGridByName_httperror_no_organism():
    with patch("urllib.request.urlopen") as mock_urlopen, patch(
        "bionetgen.atomizer.utils.pathwaycommons.logMess"
    ) as mock_logMess:

        # Setup mock to raise HTTPError
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://test.com",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None,
        )

        name1 = "GENE1"
        name2 = "GENE2"
        organism = None
        truename1 = "GENE1"
        truename2 = "GENE2"

        queryBioGridByName.cache = {}
        result = queryBioGridByName(name1, name2, organism, truename1, truename2)

        # Verify the specific error log was triggered
        mock_logMess.assert_any_call(
            "ERROR:MSC02", "A connection could not be established to biogrid"
        )
        assert result is False

@patch('bionetgen.atomizer.utils.pathwaycommons.getReactomeBondByUniprot')
@patch('bionetgen.atomizer.utils.pathwaycommons.name2uniprot')
def test_getReactomeBondByName_with_uris(mock_name2uniprot, mock_getReactomeBondByUniprot):
    # Clear memoization cache to prevent test interference
    getReactomeBondByName.cache = {}

    mock_getReactomeBondByUniprot.return_value = [['P01133', 'in-complex-with', 'P01112']]

    name1 = 'EGF'
    name2 = 'EGFR'
    sbmlURI = ['http://identifiers.org/uniprot/P01133']
    sbmlURI2 = ['http://identifiers.org/uniprot/P01112']
    organism = None

    result = getReactomeBondByName(name1, name2, sbmlURI, sbmlURI2, organism)

    # name2uniprot shouldn't be called since URIs are provided
    mock_name2uniprot.assert_not_called()

    mock_getReactomeBondByUniprot.assert_called_once_with(['P01133'], ['P01112'])
    assert result == [['P01133', 'in-complex-with', 'P01112']]

@patch('bionetgen.atomizer.utils.pathwaycommons.getReactomeBondByUniprot')
@patch('bionetgen.atomizer.utils.pathwaycommons.name2uniprot')
def test_getReactomeBondByName_without_uris(mock_name2uniprot, mock_getReactomeBondByUniprot):
    getReactomeBondByName.cache = {}

    # Mock return values for name2uniprot
    mock_name2uniprot.side_effect = [['P01133'], ['P01112']]
    mock_getReactomeBondByUniprot.return_value = [['P01133', 'in-complex-with', 'P01112']]

    name1 = 'EGF'
    name2 = 'EGFR'
    sbmlURI = []
    sbmlURI2 = []
    organism = ['tax/9606']

    result = getReactomeBondByName(name1, name2, sbmlURI, sbmlURI2, organism)

    # Verify name2uniprot was called
    assert mock_name2uniprot.call_count == 2
    mock_name2uniprot.assert_any_call(name1, organism)
    mock_name2uniprot.assert_any_call(name2, organism)

    mock_getReactomeBondByUniprot.assert_called_once_with(['P01133'], ['P01112'])
    assert result == [['P01133', 'in-complex-with', 'P01112']]

@patch('bionetgen.atomizer.utils.pathwaycommons.getReactomeBondByUniprot')
@patch('bionetgen.atomizer.utils.pathwaycommons.name2uniprot')
def test_getReactomeBondByName_fallback_to_names(mock_name2uniprot, mock_getReactomeBondByUniprot):
    getReactomeBondByName.cache = {}

    # Return empty list or None from name2uniprot
    mock_name2uniprot.side_effect = [[], None]
    mock_getReactomeBondByUniprot.return_value = []

    name1 = 'UnknownGene1'
    name2 = 'UnknownGene2'
    sbmlURI = []
    sbmlURI2 = []
    organism = None

    result = getReactomeBondByName(name1, name2, sbmlURI, sbmlURI2, organism)

    # Verify fallback to names
    mock_getReactomeBondByUniprot.assert_called_once_with(['UnknownGene1'], ['UnknownGene2'])
    assert result == []
