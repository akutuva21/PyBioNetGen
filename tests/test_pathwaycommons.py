import urllib.error
from unittest.mock import patch, MagicMock
from bionetgen.atomizer.utils.pathwaycommons import (
    queryBioGridByName,
    getReactomeBondByName,
)


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


from bionetgen.atomizer.utils.pathwaycommons import name2uniprot


def test_name2uniprot_with_organism_success():
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = "Entry name\tEntry\nEGFR_HUMAN\tP00533\n"
        mock_urlopen.return_value = mock_response

        name2uniprot.cache.clear()
        result = name2uniprot("EGFR", ["tax/9606"])
        assert result == ["P00533"]


def test_name2uniprot_with_organism_http_error():
    with patch("urllib.request.urlopen") as mock_urlopen, patch(
        "bionetgen.atomizer.utils.pathwaycommons.logMess"
    ) as mock_logMess:
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://test.com", code=500, msg="Error", hdrs={}, fp=None
        )

        name2uniprot.cache.clear()
        result = name2uniprot("EGFR", ["tax/9606"])
        mock_logMess.assert_any_call(
            "ERROR:MSC03", "A connection could not be established to uniprot"
        )
        assert result is None


def test_name2uniprot_fallback_success():
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        # Fallback uses the second URL open, we can mock it with a list of responses
        mock_response.read.side_effect = ["", "Entry name\tEntry\nEGFR_HUMAN\tP00533\n"]
        mock_urlopen.return_value = mock_response

        name2uniprot.cache.clear()
        result = name2uniprot("EGFR", ["tax/9606"])
        assert result == ["P00533"]


def test_name2uniprot_fallback_http_error():
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = ""

        def side_effect(*args, **kwargs):
            if mock_urlopen.call_count == 1:
                return mock_response
            raise urllib.error.HTTPError(
                url="http://test.com", code=500, msg="Error", hdrs={}, fp=None
            )

        mock_urlopen.side_effect = side_effect

        name2uniprot.cache.clear()
        result = name2uniprot("EGFR", ["tax/9606"])
        assert result is None


def test_name2uniprot_no_organism():
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = "Entry name\tEntry\nEGFR_HUMAN\tP00533\n"
        mock_urlopen.return_value = mock_response

        name2uniprot.cache.clear()
        # Provide empty organism list, should skip to fallback
        result = name2uniprot("EGFR", [])
        assert result == ["P00533"]
