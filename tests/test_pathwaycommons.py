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


def test_queryActiveSite_success_with_organism():
    from bionetgen.atomizer.utils.pathwaycommons import queryActiveSite

    with patch("urllib.request.urlopen") as mock_urlopen:
        queryActiveSite.cache.clear()
        mock_response = MagicMock()
        mock_response.read.return_value = (
            b"Name\tID\tFeature\nMYNAME_1\tID1\tACT_SITE\nNOT_MATCHING\tID2\tACT_SITE"
        )
        mock_urlopen.return_value.__enter__.return_value = mock_response

        res = queryActiveSite("myname", ["tax/9606"])
        assert res == ["MYNAME_1"]


def test_queryActiveSite_success_no_organism():
    from bionetgen.atomizer.utils.pathwaycommons import queryActiveSite

    with patch("urllib.request.urlopen") as mock_urlopen:
        queryActiveSite.cache.clear()
        mock_response = MagicMock()
        mock_response.read.return_value = (
            b"Name\tID\tFeature\nMYNAME_1\tID1\tACT_SITE\nNOT_MATCHING\tID2\tACT_SITE"
        )
        mock_urlopen.return_value.__enter__.return_value = mock_response

        res = queryActiveSite("myname", None)
        assert res == ["MYNAME_1"]


def test_queryActiveSite_httperror():
    from bionetgen.atomizer.utils.pathwaycommons import queryActiveSite

    with patch("urllib.request.urlopen") as mock_urlopen, patch(
        "bionetgen.atomizer.utils.pathwaycommons.logMess"
    ) as mock_logMess:
        queryActiveSite.cache.clear()
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://test.com",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None,
        )

        res = queryActiveSite("myname", ["tax/9606"])
        assert res == []
        mock_logMess.assert_any_call(
            "ERROR:MSC03", "A connection could not be established to uniprot"
        )


def test_queryActiveSite_no_match():
    from bionetgen.atomizer.utils.pathwaycommons import queryActiveSite

    with patch("urllib.request.urlopen") as mock_urlopen:
        queryActiveSite.cache.clear()
        mock_response = MagicMock()
        mock_response.read.return_value = b"Name\tID\tFeature\nNOT_MATCHING_1\tID1\tACT_SITE\nNOT_MATCHING_2\tID2\tACT_SITE"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        res = queryActiveSite("myname", ["tax/9606"])
        assert res == []
