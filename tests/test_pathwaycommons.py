import urllib.error
from unittest.mock import patch, MagicMock
from bionetgen.atomizer.utils.pathwaycommons import queryBioGridByName


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


from bionetgen.atomizer.utils.pathwaycommons import getReactomeBondByUniprot


def test_getReactomeBondByUniprot_success():
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = """protein1\tin-complex-with\tprotein2
protein3\tinteracts-with\tprotein4

protein1\txref\tuniprot1
protein2\txref\tuniprot2
protein3\txref\tuniprot3
protein4\txref\tuniprot4"""
        mock_urlopen.return_value = mock_response

        uniprot1 = ["uniprot1"]
        uniprot2 = ["uniprot2"]

        getReactomeBondByUniprot.cache = {}
        result = getReactomeBondByUniprot(uniprot1, uniprot2)

        assert result == [["protein1", "in-complex-with", "protein2"]]


def test_getReactomeBondByUniprot_httperror():
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://test.com",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None,
        )

        uniprot1 = ["uniprot_err1"]
        uniprot2 = ["uniprot_err2"]

        getReactomeBondByUniprot.cache = {}
        result = getReactomeBondByUniprot(uniprot1, uniprot2)

        assert result is None
