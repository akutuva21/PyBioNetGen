import pytest
from unittest.mock import patch
from bionetgen.modelapi.sympy_odes import _safe_rmtree


def test_safe_rmtree_exception():
    with patch("shutil.rmtree") as mock_rmtree:
        mock_rmtree.side_effect = Exception("Mock exception")
        # Should not raise an exception
        try:
            _safe_rmtree("dummy_path")
        except Exception as e:
            pytest.fail(f"_safe_rmtree raised an exception unexpectedly: {e}")


def test_export_sympy_odes_exception():
    from bionetgen.modelapi.sympy_odes import export_sympy_odes
    from bionetgen.core.exc import BNGError
    from bionetgen.modelapi.model import bngmodel
    from unittest.mock import patch, MagicMock

    with patch(
        "bionetgen.modelapi.sympy_odes.extract_odes_from_mexfile"
    ) as mock_extract:
        mock_extract.side_effect = Exception("Mock exception")
        with pytest.raises(
            BNGError, match="Failed to extract ODEs from mex C file: dummy_path"
        ):
            mock_model = MagicMock(spec=bngmodel)
            with patch(
                "bionetgen.modelapi.sympy_odes._find_mex_c_file",
                return_value="dummy_path",
            ):
                with patch("bionetgen.modelapi.runner.run"):
                    export_sympy_odes(mock_model)
