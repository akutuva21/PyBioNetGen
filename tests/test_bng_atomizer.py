import os, glob
from pytest import raises
import bionetgen as bng
from bionetgen.main import BioNetGenTest

tfold = os.path.dirname(__file__)


def test_atomize_flat():
    if not os.path.exists(os.path.join(tfold, "test")):
        os.mkdir(os.path.join(tfold, "test"))
    argv = [
        "atomize",
        "-i",
        os.path.join(tfold, "test_sbml.xml"),
        "-o",
        os.path.join(*[tfold, "test", "test_sbml_flat.bngl"]),
    ]
    to_match = ["test_sbml_flat.bngl"]
    with BioNetGenTest(argv=argv) as app:
        app.run()
        assert app.exit_code == 0
        file_list = os.listdir(os.path.join(tfold, "test"))
        assert file_list.sort() == to_match.sort()


def test_atomize_atomized():
    if not os.path.exists(os.path.join(tfold, "test")):
        os.mkdir(os.path.join(tfold, "test"))
    argv = [
        "atomize",
        "-i",
        os.path.join(tfold, "test_sbml.xml"),
        "-o",
        os.path.join(*[tfold, "test", "test_sbml_atom.bngl"]),
        "-a",
    ]
    to_match = ["test_sbml_atom.bngl"]
    with BioNetGenTest(argv=argv) as app:
        app.run()
        assert app.exit_code == 0
        file_list = os.listdir(os.path.join(tfold, "test"))
        assert file_list.sort() == to_match.sort()

def test_comb():
    from bionetgen.atomizer.sbml2json import comb

    # Happy paths
    assert comb(5, 2) == 10
    assert comb(5, 0) == 1
    assert comb(5, 5) == 1
    assert comb(10, 3) == 120
    assert comb(0, 0) == 1

    # Edge cases
    # combinations of large numbers
    assert comb(20, 10) == 184756

    # Fractional division shouldn't happen because factorial returns integers
    # but the math operation `/` returns a float in Python 3.
    # Therefore comb() will return a float.
    assert isinstance(comb(5, 2), float)
