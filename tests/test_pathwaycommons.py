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


from bionetgen.atomizer.utils.pathwaycommons import isInComplexWith


def test_isInComplexWith_success():
    with patch(
        "bionetgen.atomizer.utils.pathwaycommons.getReactomeBondByName"
    ) as mock_getReactomeBondByName:
        mock_getReactomeBondByName.return_value = [("A", "in-complex-with", "B")]
        name1 = ("GENE1", "uri1")
        name2 = ("GENE2", "uri2")
        result = isInComplexWith(name1, name2, organism=None)
        assert result is True
        mock_getReactomeBondByName.assert_called_once_with(
            "GENE1", "GENE2", "uri1", "uri2", None
        )


def test_isInComplexWith_failure():
    with patch(
        "bionetgen.atomizer.utils.pathwaycommons.getReactomeBondByName"
    ) as mock_getReactomeBondByName:
        mock_getReactomeBondByName.return_value = [("A", "interacts-with", "B")]
        name1 = ("GENE1", "uri1")
        name2 = ("GENE2", "uri2")
        result = isInComplexWith(name1, name2, organism=None)
        assert result is False
        mock_getReactomeBondByName.assert_called_once_with(
            "GENE1", "GENE2", "uri1", "uri2", None
        )


def test_isInComplexWith_retry_success():
    with patch(
        "bionetgen.atomizer.utils.pathwaycommons.getReactomeBondByName"
    ) as mock_getReactomeBondByName:
        mock_getReactomeBondByName.side_effect = [
            None,
            None,
            [("A", "in-complex-with", "B")],
        ]
        name1 = ("GENE1", "uri1")
        name2 = ("GENE2", "uri2")
        result = isInComplexWith(name1, name2, organism=None)
        assert result is True
        assert mock_getReactomeBondByName.call_count == 3
