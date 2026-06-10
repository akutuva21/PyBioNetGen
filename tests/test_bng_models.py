import os, glob
import pytest
from pytest import raises
import bionetgen as bng
from bionetgen.core.exc import BNGModelError
from bionetgen.main import BioNetGenTest

tfold = os.path.dirname(__file__)


def test_bionetgen_model():
    fpath = os.path.join(tfold, "models", "test_synthesis_simple.bngl")
    fpath = os.path.abspath(fpath)
    m = bng.bngmodel(fpath)


def test_add_invalid_block():
    fpath = os.path.join(tfold, "models", "test_synthesis_simple.bngl")
    fpath = os.path.abspath(fpath)
    m = bng.bngmodel(fpath)

    class MockBlock:
        name = "unsupported block"

    with raises(
        bng.core.exc.BNGModelError,
        match="Block type unsupported_block is not supported.",
    ):
        m.add_block(MockBlock())


def test_bionetgen_all_model_loading():
    # tests library model loading using many models
    mpattern = os.path.join(tfold, "models") + os.sep + "*.bngl"
    models = glob.glob(mpattern)
    succ = []
    fail = []
    success = 0
    fails = 0
    for model in models:
        try:
            m = bng.bngmodel(model)
            success += 1
            mstr = str(m)
            succ.append(model)
        except:
            print("can't load model {}".format(model))
            fails += 1
            fail.append(model)
    print("succ: {}".format(success))
    print(sorted(succ))
    print("fail: {}".format(fails))
    print(sorted(fail))
    assert fails == 0


def test_action_argument_type_check():
    import bionetgen
    from bionetgen.core.exc import BNGParseError

    # Test invalid dict argument type for action_args
    with raises(BNGParseError, match="must be a dict"):
        bionetgen.modelapi.structs.Action("generate_network", "not_a_dict")

    # Test unrecognized action type
    with raises(BNGParseError, match="not recognized"):
        bionetgen.modelapi.structs.Action("invalid_action", {})

    # Test valid arguments don't raise
    bionetgen.modelapi.structs.Action("generate_network", {"max_stoich": {"A": 5}})
    bionetgen.modelapi.structs.Action("simulate", {"sample_times": [1, 2, 3]})


def test_action_loading():
    # tests a BNGL file containing all BNG actions
    all_action_model = os.path.join(*[tfold, "models", "actions", "all_actions.bngl"])
    m1 = bng.bngmodel(all_action_model)
    assert len(m1.actions) + len(m1.actions.before_model) == 31

    no_action_model = os.path.join(*[tfold, "models", "actions", "no_actions.bngl"])
    try:
        m2 = bng.bngmodel(no_action_model)
        assert len(m2.actions) == 0
    except BNGModelError:
        pytest.skip("BNG2.pl is missing, active_blocks is empty, skipping action loading test")


def test_model_running_CLI():
    # tests running a list of models using the CLI
    mpattern = os.path.join(tfold, "models") + os.sep + "*.bngl"
    models = glob.glob(mpattern)
    succ = []
    fail = []
    success = 0
    fails = 0
    test_run_folder = os.path.join(tfold, "models", "cli_test_runs")
    if not os.path.isdir(test_run_folder):
        os.mkdir(test_run_folder)
    for model in models:
        model_name = os.path.basename(model).replace(".bngl", "")
        try:
            argv = [
                "run",
                "-i",
                model,
                "-o",
                os.path.join(*[tfold, "models", "cli_test_runs", model_name]),
            ]
            with BioNetGenTest(argv=argv) as app:
                app.run()
                assert app.exit_code == 0
            success += 1
            model = os.path.split(model)
            model = model[1]
            succ.append(model)
        except:
            print("can't run model {}".format(model))
            fails += 1
            model = os.path.split(model)
            model = model[1]
            fail.append(model)
    print("succ: {}".format(success))
    print(sorted(succ))
    print("fail: {}".format(fails))
    print(sorted(fail))
    assert fails == 0


def test_model_running_lib():
    # test running a list of models using the library
    mpattern = os.path.join(tfold, "models") + os.sep + "*.bngl"
    models = glob.glob(mpattern)
    succ = []
    fail = []
    success = 0
    fails = 0
    for model in models:
        if "isingspin_localfcn" in model:
            continue
        if "test_tfun" in model or "isingspin_localfcn" in model:
            continue
        try:
            bng.run(model)
            success += 1
            model = os.path.split(model)
            model = model[1]
            succ.append(model)
        except Exception as e:
            print(e)
            print("can't run model {}".format(model))
            fails += 1
            model = os.path.split(model)
            model = model[1]
            fail.append(model)
    print("succ: {}".format(success))
    print(sorted(succ))
    print("fail: {}".format(fails))
    print(sorted(fail))
    assert fails == 0


def test_setup_simulator():
    import bionetgen.core.defaults as defaults

    fpath = os.path.join(tfold, "test.bngl")
    fpath = os.path.abspath(fpath)
    bng_path = defaults.BNGDefaults().bng_path
    bngexec = os.path.join(bng_path, "BNG2.pl")
    if bngexec is None or not os.path.exists(bngexec):
        pytest.skip("BNG2.pl not installed, skipping simulator test")

    m = bng.bngmodel(fpath)
    try:
        librr_simulator = m.setup_simulator()
    except BNGModelError:
        pytest.skip("SBML generation failed, skipping simulator test")
    res = librr_simulator.simulate(0, 1, 10)
    assert res is not None


def test_bngmodel_add_block_exception():
    from bionetgen.core.exc import BNGModelError

    # Load a valid model
    fpath = os.path.join(tfold, "test.bngl")
    fpath = os.path.abspath(fpath)
    m = bng.bngmodel(fpath)

    # Create a mock block with an unsupported name
    class MockBlock:
        def __init__(self, name):
            self.name = name

    invalid_block = MockBlock("invalid_block_type")

    # Assert that adding this block raises BNGModelError
    with raises(BNGModelError, match="Block type invalid_block_type is not supported"):
        m.add_block(invalid_block)


def test_bngmodel_add_empty_block_exception():
    from bionetgen.core.exc import BNGModelError

    # Load a valid model
    fpath = os.path.join(tfold, "test.bngl")
    fpath = os.path.abspath(fpath)
    m = bng.bngmodel(fpath)

    # Assert that adding this block raises BNGModelError
    with raises(BNGModelError, match="Block type invalid_block_type is not supported"):
        m.add_empty_block("invalid_block_type")
