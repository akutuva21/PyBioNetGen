import pytest
from unittest.mock import patch
from bionetgen.modelapi.sympy_odes import _safe_rmtree


from bionetgen.core.exc import BNGError
from bionetgen.modelapi.sympy_odes import export_sympy_odes

from bionetgen.modelapi.model import bngmodel
from unittest.mock import MagicMock


def test_export_sympy_odes_exception():
    with patch(
        "bionetgen.modelapi.sympy_odes.extract_odes_from_mexfile"
    ) as mock_extract:
        mock_extract.side_effect = Exception("Mock extraction failure")

        # Create a mock model to skip bngmodel instantiation and file parsing
        mock_model = MagicMock(spec=bngmodel)

        # Mock run since we don't want to actually run the simulator
        with patch("bionetgen.modelapi.runner.run"):
            # We need to mock _find_mex_c_file so it doesn't try to look up actual files
            with patch(
                "bionetgen.modelapi.sympy_odes._find_mex_c_file",
                return_value="dummy_path.c",
            ):
                with pytest.raises(
                    BNGError, match="Failed to extract ODEs from mex C file"
                ):
                    export_sympy_odes(mock_model, "dummy_mex_c_path")


def test_safe_rmtree_exception():
    with patch("shutil.rmtree") as mock_rmtree:
        mock_rmtree.side_effect = Exception("Mock exception")
        # Should not raise an exception
        try:
            _safe_rmtree("dummy_path")
        except Exception as e:
            pytest.fail(f"_safe_rmtree raised an exception unexpectedly: {e}")
