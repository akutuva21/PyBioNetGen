import os, glob
import pytest
from pytest import raises
import bionetgen as bng
from bionetgen.main import BioNetGenTest

tfold = os.path.dirname(__file__)


def test_network_parse():
    netfile = os.path.join(tfold, "mockup.net")
    from bionetgen.network.network import Network

    try:
        net = Network(netfile)
        res = True
    except:
        res = False
    assert res is True


def test_pattern_reader():
    patfile = os.path.join(tfold, "patterns.txt")
    from bionetgen.modelapi.pattern_reader import BNGPatternReader

    try:
        with open(patfile, "r") as f:
            patterns = f.readlines()
            for pattern in patterns:
                pat_obj = BNGPatternReader(pattern).pattern
                reparsed_pat = BNGPatternReader(str(pat_obj)).pattern
                if pat_obj != reparsed_pat:
                    raise RuntimeError(
                        f"Pattern can't be reparsed correctly, og: {pat_obj}, reparsed: {reparsed_pat}"
                    )
        res = True
    except:
        res = False
    assert res is True


def test_pattern_canonicalization():
    # for now, if the platform is windows, just skip
    if os.name == "nt":
        assert True is True
    # if pynauty is uninstalled, skip the test
    try:
        import pynauty
    except ImportError:
        assert True is True
        return
    # otherwise we will test canonicalization
    from bionetgen.modelapi.pattern_reader import BNGPatternReader

    # the testing file
    testfile = os.path.join(tfold, "canon_label_testing.txt")
    with open(testfile, "r+") as f:
        tests = f.readlines()
    # loop over tests
    res = True
    for ipat, pat in enumerate(tests):
        pat_splt = pat.split("    ")
        pat1, pat2 = pat_splt[0], pat_splt[1]
        try:
            # read patterns
            pat1_obj = BNGPatternReader(pat1).pattern
            pat2_obj = BNGPatternReader(pat2).pattern
            # compare them
            if pat1_obj != pat2_obj:
                res = False
                break
        except:
            res = False
            break
    # assert that everything matched up
    assert res is True


def test_zero_molecule_parsing():
    from bionetgen.modelapi.pattern_reader import BNGPatternReader

    pat_obj = BNGPatternReader("0").pattern
    assert len(pat_obj.molecules) == 1
    assert len(pat_obj.molecules[0].components) == 0
    assert str(pat_obj) == "0"


def test_action_normalization_drops_stray_backslashes_outside_quotes():
    from bionetgen.modelapi.bngparser import _normalize_action_text

    out = _normalize_action_text(
        'parameter_scan({n_scan_pts=>101,\\log_scale=>1,method=>"ode"})'
    )
    assert "\\" not in out
    assert "log_scale=>1" in out


def test_action_normalization_preserves_backslashes_inside_quotes():
    from bionetgen.modelapi.bngparser import _normalize_action_text

    out = _normalize_action_text('action({arg=>"a\\b"})')
    assert '"a\\b"' in out


def test_action_normalization_collapses_unquoted_double_commas():
    from bionetgen.modelapi.bngparser import _normalize_action_text

    out = _normalize_action_text(
        'simulate({method=>"ode",t_end=>3000,n_steps=>20,,print_functions=>1})'
    )
    assert ",," not in out
    assert ",n_steps=>20,print_functions=>1" in out


def test_action_normalization_preserves_double_commas_inside_quotes():
    from bionetgen.modelapi.bngparser import _normalize_action_text

    out = _normalize_action_text('something({xs=>"0,,1,,2"})')
    assert '"0,,1,,2"' in out


def _build_action_parser():
    from bionetgen.core.utils.utils import ActionList

    al = ActionList()
    al.define_parser()
    return al.action_parser


def test_action_parsing_exceptions():
    import pytest
    from bionetgen.modelapi.bngparser import BNGParser
    from bionetgen.core.exc import BNGParseError
    from bionetgen.modelapi.blocks import ActionBlock

    parser = BNGParser("dummy.bngl")
    ablock = ActionBlock()

    malformed_actions = [
        "invalid_action!",
        "simulate(t_end=>10) extra_stuff",
        'simulate({method=>"ode")',
    ]

    for action in malformed_actions:
        with pytest.raises(BNGParseError) as exc_info:
            parser._parse_action_line(action, ablock)
        assert "Failed to parse action" in str(exc_info.value)


# Issue #110: the list-valued action-argument grammar must accept the same
# forms BNG2.pl/Perl runs — scientific notation and an optional trailing
# comma — or `simulator='bngsim'` silently routes these models to the legacy
# stack. Mirrors the model forms seen in RuleHub (Mitra2019, Salazar-Cavazos2019).
@pytest.mark.parametrize(
    "action_text",
    [
        # Issue repro: e-notation in par_scan_vals.
        'parameter_scan({parameter=>"x",par_scan_vals=>[2.3e-10,5.1e-10],method=>"ode"})',
        # Mixed plain and decimal values.
        'parameter_scan({parameter=>"x",par_scan_vals=>[0.3,1,3],method=>"ode"})',
        # Zero plus e-notation values.
        'parameter_scan({parameter=>"x",par_scan_vals=>[0.0,0.05e-9,50.0e-9],method=>"ode"})',
        # Trailing comma plus e-notation (both gaps at once).
        'parameter_scan({parameter=>"x",par_scan_vals=>[2.3e-10,4.9e-07,],method=>"ode"})',
        # Quoted-string list still parses.
        'simulate({method=>"ode",foo=>["a","b"]})',
        # Empty list.
        'simulate({method=>"ode",foo=>[]})',
    ],
)
def test_action_grammar_accepts_perl_list_forms(action_text):
    parser = _build_action_parser()
    parser.parse_string(action_text, parse_all=True)


@pytest.mark.parametrize(
    "action_text",
    [
        # Double comma is genuinely malformed at the grammar level.
        'simulate({method=>"ode",foo=>[1,,2]})',
        # Unclosed list (no `]`).
        'simulate({method=>"ode",foo=>[1,2,})',
    ],
)
def test_action_grammar_still_rejects_malformed_lists(action_text):
    import pyparsing as pp

    parser = _build_action_parser()
    with raises(pp.ParseBaseException):
        parser.parse_string(action_text, parse_all=True)
