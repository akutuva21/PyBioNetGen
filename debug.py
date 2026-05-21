from bionetgen.atomizer.utils.pathwaycommons import name2uniprot
import urllib.request

import urllib.error
from unittest.mock import patch, MagicMock

print("Testing mock...")
with patch("urllib.request.urlopen") as mock_urlopen, patch(
    "bionetgen.atomizer.utils.pathwaycommons.logMess"
) as mock_logMess:
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="http://test.com", code=500, msg="Error", hdrs={}, fp=None
    )

    name2uniprot.cache = {}
    result = name2uniprot("EGFR", ["tax/9606"])
    print(mock_logMess.mock_calls)
    print("Result: ", result)
