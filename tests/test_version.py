import sys
import unittest
from unittest.mock import patch, mock_open
import importlib


class TestVersionParsing(unittest.TestCase):
    def setUp(self):
        # Save original version to restore later
        import bionetgen.core.version as version_mod

        self.original_version = version_mod.VERSION

    def tearDown(self):
        # Restore the module to its original state
        import bionetgen.core.version as version_mod

        with patch(
            "builtins.open",
            mock_open(read_data=" ".join(map(str, self.original_version))),
        ):
            importlib.reload(version_mod)

    def test_version_parsing_with_string(self):
        with patch("builtins.open", mock_open(read_data="1 2 3 alpha 4")):
            import bionetgen.core.version as version_mod

            importlib.reload(version_mod)
            self.assertEqual(version_mod.VERSION, (1, 2, 3, "alpha", 4))

    def test_version_parsing_all_ints(self):
        with patch("builtins.open", mock_open(read_data="1 2 3 4 5")):
            import bionetgen.core.version as version_mod

            importlib.reload(version_mod)
            self.assertEqual(version_mod.VERSION, (1, 2, 3, 4, 5))

    def test_version_parsing_missing_parts(self):
        with patch("builtins.open", mock_open(read_data="1 2")):
            import bionetgen.core.version as version_mod

            importlib.reload(version_mod)
            self.assertEqual(version_mod.VERSION, (1, 2, 0, 0, 0))


if __name__ == "__main__":
    unittest.main()
