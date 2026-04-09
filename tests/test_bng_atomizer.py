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

def test_get_size():
    from bionetgen.atomizer.utils.util import get_size

    class HasGetSize:
        def getSize(self):
            return 1

    class HasSize:
        def size(self):
            return 2

    class HasGetLength:
        def getLength(self):
            return 3

    class HasLen:
        def __len__(self):
            return 4

    class HasNone:
        pass

    assert get_size(HasGetSize()) == 1
    assert get_size(HasSize()) == 2
    assert get_size(HasGetLength()) == 3
    assert get_size(HasLen()) == 4
    assert get_size(HasNone()) == 0
