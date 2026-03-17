import pytest

from bionetgen.core.utils.utils import ActionList


def test_action_parser_rejects_unclosed_brace():
    """Ensure malformed actions (missing closing brace) raise a parsing error."""

    alist = ActionList()
    alist.define_parser()

    # Missing closing '}' should cause pyparsing to raise an exception
    malformed = "simulate_ssa({t_start=>0,t_end=>10"  # missing closing '}' and ')'

    with pytest.raises(Exception):
        alist.action_parser.parseString(malformed)
