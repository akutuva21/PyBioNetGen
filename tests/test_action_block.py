import pytest
from bionetgen.modelapi.blocks import ActionBlock


def test_action_block_iter():
    """Test that ActionBlock iteration works correctly."""
    ab = ActionBlock()
    ab.add_action("simulate", {"method": "ode", "t_end": 10})
    ab.add_action("generate_network", {"overwrite": 1})
    ab.add_action("simulate", {"method": "ssa", "t_end": 20})

    count = 0
    for i in ab:
        count += 1

    assert count == 3
