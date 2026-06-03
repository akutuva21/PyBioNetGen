import os, glob
from unittest.mock import patch
from pytest import raises
import bionetgen as bng
from bionetgen.main import BioNetGenTest

tfold = os.path.dirname(__file__)


def test_bionetgen_help():
    # tests basic command help
    with raises(SystemExit):
        argv = ["--help"]
        with BioNetGenTest(argv=argv) as app:
            app.run()
            assert app.exit_code == 0


def test_bionetgen_input():
    argv = [
        "run",
        "-i",
        os.path.join(tfold, "test.bngl"),
        "-o",
        os.path.join(tfold, "test"),
    ]
    to_match = ["test.xml", "test.cdat", "test.gdat", "test.net"]
    with BioNetGenTest(argv=argv) as app:
        app.run()
        assert app.exit_code == 0
        file_list = os.listdir(os.path.join(tfold, "test"))
        assert file_list.sort() == to_match.sort()


def test_bionetgen_plot():
    # first run the model to generate the data
    argv = [
        "run",
        "-i",
        os.path.join(tfold, "test.bngl"),
        "-o",
        os.path.join(tfold, "test"),
    ]
    with BioNetGenTest(argv=argv) as app:
        app.run()
        assert app.exit_code == 0

    # now plot the data
    argv = [
        "plot",
        "-i",
        os.path.join(*[tfold, "test", "test.gdat"]),
        "-o",
        os.path.join(*[tfold, "test", "test.png"]),
    ]
    if os.path.exists(os.path.join(*[tfold, "test", "test.gdat"])):
        with BioNetGenTest(argv=argv) as app:
            app.run()
            assert app.exit_code == 0
            assert os.path.isfile(os.path.join(*[tfold, "test", "test.png"]))
            # cleanup
            os.remove(os.path.join(*[tfold, "test", "test.png"]))


def test_bionetgen_info():
    # tests info subcommand
    argv = ["info"]
    with BioNetGenTest(argv=argv) as app:
        app.run()
        assert app.exit_code == 0


def test_printInfo():
    from unittest.mock import patch, MagicMock
    from bionetgen.core.main import printInfo

    app_mock = MagicMock()
    app_mock.config = {"some": "config"}

    with patch("bionetgen.core.main.BNGInfo") as MockBNGInfo:
        printInfo(app_mock)

        MockBNGInfo.assert_called_once_with(config=app_mock.config, app=app_mock)
        MockBNGInfo.return_value.gatherInfo.assert_called_once()
        MockBNGInfo.return_value.messageGeneration.assert_called_once()
        MockBNGInfo.return_value.run.assert_called_once()
        app_mock.log.debug.assert_called()


def test_plotDAT_valid_input():
    from unittest.mock import patch
    from unittest.mock import MagicMock
    from bionetgen.core.main import plotDAT

    app_mock = MagicMock()
    app_mock.pargs.input = "test.gdat"
    app_mock.pargs.output = "test_out.png"
    app_mock.pargs._get_kwargs.return_value = {"kwarg1": "val1"}.items()

    with patch("bionetgen.core.tools.BNGPlotter") as MockBNGPlotter:
        plotDAT(app_mock)

        MockBNGPlotter.assert_called_once_with(
            "test.gdat", "test_out.png", app=app_mock, kwarg1="val1"
        )
        MockBNGPlotter.return_value.plot.assert_called_once()
        app_mock.log.debug.assert_called()


def test_plotDAT_invalid_input():
    from unittest.mock import MagicMock
    from bionetgen.core.main import plotDAT
    from bionetgen.core.exc import BNGFileError
    import pytest

    app_mock = MagicMock()
    app_mock.pargs.input = "test.txt"

    with pytest.raises(BNGFileError):
        plotDAT(app_mock)

    app_mock.log.error.assert_called_once()


@patch("bionetgen.core.tools.BNGPlotter")
def test_plotDAT_current_folder(MockBNGPlotter):
    from unittest.mock import patch
    from unittest.mock import MagicMock
    import os

    app_mock = MagicMock()
    app_mock.pargs.input = "/path/to/test.cdat"
    app_mock.pargs.output = "."
    app_mock.pargs._get_kwargs.return_value = {}.items()

    with patch("bionetgen.core.tools.plot.BNGResult.load") as mock_load:
        with patch("bionetgen.core.tools.plot.BNGPlotter") as MockBNGPlotter:
            import bionetgen.core.tools

            original_plotter = bionetgen.core.tools.BNGPlotter
            bionetgen.core.tools.BNGPlotter = MockBNGPlotter
            try:
                from bionetgen.core.main import plotDAT

                plotDAT(app_mock)

                expected_out = os.path.join("/path/to", "test.png")
                MockBNGPlotter.assert_called_once_with(
                    "/path/to/test.cdat", expected_out, app=app_mock
                )
                MockBNGPlotter.return_value.plot.assert_called_once()
            finally:
                bionetgen.core.tools.BNGPlotter = original_plotter
