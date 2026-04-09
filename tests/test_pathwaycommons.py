import pytest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError
import urllib.request
from bionetgen.atomizer.utils.pathwaycommons import name2uniprot


def test_name2uniprot_with_organism():
    """Test name2uniprot when organism is provided and response is successful."""
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = (
            b"entry name\tid\nEGF_HUMAN\tP01133\nEGF_MOUSE\tP01132\n".decode("utf-8")
        )
        mock_urlopen.return_value = mock_response

        # Use an organism that ends in '9606' to trigger organism query building
        result = name2uniprot("EGF", ["taxonomy/9606"])

        # It should parse matching symbols based on `nameStr` ignoring case.
        # Since 'EGF' is in 'EGF_HUMAN' and 'EGF_MOUSE', both should be returned.
        assert result == ["P01133", "P01132"]
        mock_urlopen.assert_called_once()


def test_name2uniprot_fallback_no_organism():
    """Test name2uniprot fallback when initial organism query returns no results."""
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response_1 = MagicMock()
        # Empty string response or missing to trigger fallback
        mock_response_1.read.return_value = b"".decode("utf-8")

        mock_response_2 = MagicMock()
        # Mocking the fallback response
        mock_response_2.read.return_value = (
            b"entry name\tid\nEGF2_HUMAN\tP01133\n".decode("utf-8")
        )

        # urlopen will return mock_response_1 then mock_response_2 on successive calls
        mock_urlopen.side_effect = [mock_response_1, mock_response_2]

        result = name2uniprot("EGF2", ["taxonomy/9606"])

        assert result == ["P01133"]
        assert mock_urlopen.call_count == 2


def test_name2uniprot_no_organism():
    """Test name2uniprot when no organism is provided."""
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = (
            b"entry name\tid\nEGF3_HUMAN\tP01133\n".decode("utf-8")
        )
        mock_urlopen.return_value = mock_response

        result = name2uniprot("EGF3", None)

        assert result == ["P01133"]
        mock_urlopen.assert_called_once()


def test_name2uniprot_http_error_with_organism():
    """Test name2uniprot handling of HTTPError when organism is provided."""
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = HTTPError(
            url="", code=500, msg="Internal Server Error", hdrs={}, fp=None
        )

        result = name2uniprot("EGF4", ["taxonomy/9606"])

        # It should catch the error, log it, and return None
        assert result is None
        mock_urlopen.assert_called_once()


def test_name2uniprot_http_error_no_organism():
    """Test name2uniprot handling of HTTPError when no organism is provided (fallback)."""
    with patch("urllib.request.urlopen") as mock_urlopen:
        # Side effect raises error for the query
        mock_urlopen.side_effect = HTTPError(
            url="", code=500, msg="Internal Server Error", hdrs={}, fp=None
        )

        result = name2uniprot("EGF5", None)

        assert result is None
        mock_urlopen.assert_called_once()
