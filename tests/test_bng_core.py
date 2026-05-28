import os, glob
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
    argv = [
        "plot",
        "-i",
        os.path.join(*[tfold, "test", "test.gdat"]),
        "-o",
        os.path.join(*[tfold, "test", "test.png"]),
    ]
    with BioNetGenTest(argv=argv) as app:
        app.run()
        assert app.exit_code == 0
        assert os.path.isfile(os.path.join(*[tfold, "test", "test.png"]))


def test_bionetgen_info():
    # tests info subcommand
    argv = ["info"]
    with BioNetGenTest(argv=argv) as app:
        app.run()
        assert app.exit_code == 0


def test_plotDAT_valid_input(mocker):
    from unittest.mock import MagicMock
    from bionetgen.core.main import plotDAT

    app_mock = MagicMock()
    app_mock.pargs.input = "test.gdat"
    app_mock.pargs.output = "test_out.png"
    app_mock.pargs._get_kwargs.return_value = {"kwarg1": "val1"}.items()

    MockBNGPlotter = mocker.patch("bionetgen.core.tools.BNGPlotter")

    plotDAT(app_mock)

    MockBNGPlotter.assert_called_once_with(
        "test.gdat", "test_out.png", app=app_mock, kwarg1="val1"
    )
    MockBNGPlotter.return_value.plot.assert_called_once()
    app_mock.log.debug.assert_called()


def test_plotDAT_invalid_input(mocker):
    from unittest.mock import MagicMock
    from bionetgen.core.main import plotDAT
    from bionetgen.core.exc import BNGFileError
    import pytest

    app_mock = MagicMock()
    app_mock.pargs.input = "test.txt"

    with pytest.raises(BNGFileError):
        plotDAT(app_mock)

    app_mock.log.error.assert_called_once()


def test_plotDAT_current_folder(mocker):
    from unittest.mock import MagicMock
    from bionetgen.core.main import plotDAT
    import os

    app_mock = MagicMock()
    app_mock.pargs.input = "/path/to/test.cdat"
    app_mock.pargs.output = "."
    app_mock.pargs._get_kwargs.return_value = {}.items()

    MockBNGPlotter = mocker.patch("bionetgen.core.tools.BNGPlotter")

    plotDAT(app_mock)

    expected_out = os.path.join("/path/to", "test.png")
    MockBNGPlotter.assert_called_once_with(
        "/path/to/test.cdat", expected_out, app=app_mock
    )
    MockBNGPlotter.return_value.plot.assert_called_once()
