import importlib.metadata
import pytest
from unittest.mock import patch


def test_init_version_fallback():
    import bionetgen

    with patch("importlib.metadata.version") as mock_version:
        mock_version.side_effect = importlib.metadata.PackageNotFoundError
        with patch("bionetgen.core.version.get_version") as mock_get_version:
            mock_get_version.return_value = "1.2.3-fallback"

            result = bionetgen.__getattr__("__version__")

            assert result == "1.2.3-fallback"
            mock_version.assert_called_once_with("bionetgen")
            mock_get_version.assert_called_once()
