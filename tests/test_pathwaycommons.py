import urllib.request
import urllib.error
from unittest.mock import patch
from bionetgen.atomizer.utils.pathwaycommons import name2uniprot


def test_name2uniprot_organism_httperror():
    with patch("urllib.request.urlopen") as mock_urlopen:
        # Create an HTTPError instance
        # HTTPError requires url, code, msg, hdrs, fp
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://www.uniprot.org/uniprot/?",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None,
        )

        # Call the function with an organism to hit the target try/except block
        result = name2uniprot("TestGene", ["http://identifiers.org/taxonomy/9606"])

        # The function should catch the HTTPError and return None
        assert result is None
