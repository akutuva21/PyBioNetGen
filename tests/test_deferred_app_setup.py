import subprocess
import sys
import textwrap
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_library_imports_do_not_setup_default_app():
    script = textwrap.dedent("""
        import importlib
        from unittest.mock import patch

        modules = [
            "bionetgen.modelapi.bngfile",
            "bionetgen.modelapi.bngparser",
            "bionetgen.modelapi.model",
            "bionetgen.network.network",
            "bionetgen.network.networkparser",
            "bionetgen.simulator.csimulator",
        ]

        with patch("cement.core.foundation.App.setup") as setup:
            for module in modules:
                importlib.import_module(module)

        if setup.called:
            raise SystemExit(f"App.setup() called during import: {setup.call_args!r}")
        """)
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_bngfile_resolves_default_bngpath_lazily():
    from bionetgen.modelapi import bngfile as bngfile_module

    with patch.object(
        bngfile_module, "get_default_bng_path", return_value="/default/bng"
    ) as mock_default, patch.object(
        bngfile_module,
        "find_BNG_path",
        return_value=("/resolved/bng", "/resolved/bng/BNG2.pl"),
    ) as mock_find:
        bngfile_module.BNGFile("/some/model.bngl")

    mock_default.assert_called_once_with()
    mock_find.assert_called_once_with("/default/bng")


def test_bngfile_explicit_bngpath_skips_default_lookup():
    from bionetgen.modelapi import bngfile as bngfile_module

    with patch.object(
        bngfile_module, "get_default_bng_path"
    ) as mock_default, patch.object(
        bngfile_module,
        "find_BNG_path",
        return_value=("/custom/bng", "/custom/bng/BNG2.pl"),
    ) as mock_find:
        bngfile_module.BNGFile("/some/model.bngl", BNGPATH="/custom/bng")

    mock_default.assert_not_called()
    mock_find.assert_called_once_with("/custom/bng")
