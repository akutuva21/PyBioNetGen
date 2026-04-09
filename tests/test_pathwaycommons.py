import pytest
from unittest.mock import patch, MagicMock
import urllib.error
import sys
import os
import importlib.util

class DummyUtil:
    @staticmethod
    def logMess(*args, **kwargs):
        pass

# We use a pytest fixture to safely inject mock modules into sys.modules
# only for the duration of this test module.
@pytest.fixture(scope="module", autouse=True)
def mock_dependencies():
    with patch.dict('sys.modules', {"bionetgen.atomizer.utils.util": DummyUtil()}):
        spec = importlib.util.spec_from_file_location(
            "bionetgen.atomizer.utils.pathwaycommons",
            os.path.abspath("bionetgen/atomizer/utils/pathwaycommons.py")
        )
        pathwaycommons = importlib.util.module_from_spec(spec)

        with patch.dict('sys.modules', {"bionetgen.atomizer.utils.pathwaycommons": pathwaycommons}):
            spec.loader.exec_module(pathwaycommons)

            # Make it accessible to the module via a global or by yielding it
            yield pathwaycommons


# Because of memoization, we need to bypass it or clear cache between tests.
@pytest.fixture(autouse=True)
def clear_memoize_cache(mock_dependencies):
    if hasattr(mock_dependencies.name2uniprot, "cache"):
        mock_dependencies.name2uniprot.cache.clear()
    yield

def test_name2uniprot_with_organism(mock_dependencies):
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = "Entry name\tEntry\nEGFR_HUMAN\tP00533\nOther_HUMAN\tQ12345"
        mock_urlopen.return_value = mock_response

        # Call with organism
        result = mock_dependencies.name2uniprot("EGFR", organism=["NCBI:9606"])

        assert result == ["P00533"]

        mock_urlopen.assert_called_once()
        args, kwargs = mock_urlopen.call_args
        assert "organism%3ANCBI%3A9606" in kwargs["data"].decode("utf-8")

def test_name2uniprot_without_organism(mock_dependencies):
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = "Entry name\tEntry\nEGFR_MOUSE\tQ01279\n"
        mock_urlopen.return_value = mock_response

        # Call without organism
        result = mock_dependencies.name2uniprot("EGFR", organism=None)

        assert result == ["Q01279"]

        mock_urlopen.assert_called_once()
        args, kwargs = mock_urlopen.call_args
        assert "organism:" not in kwargs["data"].decode("utf-8")

def test_name2uniprot_fallback(mock_dependencies):
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response_empty = MagicMock()
        mock_response_empty.read.return_value = ""

        mock_response_valid = MagicMock()
        mock_response_valid.read.return_value = "Entry name\tEntry\nEGFR_RAT\tO00111\n"

        mock_urlopen.side_effect = [mock_response_empty, mock_response_valid]

        result = mock_dependencies.name2uniprot("EGFR", organism=["NCBI:9606"])

        assert result == ["O00111"]
        assert mock_urlopen.call_count == 2

        args1, kwargs1 = mock_urlopen.call_args_list[0]
        assert "organism%3ANCBI%3A9606" in kwargs1["data"].decode("utf-8")

        args2, kwargs2 = mock_urlopen.call_args_list[1]
        assert "organism:" not in kwargs2["data"].decode("utf-8")

def test_name2uniprot_http_error_first_call(mock_dependencies):
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://www.uniprot.org/uniprot/?",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None
        )

        with patch.object(mock_dependencies, 'logMess') as mock_log:
            result = mock_dependencies.name2uniprot("EGFR", organism=["NCBI:9606"])

            assert result is None
            mock_log.assert_called_once_with("ERROR:MSC03", "A connection could not be established to uniprot")

def test_name2uniprot_http_error_second_call(mock_dependencies):
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response_empty = MagicMock()
        mock_response_empty.read.return_value = ""

        mock_urlopen.side_effect = [
            mock_response_empty,
            urllib.error.HTTPError(
                url="http://www.uniprot.org/uniprot/?",
                code=500,
                msg="Internal Server Error",
                hdrs={},
                fp=None
            )
        ]

        result = mock_dependencies.name2uniprot("EGFR", organism=["NCBI:9606"])

        assert result is None
