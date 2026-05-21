import re

with open("tests/test_pathwaycommons.py", "r") as f:
    content = f.read()

# Replace mock responses from bytes to str or let mock_response.read() return bytes and decode it, wait no,
# python's read() on mock was returning bytes, but the str(response) on bytes yields "b'Entry...'", so .split('\n') doesnt work!
# we just need to return bytes but decoded inside the real code if the real code decodes it?
# The real code:
# response = urllib.request.urlopen(url, data=data).read()
# parsedData = [x.split("\t") for x in str(response).split("\n")][1:]
# wait, if urllib returns bytes, str(response) will literally be "b'Entry...'"! Let's check python 3 urllib behavior.
