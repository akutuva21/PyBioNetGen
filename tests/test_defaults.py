from unittest.mock import patch, mock_open
from bionetgen.core.defaults import get_latest_bng_version


def test_get_latest_bng_version_exists():
    with patch("os.path.isfile", return_value=True):
        with patch("builtins.open", mock_open(read_data="2.9.3")):
            version = get_latest_bng_version()
            assert version == "2.9.3"


def test_get_latest_bng_version_not_exists():
    with patch("os.path.isfile", return_value=False):
        version = get_latest_bng_version()
        assert version == "UNKNOWN"
