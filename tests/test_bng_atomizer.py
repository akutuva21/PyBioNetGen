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

def test_factorial():
    from bionetgen.atomizer.sbml2json import factorial
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(5) == 120
    assert factorial(10) == 3628800
