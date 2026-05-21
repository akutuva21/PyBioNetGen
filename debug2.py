from bionetgen.atomizer.utils.pathwaycommons import name2uniprot
import urllib.error
from unittest.mock import patch, MagicMock

with patch("urllib.request.urlopen") as mock_urlopen:
    mock_response = MagicMock()
    mock_response.read.return_value = ""

    def side_effect(*args, **kwargs):
        print(f"Call count: {mock_urlopen.call_count}")
        if mock_urlopen.call_count == 1:
            return mock_response
        raise urllib.error.HTTPError(url="http://test.com", code=500, msg="Error", hdrs={}, fp=None)

    mock_urlopen.side_effect = side_effect

    name2uniprot.cache = {}
    result = name2uniprot("EGFR", ["tax/9606"])
    print("Fallback HTTP Error Result:", result)
