import pytest
from unittest.mock import patch, MagicMock
from bionetgen.core.tools.gdiff import BNGGdiff


def test_get_color_id_exception():
    gdiff = BNGGdiff.__new__(BNGGdiff)
    gdiff.app = MagicMock()
    gdiff.logger = MagicMock()

    node = MagicMock()

    with patch.object(gdiff, "_get_node_color", return_value="#UNKNOWN_COLOR"):
        with pytest.raises(
            RuntimeError, match="Node color #UNKNOWN_COLOR doesn't match known colors"
        ):
            gdiff._get_color_id(node)
